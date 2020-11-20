import re

from nltk.corpus import stopwords


stopwords_fr = stopwords.words("french")

def nlp_message(message_text):
    message_text = message_text.lower()
    message_text = re.sub(string=message_text,
                          pattern=r"([$&+,:;=?@#|\"<>.^*()%!-])",
                          repl=r" \1 ")

    message_text_split = message_text.split(" ")

    message_text_split = [word for word in message_text_split
                               if not word in stopwords_fr]

    output = " ".join(message_text_split).strip()

    return output
