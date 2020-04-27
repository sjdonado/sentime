import os
import sys
import json
import csv

if __name__ == '__main__':
  date = sys.argv[1]
  if date is None:
    print("Error: date arg is required")
    exit(1)

  labels = []
  tweets = []
  dataset_path = os.path.join(os.getcwd(), 'model', 'data', "{}_dataset.csv".format(date))

  output_path = os.path.join(os.getcwd(), 'model', 'data', "{}_output".format(date))
  output = open(output_path, 'r')
  for line in output.readlines():
    data = json.loads(line)
    labels.append((data['Line'] + 1, data['Sentiment']))

  labels.sort(key=lambda tup: tup[0])

  tweets_path = os.path.join(os.getcwd(), 'model', 'data', "{}_tweets_parsed.txt".format(date))
  tweets_input = open(tweets_path, 'r')
  for line in tweets_input.readlines():
    tweets.append(line.strip())

  with open(dataset_path, 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['tweet', 'sentiment'])
    for idx, tweet in enumerate(tweets):
      csv_out.writerow([tweet, labels[idx][1]])

  print("{} saved successfully".format(dataset_path))
