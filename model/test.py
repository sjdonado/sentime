import re
import emoji
from googletrans import Translator

translator = Translator()
text = 'cuando será que vuelvo a las europas y me repito estas fiestas? 🥺🤣 charlotte de witte 👽,NEUTRAL'

def clean_text(s):
  s = re.sub(r'pic.twitter\S+', '', s)
  # Remove links
  s = re.sub(r'(\w+:\/\/\S+)', '', s)
  # Remove mentions and hashtags
  s = re.sub(r'(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)', '', s)
  # Parse emojis to text
  s = emoji.demojize(s).replace('_', ' ')
  # Translate to spanish
  translation = translator.translate(s, src='en', dest='es')
  # Remove puntuation
  s = translation.text.lower()
  s = re.sub(r'[\.\,\!\?\:\;\-\=]', '', s)
  return s

print(clean_text(text))