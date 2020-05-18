import re
import emoji

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