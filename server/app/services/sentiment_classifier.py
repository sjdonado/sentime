import os
import re
import string

import torch.nn as nn
import numpy as np
import torch
import dill
import spacy
from spacymoji import Emoji

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
  def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, 
                bidirectional, dropout, pad_idx):
    super().__init__()
    self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx = pad_idx)
    self.rnn = nn.LSTM(embedding_dim, 
                        hidden_dim, 
                        num_layers=n_layers, 
                        bidirectional=bidirectional, 
                        dropout=dropout)
    self.fc = nn.Linear(hidden_dim * 2, output_dim)
    self.dropout = nn.Dropout(dropout)
        
  def forward(self, text, text_lengths):
    embedded = self.dropout(self.embedding(text))
    #pack sequence
    packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths)
    packed_output, (hidden, cell) = self.rnn(packed_embedded)
    #unpack sequence
    output, output_lengths = nn.utils.rnn.pad_packed_sequence(packed_output)
    hidden = self.dropout(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim = 1))
            
    return self.fc(hidden)

class SentimentClasssifier():
  model = None
  TEXT = None
  LABEL = None
  nlp = None
  device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

  @classmethod
  def get_model(cls):
    """Get the model object for this instance, loading it if it's not already loaded."""
    if cls.model == None:
      # Loading vocab models
      with open(os.path.join(DATA_PATH, "TEXT.Field"), 'rb') as f:
        cls.TEXT = dill.load(f)
      with open(os.path.join(DATA_PATH, "LABEL.Field"), 'rb') as f:
        cls.LABEL = dill.load(f)

      # Loading model
      cls.model = Net(len(cls.TEXT.vocab), 300, 256, 3, 2, True, 0.5, cls.TEXT.vocab.stoi[cls.TEXT.pad_token])
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
  def tokenizer_tweet(cls, tweet):
    vector = cls.nlp(clean_tweet(tweet))
    vector = [token for token in vector if not token.is_punct]
    vector = [token for token in vector if not token.like_num]
    vector = [token for token in vector if not token._.is_emoji]
    vector = [token.text.lower() for token in vector]

    return vector

  @classmethod
  def predict(cls, tweets, return_dict=False):
    """
    Classify an array of tweets by sentimens NEGATIVE, NEUTRAL and POSITIVE
    Args:
      tweets -- Array of strings
    Return: 
      Array of ints [-1, 0, 1]
    """
    if len(tweets) == 0:
      return []

    tweets_tokenize = [cls.tokenizer_tweet(tweet) for tweet in tweets]
    preprocess_for_model = cls.TEXT.pad(tweets_tokenize)

    preprocess_for_model_tensor = cls.TEXT.numericalize(preprocess_for_model, device=cls.device)

    return cls.batch_prediction(preprocess_for_model_tensor, tweets, return_dict)

  @classmethod
  def predict_sentiment(cls, sentence):
    tokenized = [tok.strip() for tok in cls.tokenizer_tweet(sentence)]
    indexed = [cls.TEXT.vocab.stoi[t] for t in tokenized]
    length = [len(indexed)]
    tensor = torch.LongTensor(indexed).to(cls.device)
    tensor = tensor.unsqueeze(1)
    length_tensor = torch.LongTensor(length)
    with torch.no_grad():
        outputs = cls.model(tensor, length_tensor).squeeze(1)
        _, prediction = torch.max(outputs, 1)
        
    return cls.LABEL.vocab.itos[prediction.item()]

  @classmethod
  def batch_prediction(cls, preprocess_for_model_tensor, input_tweets, return_dict):
    """
    Make batch predictions
    Args:
        model -- lstm model
        preprocess_for_model_tensor -- tuple containing the preprocess_tweets and 
                        the lenghts
        input_tweets -- plain text tweets
    """
    # Sort lengths
    tweets, tweets_lengths = preprocess_for_model_tensor
    idx_sort = tweets_lengths.argsort(descending=True)

    # Make the respective sorts reorded the columns
    tweets_sort = tweets[:, idx_sort]
    
    # Make the respective sorts reorded leghts
    tweets_lengths_sort = tweets_lengths[idx_sort]
    tweets_reorded = np.array(input_tweets)[idx_sort]

    with torch.no_grad():
        outputs = cls.model(tweets_sort, tweets_lengths_sort)

    _, preds = torch.max(outputs, 1)

    predictions = np.array(cls.LABEL.vocab.itos)[preds]

    if return_dict:
      return dict((tweet, pred) for tweet, pred in zip(tweets_reorded, predictions))

    return predictions

def get_health():
  model_health = SentimentClasssifier.get_model() is not None
  nlp_health = SentimentClasssifier.get_nlp() is not None

  return model_health and nlp_health

def get_scores(tweets):
  if get_health():
    scores = SentimentClasssifier.predict(tweets)
    if (len(scores) == 0):
      return {
      'positive': 0,
      'neutral': 0,
      'negative': 0
    }
    
    return {
      'positive': int(np.sum(scores == 'POSITIVE')),
      'neutral': int(np.sum(scores == 'NEUTRAL')),
      'negative': int(np.sum(scores == 'NEGATIVE'))
    }

def get_prediction(text):
  return SentimentClasssifier.predict_sentiment(text)