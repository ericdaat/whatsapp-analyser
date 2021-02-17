import re
import json

from nltk.corpus import stopwords


with open("data/stopwords_fr.json") as f:
    stopwords_fr = json.loads(f.read())

def nlp_message(message_text):
    message_text = message_text.lower()

    # split punctuation
    message_text = re.sub(string=message_text,
                          pattern=r"([$&+,:;=?@#|\"<>.^*()%!-])",
                          repl=r" \1 ")

    message_text_split = message_text.split(" ")

    message_text_split = [word for word in message_text_split
                               if word not in stopwords_fr and word.isalnum() and not word.isnumeric()]

    output = " ".join(message_text_split)

    return output
