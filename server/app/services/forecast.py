import os
import re
import string
import pandas as pd
from keras.models import model_from_json

from .. import app

model_path = os.path.join(app.static_folder, 'data', 'model.json')
model_weights_path = os.path.join(app.static_folder, 'data', 'model.h5')

# load json and create model
json_file = open(model_path, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(model_weights_path)

print("Loaded model from disk")

def preprocessing(tweets):
  def clean_text(s):
    s = re.sub(r'pic.twitter\S+', '', s)
    s = re.sub(r'https?:\/\/.*[\r\n]*', '', s)
    s = re.sub(r'@[A-Za-z0-9]+', '', s)
    s = s.lower()
    return "".join([c for c in s if c != string.punctuation and c != '\n' and c != '\r']).strip()

  tweets.apply(clean_text)
  return tweets

def get_score(tweets):
  X = preprocessing(pd.DataFrame(tweets))
  score = loaded_model.predict(X)
  return score