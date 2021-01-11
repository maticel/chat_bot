import re
import pandas as pd

from setup import LINES, CONVERSATIONS, ENCODING, SEPARATOR, PATTERN, HEADER


def prep_data():
    # Load data
    lines, conversations = load_data()
    # Clean lines

    # Clean conversations
    conversations.iloc[:, 3] = conversations.iloc[:, 3].apply(lambda x: re.findall(PATTERN, str(x)))


def load_data():
    lines = pd.read_csv(LINES, engine='python', encoding=ENCODING, header=HEADER, sep=SEPARATOR)
    conversations = pd.read_csv(CONVERSATIONS, engine='python', encoding=ENCODING, header=HEADER, sep=SEPARATOR)
    return lines, conversations
