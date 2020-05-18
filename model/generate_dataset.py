import os
import sys
import json
import csv
from cleaner import clean_tweet

def write_dataset(path, tweets, labels):
  with open(path, 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['tweet', 'sentiment'])
    for idx, tweet in enumerate(tweets):
      csv_out.writerow([tweet, labels[idx][1]])

  print("Saved {} tweets at {}".format(len(tweets), path))

def create_folder(path):
  if not os.path.exists(path):
    os.makedirs(path)
  return path

if __name__ == '__main__':
  date = sys.argv[1]
  if date is None:
    print("Error: date arg is required")
    exit(1)

  labels = []
  tweets = []
  dataset_path = os.path.join(os.getcwd(), 'data', date)

  output_path = os.path.join(dataset_path, "aws_output")
  output = open(output_path, 'r')
  for line in output.readlines():
    data = json.loads(line)
    if data['Line']:
      labels.append((data['Line'] + 1, data['Sentiment']))

  labels.sort(key=lambda tup: tup[0])

  tweets_path = os.path.join(dataset_path, "tweets_parsed.txt")
  tweets_input = open(tweets_path, 'r')
  for line in tweets_input.readlines():
    tweets.append(line.strip())

  # Clean tweets
  tweets = [clean_tweet(tweet, remove_emojis=True) for tweet in tweets]

  # Split dataset
  limit = round(len(tweets) * 0.7)

  dataset_path = create_folder(os.path.join(dataset_path, "dataset"))
  train_folder = create_folder(os.path.join(dataset_path, "train"))
  test_folder = create_folder(os.path.join(dataset_path, "test"))

  write_dataset(os.path.join(train_folder, "data.csv"),
    tweets[:limit], labels[:limit])
  
  write_dataset(os.path.join(test_folder, "data.csv"),
    tweets[limit + 1:], labels[limit + 1:])
