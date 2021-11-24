'''
Purpose: To analyze the sentiments of the reddit
This program uses Vader SentimentIntensityAnalyzer
to calculate the ticker compound value.
You can change multiple parameters to suit your needs.
See below u nder "set program parameters."

Implementation:
I am using sets for 'x in s' comparison, sets time complexity for "x in s" is O(1) compare to list: O(n).

Limitations:
It depends mainly on the defined parameters for current implementation:
It completely ignores the heavily downvoted comments, and there can be a time when
the most mentioned ticker is heavily downvoted, but you can change that in upvotes variable.
Author: github:asad70
'''

#  Import Libraries
import pandas as pd
import praw
from stocks_to_trade import *
from secrets import user_agent, client_id, client_secret
import time
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date
import update_financials

class crawlSubreddit:

    def __init__(self, subs, post_flairs, goodAuth, uniqueCmt,
                 ignoreAuthP, ignoreAuthC, upvoteRatio, ups,
                 limit, upvotes, posts, c_analyzed, count, tickers,
                 titles, a_comments, cmt_auth
                 ):
        self.subs = subs
        self.post_flairs = post_flairs
        self.goodAuth = goodAuth
        self.uniqueCmt = uniqueCmt
        self.ignoreAuthP = ignoreAuthP
        self.ignoreAuthC = ignoreAuthC
        self.upvoteRatio = upvoteRatio
        self.ups = ups
        self.limit = limit
        self.upvotes = upvotes
        self.posts = posts
        self.c_analyzed = c_analyzed
        self.count = count
        self.tickers = tickers
        self.titles = titles
        self.a_comments = a_comments
        self.cmt_auth = cmt_auth

    def extract_tickers(self):
        """
        Crawls the subreddits and performs analysis
        """
        for sub in self.subs:
            subreddit = reddit.subreddit(sub)
            hot_python = subreddit.hot() # sorting posts by hot
            # Extracting comments, symbols from subreddit
            for submission in hot_python:
                # print(submission)
                flair = submission.link_flair_text
                # print(flair)
                try:
                    author = submission.author.name
                except AttributeError:
                    pass
                #print(author)

                # Checking: post upvote ratio # of upvotes, post flair, and author
                if submission.upvote_ratio >= self.upvoteRatio and submission.ups > self.ups and (flair in self.post_flairs or flair is None) and author not in ignoreAuthP:
                    submission.comment_sort = 'new'
                    comments = submission.comments
                    titles.append(submission.title)
                    self.posts += 1
                    submission.comments.replace_more(limit = limit)
                    for comment in comments:
                        # try except for deleted account?
                        try:
                            auth = comment.author.name
                        except:
                            pass
                        self.c_analyzed += 1

                        # checking: comment upvotes and author
                        if comment.score > self.upvotes and auth not in self.ignoreAuthC:
                            split = comment.body.split(' ')
                            for word in split:
                                word = word.replace("$", "")
                                # upper = ticker, length of ticker <= 5, excluded words
                                if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks:
                                    
                                    # unique comments, try/except for key errors
                                    if uniqueCmt and auth not in self.goodAuth:
                                        try:
                                            if auth in self.cmt_auth[word]:
                                                break
                                        except:
                                            pass
                                    
                                    # counting tickers
                                    if word in tickers:
                                        tickers[word] += 1
                                        a_comments[word].append(comment.body)
                                        cmt_auth[word].append(auth)
                                        self.count += 1
                                    else:
                                        tickers[word] = 1
                                        cmt_auth[word] = [auth]
                                        a_comments[word] = [comment.body]
                                        self.count += 1

        return tickers, posts

class cleanData:

    def __init__(self, tickers, picks):
        self.tickers = tickers
        self.picks = picks

    def sort_dictionary(self):
        """
        Sorts the dictionary
        """
        symbols = dict(sorted(self.tickers.items(), key=lambda item: item[1], reverse = True))
        top_picks = list(symbols.keys())[0:self.picks]

        return symbols, top_picks

class userFeedback:

    def __init__(self, c_analyzed, posts, subs, picks, top_picks, symbols):
        self.c_analyzed = c_analyzed
        self.posts = posts
        self.subs = subs
        self.picks = picks
        self.top_picks = top_picks
        self.symbols = symbols

    def print_top_picks(self):
        # print top picks
        print("It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.\n".format(t=self.run_time,
                                                                                                        c=self.c_analyzed,
                                                                                                        p=self.posts,
                                                                                                        s=len(self.subs)))

    def print_most_mentioned(self):
        print(f"\n{self.picks} most mentioned picks: ")
        times = []
        top = []
        for i in self.top_picks:
            print(f"{i}: {self.symbols[i]}")
            times.append(self.symbols[i])
            top.append(f"{i}: {self.symbols[i]}")

        return times, top

class sentimentAnalysis:
    
    def __init__(self, vader, symbols, picks_ayz, a_comments, times, top, picks):
        self.vader = vader
        self.symbols = symbols
        self.picks_ayz = picks_ayz
        self.a_comments = a_comments
        self.times = times
        self.top = top
        self.picks = picks

    def vaderSentiment(self):

        # adding custom words from data.py
        self.vader.lexicon.update(new_words)
        scores, s = {}, {}
        picks_sentiment = list(self.symbols.keys())[0: self.picks_ayz]
        for symbol in picks_sentiment:
            stock_comments = self.a_comments[symbol]
            for cmnt in stock_comments:
                score = self.vader.polarity_scores(cmnt)
                if symbol in s:
                    s[symbol][cmnt] = score
                else:
                    s[symbol] = {cmnt: score}
                if symbol in scores:
                    for key, _ in score.items():
                        scores[symbol][key] += score[key]
                else:
                    scores[symbol] = score

            # calculating averages
            for key in score:
                scores[symbol][key] = scores[symbol][key] / symbols[symbol]
                scores[symbol][key] = "{pol:.3f}".format(pol=scores[symbol][key])

        return scores, s

    def print_details(self, scores):
        '''
        Printing sentiment analysis
        '''
        print(f"\nSentiment analysis of top {self.picks_ayz} picks:")
        df = pd.DataFrame(scores)
        df.index = ['Bearish', 'Neutral', 'Bullish', 'Total_Compound']
        df = df.T
        print(df)

        return df

    def plot_details(self, df):
        """
        Data visualization. Most mentioned picks and sentiment analysis
        """
        squarify.plot(sizes=self.times, label=self.top, alpha=0.7)
        plt.axis('off')
        plt.title(f"{self.picks} most mentioned picks")
        plt.show()

        # Sentiment analysis
        df = df.astype(float)
        colors = ['red', 'springgreen', 'forestgreen', 'coral']
        df.plot(kind='bar', color=colors, title=f"Sentiment analysis of top {picks_ayz} picks:")
        plt.show()

class Saving:

    def __init__(self, df, date):
        self.df = df
        self.date = date
    
    def save_csv(self):
        """
        Preps dataframe then saves as csv in current directory
        """
        # append date column to dataframe for storing in database
        self.df['date'] = [self.date.today() for x in range(self.df.shape[0])]
        self.df.reset_index(inplace=True)
        self.df.rename(columns={'index': 'stock'}, inplace=True)

        # Save current top wsb stocks to csv file
        self.df.to_csv('./data/df.csv')

def time_it(time):
    '''
    Records time
    '''
    return time.time()

def print_run_time(start, end):
    '''
    Prints program run time
    '''
    run_time = end - start
    print("Program run time: %.0f" % run_time, "seconds")


if __name__ == "__main__":

    # Set program parameters
    subs = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']     # sub-reddit to search
    post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}    # posts flairs to search || None flair is automatically considered
    goodAuth = {'AutoModerator'}   # authors whom comments are allowed more than once
    uniqueCmt = True                # allow one comment per author per symbol
    ignoreAuthP = {'example'}       # authors to ignore for posts 
    ignoreAuthC = {'example'}       # authors to ignore for comment 
    upvoteRatio = 0.70         # upvote ratio for post to be considered, 0.70 = 70%
    ups = 20       # define # of upvotes, post is considered if upvotes exceed this #
    limit = 10      # define the limit, comments 'replace more' limit
    upvotes = 2     # define # of upvotes, comment is considered if upvotes exceed this #
    posts = 0
    c_analyzed = 0
    picks = 10     # define # of picks here, prints as "Top ## picks are:"
    picks_ayz = 10   # define # of picks for sentiment analysis
    count, tickers, titles, a_comments = 0, {}, [], {}
    cmt_auth = {}

    start_time = time_it(time)

    print("\nRunning program, this may take a few minutes...\n")
    
    reddit = praw.Reddit(
        user_agent = user_agent,
        client_id = client_id,
        client_secret = client_secret
    )

    crawlSubreddit = crawlSubreddit(
        subs=subs, post_flairs=post_flairs, goodAuth=goodAuth, uniqueCmt=uniqueCmt,
        ignoreAuthP=ignoreAuthP, ignoreAuthC=ignoreAuthC, upvoteRatio=upvoteRatio,
        ups=ups, limit=limit, upvotes=upvotes, posts=posts, c_analyzed=c_analyzed,
        count=count, tickers=tickers, titles=titles, a_comments=a_comments, cmt_auth=cmt_auth
    )

    tickers, posts = crawlSubreddit.extract_tickers()

    cleanData = cleanData(tickers=tickers, picks=picks)
    symbols, top_picks = cleanData.sort_dictionary()

    # userFeedback.print_top_picks(run_time, c_analyzed, posts, subs)
    # times, top = userFeedback.print_most_mentioned(picks)

    feedback = userFeedback(c_analyzed=c_analyzed, posts=posts,
                            subs=subs, picks=picks, top_picks=top_picks,
                            symbols=symbols)
    
    feedback.print_top_picks
    times, top = feedback.print_most_mentioned()

    ### Sentiment Analysis ###
    

    vader = SentimentIntensityAnalyzer()
    # adding custom words from data.py
    vader.lexicon.update(new_words)

    sentiment_analysis = sentimentAnalysis(vader=vader, symbols=symbols,
                                           picks_ayz=picks_ayz, a_comments=a_comments,
                                           times=times, top=top, picks=picks)

    scores, s = sentiment_analysis.vaderSentiment()

    df = sentiment_analysis.print_details(scores=scores)

    sentiment_analysis.plot_details(df)

    saving = Saving(df, date)
    saving.save_csv()
    
    # Extract recent financials, update dataframe, and save as csv
    historic_sentiment_analysis = update_financials.main_program()

    end_time = time_it(time)
    print_run_time(start=start_time, end=end_time)








    

