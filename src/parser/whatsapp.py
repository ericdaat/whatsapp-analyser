import re

import numpy as np
import pandas as pd


def extract_infos_from_message(message):
    regex = re.compile(r"\[(.+)\]\s([A-Za-z\s]+)\:\s(.+)$")

    try:
        message_date, message_author, message_text = regex.findall(message)[0]
    except IndexError:
        message_date = np.nan
        message_author = np.nan
        message_text = np.nan

    return message_date, message_author, message_text
