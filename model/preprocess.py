import os
import sys
import csv
import pandas as pd
from cleaner import clean_tweet

if __name__ == '__main__':
  date = sys.argv[1]
  if date is None:
    print("Error: date arg is required")
    exit(1)
    
  tweets_path = os.path.join(os.getcwd(), 'data', date, "tweets.csv")

  tweets = pd.read_csv(tweets_path, encoding='UTF-8')
  tweets = pd.DataFrame([clean_tweet(tweet) for tweet in tweets])
  tweets = tweets[tweets != '']

  output_path = os.path.join(os.getcwd(), 'data', date, "tweets_parsed.txt")
  tweets.to_csv(output_path, header=None, index=None, sep='\n', quoting=csv.QUOTE_NONE)
  print("{} saved successfully".format(output_path))
