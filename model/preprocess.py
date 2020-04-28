import os
import sys
import re
import csv
import pandas as pd
import string

# function that removes the mentions and URLS. String begining with @
def remove_mentions_urls(text):
  tweet_out = re.sub(r'pic.twitter\S+', '', text)
  tweet_out = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet_out)
  tweet_out = re.sub(r'@[A-Za-z0-9]+', '', tweet_out)
  return tweet_out

def remove_non_alphanumeric(text):
  # Remove multiple spaces
  text = re.sub(r'\s\s+', ' ', text.lower())
  # Remove breaklines and puntuaction
  text_out = "".join([char for char in text if char != string.punctuation and char != '\n' and char != '\r']).strip()

  return text_out

if __name__ == '__main__':
  date = sys.argv[1]
  if date is None:
    print("Error: date arg is required")
    exit(1)
    
  tweets_path = os.path.join(os.getcwd(), 'model', 'data', "{}_tweets.csv".format(date))
  tweets = pd.read_csv(tweets_path, encoding='UTF-8')

  tweets['tweet_noment_nourl'] = tweets['tweet'].apply(lambda t: remove_mentions_urls(t))
  tweets['tweet_parsed'] = tweets['tweet_noment_nourl'].apply(lambda t: remove_non_alphanumeric(t))
  clean_tweets = pd.DataFrame([t for t in tweets['tweet_parsed'] if t != ''])

  output_path = os.path.join(os.getcwd(), 'model', 'data', "{}_tweets_parsed.txt".format(date))
  clean_tweets.to_csv(output_path, header=None, index=None, sep='\n', quoting=csv.QUOTE_NONE)
  print("{} saved successfully".format(output_path))
