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
  dataset_path = "{}_dataset.csv".format(date)
  
  output = open("{}_output".format(date), 'r')
  for line in output.readlines():
    data = json.loads(line)
    labels.append((data['Line'] + 1, data['Sentiment']))

  labels.sort(key=lambda tup: tup[0])

  tweets_input = open("{}_tweets_parsed.txt".format(date), 'r')
  for line in tweets_input.readlines():
    tweets.append(line.strip())

  with open(dataset_path, 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['tweet', 'sentiment'])
    for idx, tweet in enumerate(tweets):
      csv_out.writerow([tweet, labels[idx][1]])

  print("{} saved successfully".format(dataset_path))
