import os
import datetime
import joblib
import pandas as pd
import GetOldTweets3 as got
import time

def getTuits(user, since, until):
    
    if not os.path.exists(f'database/{user}'):
        os.makedirs(f'database/{user}')
    
    tweetCriteria = got.manager.TweetCriteria().setUsername(user)\
                                       .setSince(since)\
                                       .setUntil(until)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
    tweets_df = pd.DataFrame(user_tweets)
    tweets_df.columns = ['date', 'tweet']
    
    joblib.dump(tweets_df,f'database/{user}/{user}.pkl')

user = input('User: ')
print(user)
print('FROM: ')
from_year = input('from year: ')
from_month = input('from month: ')
from_day = input('from day: ')
start = datetime.datetime(int(from_year), int(from_month), int(from_day))
print(f'From {start}')
print('Until: ')
to_year = input('to year: ')
to_month = input('to month: ')
to_day = input('to day: ')
end = datetime.datetime(int(to_year), int(to_month), int(to_day))
print(f'From {end}')

start = time.time()

getTuits(user, f"{from_year}-{from_month}-{from_day}", f"{to_year}-{to_month}-{to_day}")

end = time.time()
print(f"Runtime of the program is {end - start}")