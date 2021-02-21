import re
import pandas as pd

from setup import LINES, CONVERSATIONS, ENCODING, SEPARATOR, HEADER


def prep_data():
    # Load data
    lines, conversations = load_data()
    # Clean lines
    lines = clean_lines(lines)
    # Clean conversations
    conversations = clean_conversations(conversations)
    


def load_data():
    lines = pd.read_csv(LINES, engine='python', encoding=ENCODING, header=HEADER, sep=SEPARATOR)
    conversations = pd.read_csv(CONVERSATIONS, engine='python', encoding=ENCODING, header=HEADER, sep=SEPARATOR)
    return lines, conversations


def clean_lines(lines):
    # Drop useless columns
    lines = lines.drop([1, 2, 3], axis=1)
    # Rename headers
    lines.columns = ['id_line', 'line']
    # Tokenize sentences
    lines.line = lines.line.apply(lambda line: tokenize(line))
    return lines


def tokenize(line):
    # Tokenization could be more specific
    line = str(line).split()
    return line


def clean_conversations(conversations):
    from setup import PATTERN
    # Drop useless columns
    conversations = conversations.drop([0, 1, 2], axis=1)
    # Rename headers
    conversations.columns = ['conversation']
    # Cast string to list of IDs - Can it be done better?
    conversations.conversation = conversations.conversation.apply(lambda x: re.findall(PATTERN, str(x)))
    return conversations
