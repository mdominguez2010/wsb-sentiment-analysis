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
from data import *
from credentials import user_agent, client_id, client_secret
import time
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date

class crawlSubreddit:

    def __init__(self, subs):
        self.subs = subs
        self.post_flairs = post_flairs
        self.goodAuth = goodAuth
        self.uniqueCmt = uniqueCmt
        self.ignoreAuthP = ignoreAuthP
        self.ignorAuthC = ignoreAuthC
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
        ***REMOVED***
        Crawls the subreddits and performs analysis
        ***REMOVED***
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
                if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in self.post_flairs or flair is None) and author not in ignoreAuthP:
                    submission.comment_sort = 'new'
                    comments = submission.comments
                    titles.append(submission.title)
                    posts += 1
                    submission.comments.replace_more(limit = limit)
                    for comment in comments:
                        # try except for deleted account?
                        try:
                            auth = comment.author.name
                        except:
                            pass
                        c_analyzed += 1

                        # checking: comment upvotes and author
                        if comment.score > upvotes and auth not in ignoreAuthC:
                            split = comment.body.split(' ')
                            for word in split:
                                word = word.replace("$", "")
                                # upper = ticker, length of ticker <= 5, excluded words
                                if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks:
                                    
                                    # unique comments, try/except for key errors
                                    if uniqueCmt and auth not in goodAuth:
                                        try:
                                            if auth in cmt_auth[word]:
                                                break
                                        except:
                                            pass
                                    
                                    # counting tickers
                                    if word in tickers:
                                        tickers[word] += 1
                                        a_comments[word].append(comment.body)
                                        cmt_auth[word].append(auth)
                                        count += 1
                                    else:
                                        tickers[word] = 1
                                        cmt_auth[word] = [auth]
                                        a_comments[word] = [comment.body]
                                        count += 1

        return tickers, posts

class cleanData:

    def __init__(self, tickers, picks):
        self.tickers = tickers
        self.picks = picks

    def sort_dictionary(self):
        ***REMOVED***
        Sorts the dictionary
        ***REMOVED***
        symbols = dict(sorted(self.tickers.items(), key=lambda item: item[1], reverse = True))
        top_picks = list(symbols.keys())[0:self.picks]

        return symbols, top_picks

class userFeedback:

    def time_it(self):
        return time.time()

    def print_top_picks(self, run_time, c_analyzed, posts, subs):
        # print top picks
        print("It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.\n".format(t=run_time,
                                                                                                        c=c_analyzed,
                                                                                                        p=posts,
                                                                                                        s=len(subs)))

    def print_most_mentioned(self, picks):
        print(f"\n{picks} most mentioned picks: ")
        times = []
        top = []
        for i in top_picks:
            print(f"{i}: {symbols[i]}")
            times.append(symbols[i])
            top.append(f"{i}: {symbols[i]}")

        return times, top

class sentimentAnalysis:
    
    def vaderSentiment(self, vader):

        # adding custom words from data.py
        vader.lexicon.update(new_words)
        scores, s = {}, {}
        picks_sentiment = list(symbols.keys())[0: picks_ayz]
        for symbol in picks_sentiment:
            stock_comments = a_comments[symbol]
            for cmnt in stock_comments:
                score = vader.polarity_scores(cmnt)
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
        print(f"\nSentiment analysis of top {picks_ayz} picks:")
        df = pd.DataFrame(scores)
        df.index = ['Bearish', 'Neutral', 'Bullish', 'Total_Compound']
        df = df.T
        print(df)

        return df

    def plot_details(self, times, top, df):
        ***REMOVED***
        Data visualization. Most mentioned picks and sentiment analysis
        ***REMOVED***
        squarify.plot(sizes=times, label=top, alpha=0.7)
        plt.axis('off')
        plt.title(f"{picks} most mentioned picks")
        plt.show()

        # Sentiment analysis
        df = df.astype(float)
        colors = ['red', 'springgreen', 'forestgreen', 'coral']
        df.plot(kind='bar', color=colors, title=f"Sentiment analysis of top {picks_ayz} picks:")
        plt.show()

class Saving:

    def __init__(self, df):
        self.df = df
    
    def save_csv(self, df):
        ***REMOVED***
        Preps dataframe then saves as csv in current directory
        ***REMOVED***
        # append date column to dataframe for storing in database
        df['date'] = [date.today() for x in range(df.shape[0])]
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'stock'}, inplace=True)

        # Save current top wsb stocks to csv file
        df.to_csv('df.csv')

if __name__ == "__main__":

    start_time = userFeedback.time_it()

    print("\nRunning sentiment analysis, this may take a few minutes...\n")
    
    reddit = praw.Reddit(
        user_agent = user_agent,
        client_id = client_id,
        client_secret = client_secret
    )

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
    count, tickers, titles, a_comments = 0, {}, [], {}
    cmt_auth = {}
    
    crawlSubreddit = crawlSubreddit(
        subs=subs, post_flairs=post_flairs, goodAuth=goodAuth, uniqueCmt=uniqueCmt,
        ignoreAuthP=ignoreAuthP, ignoreAuthC=ignoreAuthC, upvoteRatio=upvoteRatio,
        ups=ups, limit=limit, upvotes=upvotes, posts=posts, c_analyzed=c_analyzed,
        count=count, tickers=tickers, titles=titles, a_comments=a_comments, cmt_auth=cmt_auth
    )

    tickers, posts = crawlSubreddit.extract_tickers()

    cleanData = cleanData(tickers=tickers, picks=picks)
    symbols, top_picks = cleanData.sort_dictionary(tickers=tickers, picks=picks)


    end_time = userFeedback.time_it()
    run_time = end_time - start_time

    userFeedback.print_top_picks(run_time, c_analyzed, posts, subs)
    times, top = userFeedback.print_most_mentioned(picks)

    ### Sentiment Analysis ###
    picks_ayz = 10   # define # of picks for sentiment analysis

    vader = SentimentIntensityAnalyzer()
    # adding custom words from data.py
    vader.lexicon.update(new_words)

    scores, s = sentimentAnalysis.vaderSentiment(vader)

    df = sentimentAnalysis.print_details(scores=scores)

    sentimentAnalysis.plot_details(times, top, df)

    Saving.save_csv(df)








    

