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
batch_size = 128
DATA_PATH = pathlib.Path(os.path.join(app.static_folder, 'data'))

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

class SentimentAnalyser():
    @staticmethod
    def get_embeddings(vocab):
      return vocab.vectors.data

    @classmethod
    def load(cls, nlp, model, lstm_weights, max_length=140):
      embeddings = cls.get_embeddings(nlp.vocab)
      model.set_weights([embeddings] + lstm_weights)
      return cls(model, max_length=max_length)

    @classmethod
    def predict(cls, nlp, texts):
      docs = nlp.pipe(texts, batch_size=batch_size)
      return [doc.sentiment for doc in docs]

    def __init__(self, model, max_length=100):
      self._model = model
      self.max_length = max_length

    def __call__(self, doc):
      X = get_features([doc], self.max_length)
      y = self._model.predict(X)
      self.set_sentiment(doc, y)

    def pipe(self, docs, batch_size=batch_size):
      for minibatch in cytoolz.partition_all(batch_size, docs):
        minibatch = list(minibatch)
        sentences = []
        for doc in minibatch:
          sentences.extend(doc.sents)
        Xs = get_features(sentences, self.max_length)
        ys = self._model.predict(Xs)
        for sent, label in zip(sentences, ys):
          sent.doc.sentiment += np.argmax(label) - 1
        for doc in minibatch:
          yield doc

    def set_sentiment(self, doc, y):
      doc.sentiment = y

def init_nlp():
  print('Loading nlp...', flush=True)
  with (DATA_PATH / "config.json").open() as file_:
    model = model_from_json(file_.read())

  with (DATA_PATH / "model").open("rb") as file_:
    lstm_weights = pickle.load(file_)

  nlp = spacy.load(SPACY_CORE_MODEL)
  nlp.add_pipe(nlp.create_pipe("sentencizer"))
  nlp.add_pipe(SentimentAnalyser.load(nlp, model, lstm_weights))

  print('nlp loaded!', flush=True)
  return nlp

def get_scores(nlp, tweets):
  tweets = [clean_tweet(tweet) for tweet in tweets]
  scores = SentimentAnalyser.predict(nlp, tweets)

  positive = 0
  negative = 0
  for score in scores:
    if score == 1:
      positive += 1
    if score == -1:
      positive += 1
  
  return {
    'positive': positive,
    'negative': negative,
    'neutral': len(scores) - (positive + negative)
  }