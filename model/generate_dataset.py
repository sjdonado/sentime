import os
import sys
import json
import csv
from cleaner import clean_tweet

def write_dataset(path, tweets):
  with open(path, 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['tweet', 'sentiment'])
    for tweet in tweets:
      if tweet[1] != 'NONE':
        csv_out.writerow([tweet[0], tweet[1]])

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

  tweets_path = os.path.join(dataset_path, "tweets_parsed.txt")
  tweets_input = open(tweets_path, 'r')
  for line in tweets_input.readlines():
    tweets.append((clean_tweet(line.strip(), remove_emojis=True), 'NONE'))

  output_path = os.path.join(dataset_path, "aws_output")
  output = open(output_path, 'r')
  for line in output.readlines():
    data = json.loads(line)
    if 'Line' in data and data['Line'] is not None:
      tweets[data['Line']] = (tweets[data['Line']][0], data['Sentiment'])

  # Split dataset
  size = len(tweets)
  limit = round(size * 0.8)
  test_limit = round(limit + (size - limit) * 0.75)

  dataset_path = create_folder(os.path.join(dataset_path, "dataset"))
  train_folder = create_folder(os.path.join(dataset_path, "train"))
  val_folder = create_folder(os.path.join(dataset_path, "validation"))
  test_folder = create_folder(os.path.join(dataset_path, "test"))

  write_dataset(os.path.join(train_folder, "data.csv"), tweets[:limit-1])
  write_dataset(os.path.join(val_folder, "data.csv"), tweets[limit:test_limit-1])
  write_dataset(os.path.join(test_folder, "data.csv"), tweets[test_limit:])
