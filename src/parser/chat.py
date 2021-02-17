from datetime import datetime

import pandas as pd

from src.parser.whatsapp import extract_infos_from_message
from src.parser.nlp import nlp_message


def read_chat(path):
    with open(path, "r") as f:
        chat = f.readlines()[2:]

    return chat


def chat_pipeline(chat):
    chat_parsed = list(map(extract_infos_from_message, chat))

    messages_df = pd.DataFrame(
        chat_parsed,
        columns=["timestamp", "author", "message"]
    )
    messages_df.dropna(subset=["timestamp"], inplace=True)
    messages_df["timestamp"] = messages_df["timestamp"]\
        .apply(lambda r: datetime.strptime(r, "%d/%m/%Y %H:%M:%S"))

    messages_df["timestamp"] = messages_df["timestamp"].apply(pd.Timestamp)
    messages_df["message_len"] = messages_df["message"].apply(len)
    messages_df["message_nlp"] = messages_df["message"].apply(nlp_message)
    messages_df = messages_df.set_index("timestamp")

    return messages_df
