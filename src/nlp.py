import re
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


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


def topic_modeling(chat_df):
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                   stop_words=stopwords_fr)

    corpus = chat_df.loc[chat_df["message_len"] > 30]["message_nlp"]

    X = vectorizer.fit_transform(corpus)

    topic_model = NMF(
        n_components=10,
        beta_loss="kullback-leibler",
        solver="mu",
        max_iter=1000,
        alpha=.1,
        l1_ratio=.5
    )

    topic_model.fit(X)

    return topic_model, vectorizer

