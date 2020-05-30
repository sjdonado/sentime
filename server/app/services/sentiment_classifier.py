import os
import re
import string

import torch.nn as nn
import numpy as np
import torch
import spacy
from spacymoji import Emoji
from fse.models import SIF

from .. import app, logger

SPACY_CORE_MODEL = 'es_core_news_md'
DATA_PATH = os.path.join(app.static_folder, 'data')

def clean_tweet(text):
  # Remove imgs
  text = re.sub(r'pic.twitter\S+', '', text)
  # Remove links
  text = re.sub(r'http\S+', '', text)
  # Remove mentions and hashtags
  text = ' '.join(re.sub('(\s?[@#][\w_-]+)', '', text).split())
  # Remove puntuation
  text = re.sub(r'[\_\-\.\,\;]', ' ', text)
  # text = re.sub(r'[\#\!\?\:\-\=]', '', text)
  # Remove multiple spaces
  text = re.sub(r'\s\s+', ' ', text.lower())
  # Remove breaklines
  text = ''.join([c for c in text if c != '\n' and c != '\r']).strip()
  return text.lower()

class Net(nn.Module):
  """Class neural net with the architecture definition"""
  def __init__(self, input_size, hidden_size, output_size, n_layers, 
               bidirectional, dropout):
    super(Net, self).__init__()
    self.lstm = nn.LSTM(
      input_size, hidden_size, 
      num_layers=n_layers,
      bidirectional=bidirectional,
      dropout=dropout
    )

    self.head_layers = nn.Sequential(
      nn.Dropout(dropout),
      nn.Linear(2*hidden_size, hidden_size),
      nn.Dropout(dropout),
      nn.ReLU(),
      nn.Linear(hidden_size, output_size),
      nn.Dropout(dropout)
    )

  def forward(self, x):
    lstm_out, _ = self.lstm(x.view(len(x), 1, -1))
    x = self.head_layers(lstm_out.view(len(x), -1))
    return x

class SentimentClasssifier():
  model = None
  fse_model = None
  nlp = None
  device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

  @classmethod
  def get_model(cls):
    """Get the model object for this instance, loading it if it's not already loaded."""
    if cls.model == None:
      # Loading embedding model
      cls.fse_model = SIF.load(os.path.join(DATA_PATH, "embedding_model.pt"))
      # Loading model
      cls.model = Net(300, 100, 3, 3, True, 0.5).cpu()
      cls.model.load_state_dict(torch.load(os.path.join(DATA_PATH, "model.pt"), map_location=cls.device))
      cls.model.eval().to(cls.device)
    return cls.model

  @classmethod
  def get_nlp(cls):
    """Get the nlp object for this instance, loading it if it's not already loaded."""
    if cls.nlp == None:
      cls.nlp = spacy.load(SPACY_CORE_MODEL)
      cls.nlp.add_pipe(Emoji(cls.nlp, merge_spans=False), first=True)
    return cls.nlp
    
  @classmethod
  def preprocess(cls, tweet):
    vector = cls.nlp(clean_tweet(tweet))
    vector = [token for token in vector if not token.is_punct]
    vector = [token for token in vector if not token.like_num]
    vector = [token for token in vector if not token._.is_emoji]
    vector = [token.text.lower() for token in vector]
    vector = cls.fse_model.infer([(vector, 0)])

    return vector

  @classmethod
  def predict(cls, tweets):
    """
    Classify an array of tweets by sentimens NEGATIVE, NEUTRAL and POSITIVE
    Args:
      tweets -- Array of strings
    Return: 
      Array of ints [-1, 0, 1]
    """
    if len(tweets) == 0:
      return []

    tweets = [cls.preprocess(tweet) for tweet in tweets]
    outputs = cls.model(torch.Tensor(tweets).cpu().float())
    _, preds = torch.max(outputs, 1)

    with torch.no_grad():
      return preds.cpu().numpy() - 1

def get_scores(tweets):
  if SentimentClasssifier.get_model() is not None and SentimentClasssifier.get_nlp() is not None:
    scores = SentimentClasssifier.predict(tweets)
    print(scores, flush=True)
    positive = 0
    negative = 0
    neutral = 0
    if (len(scores) > 0):
      positive = np.sum(scores == 1)
      neutral = np.sum(scores == 0)
      negative = np.sum(scores == -1)
    
    return {
      'positive': int(positive),
      'neutral': int(neutral),
      'negative': int(negative)
    }

def get_health():
  model_health = SentimentClasssifier.get_model() is not None
  nlp_health = SentimentClasssifier.get_nlp() is not None

  return model_health and nlp_health