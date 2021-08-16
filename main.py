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
from secrets import user_agent, client_id, client_secret
import time
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date

print("\nRunning sentiment analysis, this may take a few minutes...\n")

# Instantiate praw object
start_time = time.time()
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
picks = 10     # define # of picks here, prints as "Top ## picks are:"
picks_ayz = 10   # define # of picks for sentiment analysis
posts, count, c_analyzed, tickers, titles, a_comments = 0, 0, 0, {}, [], {}
cmt_auth = {}

for sub in subs:
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
        if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in post_flairs or flair is None) and author not in ignoreAuthP:
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

# sorts the dictionary
symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True))
top_picks = list(symbols.keys())[0:picks]
time = (time.time() - start_time)

# print top picks
print("It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.\n".format(t=time,
                                                                                                c=c_analyzed,
                                                                                                p=posts,
                                                                                                s=len(subs)))
print("Posts analyzed saved in titles")
# for i in titles: print(i) # prints the title of the posts analyzed

print(f"\n{picks} most mentioned picks: ")
times = []
top = []
for i in top_picks:
    print(f"{i}: {symbols[i]}")
    times.append(symbols[i])
    top.append(f"{i}: {symbols[i]}")

# Applying sentiment analysis
scores, s = {}, {}

vader = SentimentIntensityAnalyzer()
# adding custom words from data.py
vader.lexicon.update(new_words)

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

# Printing sentiment analysis
print(f"\nSentiment analysis of top {picks_ayz} picks:")
df = pd.DataFrame(scores)
df.index = ['Bearish', 'Neutral', 'Bullish', 'Total_Compound']
df = df.T
print(df)

# Data Visualization
# Most mentioned picks
squarify.plot(sizes=times, label=top, alpha=0.7)
plt.axis('off')
plt.title(f"{picks} most mentioned picks")
plt.show()

# Sentiment analysis
df = df.astype(float)
colors = ['red', 'springgreen', 'forestgreen', 'coral']
df.plot(kind='bar', color=colors, title=f"Sentiment analysis of top {picks_ayz} picks:")
plt.show()

# append date column to dataframe for storing in database
df['date'] = [date.today() for x in range(df.shape[0])]
df.reset_index(inplace=True)
df.rename(columns={'index': 'stock'}, inplace=True)

# Save current top wsb stocks to csv file
df.to_csv('df.csv')