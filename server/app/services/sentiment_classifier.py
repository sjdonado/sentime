import os
import re
import string
import emoji
import pathlib

import numpy as np
import spacy
from spacy.compat import pickle
from tensorflow.keras.models import model_from_json
import cytoolz

from .. import app

SPACY_CORE_MODEL = 'es_core_news_md'

def get_labelled_sentences(docs, doc_labels):
    labels = []
    sentences = []
    for doc, y in zip(docs, doc_labels):
        for sent in doc.sents:
            sentences.append(sent)
            labels.append(y)
    return sentences, np.asarray(labels, dtype="int32")

def get_features(docs, max_length):
    docs = list(docs)
    Xs = np.zeros((len(docs), max_length), dtype="int32")
    for i, doc in enumerate(docs):
        j = 0
        for token in doc:
            vector_id = token.vocab.vectors.find(key=token.orth)
            if vector_id >= 0:
                Xs[i, j] = vector_id
            else:
                Xs[i, j] = 0
            j += 1
            if j >= max_length:
                break
    return Xs

class SentimentAnalyser():
    @staticmethod
    def get_embeddings(vocab):
      return vocab.vectors.data

    @classmethod
    def load(cls, path, nlp, max_length=100):
      with (path / "config.json").open() as file_:
          model = model_from_json(file_.read())
      with (path / "model").open("rb") as file_:
          lstm_weights = pickle.load(file_)
      embeddings = cls.get_embeddings(nlp.vocab)
      model.set_weights([embeddings] + lstm_weights)

      return cls(model, max_length=max_length)

    @classmethod
    def predict(cls, model_dir, texts, max_length=100):
      nlp = spacy.load(SPACY_CORE_MODEL)
      nlp.add_pipe(nlp.create_pipe("sentencizer"))
      nlp.add_pipe(cls.load(model_dir, nlp, max_length))
      docs = nlp.pipe(texts, batch_size=1000)

      return [doc.sentiment >= 0.5 for doc in docs]

    def __init__(self, model, max_length=100):
      self._model = model
      self.max_length = max_length

    def __call__(self, doc):
      X = get_features([doc], self.max_length)
      y = self._model.predict(X)
      self.set_sentiment(doc, y)

    def pipe(self, docs, batch_size=1000):
      for minibatch in cytoolz.partition_all(batch_size, docs):
          minibatch = list(minibatch)
          sentences = []
          for doc in minibatch:
              sentences.extend(doc.sents)
          Xs = get_features(sentences, self.max_length)
          ys = self._model.predict(Xs)
          for sent, label in zip(sentences, ys):
              sent.doc.sentiment += label - 0.5
          for doc in minibatch:
              yield doc

    def set_sentiment(self, doc, y):
      doc.sentiment = float(y[0])
      # Sentiment has a native slot for a single float.
      # For arbitrary data storage, there's:
      # doc.user_data['my_data'] = y

def clean_tweet(text, remove_emojis=False):
  # Remove imgs
  text = re.sub(r'pic.twitter\S+', '', text)
  # Remove links
  text = re.sub(r'http\S+', '', text)
  # Remove mentions and hashtags
  text = ' '.join(re.sub('(\s?[@#][\w_-]+)|(@[A-Za-z0-9]+)|(#\s?[A-Za-z0-9]+)', ' ', text).split())
  if remove_emojis:
    # Remove emojis
    text = emoji.get_emoji_regexp().sub('', text)
  # Remove puntuation
  text = re.sub(r'[\_\-\.\,\;]', ' ', text)
  text = re.sub(r'[\#\!\?\:\-\=]', '', text)
  # Remove multiple spaces
  text = re.sub(r'\s\s+', ' ', text.lower())
  # Remove breaklines
  text = ''.join([c for c in text if c != '\n' and c != '\r']).strip()

  return text.lower()

def get_scores(tweets):
  tweets = [clean_tweet(tweet) for tweet in tweets]
  scores = SentimentAnalyser.predict(pathlib.Path(os.path.join(app.static_folder, 'data')), tweets)
  return scores