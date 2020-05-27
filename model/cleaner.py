import re
import emoji

def clean_tweet(text, remove_emojis=False):
  # Remove imgs
  text = re.sub(r'pic.twitter\S+', '', text)
  # Remove links
  text = re.sub(r'http\S+', '', text)
  # Remove locations
  text = re.sub(r'\([^)]*\)', '', text)
  # Remove puntuation
  text = re.sub(r'[\_\-\.\,\;]', ' ', text)
  # Remove breaklines
  text = re.sub(r'\r?\n', '', text)
  # Remove mentions and hashtags
  text = re.sub(r'\@\s?\S+|\#\s?\S+', '', text)
  if remove_emojis:
    # Remove emojis
    text = emoji.get_emoji_regexp().sub('', text)
  # Remove Read more
  text = re.sub(r'(leer más|leer mas|…)', '', text)
  # Remove multiple spaces
  text = re.sub(r'\s\s+', ' ', text)
  # Remove double quotes
  text = re.sub(r'"+', '', text)

  return text.lower().strip()