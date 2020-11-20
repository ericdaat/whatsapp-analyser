import pandas as pd

from src.parser.whatsapp import extract_infos_from_message
from src.parser.nlp import nlp_message


def read_chat(path):
    with open("/Users/eric/Downloads/_chat.txt", "r") as f:
        chat = f.readlines()[2:]

    return chat


def chat_pipeline(chat):
    chat_parsed = list(map(extract_infos_from_message, chat))

    messages_df = pd.DataFrame(
        chat_parsed,
        columns=["timestamp", "author", "message"]
    )
    messages_df = messages_df.dropna()

    messages_df["message_len"] = messages_df["message"].apply(len)
    messages_df["message_nlp"] = messages_df["message"].apply(nlp_message)

    return messages_df
