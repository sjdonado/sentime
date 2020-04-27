import sys
import re
import string
import csv
import pandas as pd

# function that removes the mentions and URLS. String begining with @
def remove_mentions_urls(text):
  tweet_out = re.sub(r'pic.twitter\S+', '', text)
  tweet_out = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet_out)
  tweet_out = re.sub(r'@[A-Za-z0-9]+', '', tweet_out)
  return tweet_out

def remove_non_alphanumeric(text):
  text_out = "".join([char for char in text if char not in string.punctuation and (char != '\n' and char != '\r')])
  return text_out

if __name__ == '__main__':
  date = sys.argv[1]
  if date is None:
    print("Error: date arg is required")
    exit(1)
    
  tweets = pd.read_csv("{}_tweets.csv".format(date), encoding='UTF-8')

  tweets['tweet_noment_nourl'] = tweets['tweet'].apply(lambda x: remove_mentions_urls(x))
  tweets['tweet_parsed'] = tweets['tweet_noment_nourl'].apply(lambda x: remove_non_alphanumeric(x))

  output_path = "{}_tweets_parsed.txt".format(date)
  tweets['tweet_parsed'].to_csv(output_path, header=None, index=None, sep='\n', quoting=csv.QUOTE_NONE)
  print("{} saved successfully".format(output_path))
