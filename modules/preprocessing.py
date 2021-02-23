import re
import pandas as pd

from setup import LINES, CONVERSATIONS, ENCODING, SEPARATOR, ENC_DEC_IDS


def prep_data():
    # Load data
    lines = load_data(LINES)
    conversations = load_data(CONVERSATIONS)
    # Clean lines
    lines = clean_lines(lines)
    # Clean conversations
    conversations = clean_conversations(conversations)
    # Encode/Decode data
    print('Creating encodes and decodes ...')
    enc_dec_data = generate_enc_dec_data(lines, conversations)
    print('Saving created data set to {} ...'.format(ENC_DEC_IDS))
    enc_dec_data.to_csv(ENC_DEC_IDS)
    print('Translating {} ...'.format(ENC_DEC_IDS))


def load_data(file, header=None):
    data = pd.read_csv(file, engine='python', encoding=ENCODING, header=header, sep=SEPARATOR)
    return data


def clean_lines(lines):
    # Drop useless columns
    lines = lines.drop([1, 2, 3], axis=1)
    # Rename headers
    lines.columns = ['id_line', 'line']
    # Tokenize sentences
    lines.line = lines.line.apply(lambda line: tokenize(line))
    return lines


def tokenize(line):
    # TODO: Tokenization could be more specific
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


def generate_enc_dec_data(lines, conversations):
    # Generates data frame of encode|decode lines ids
    # TODO: add multiprocessing
    data = pd.DataFrame(columns=['enc', 'dec'])
    for conversation in conversations.conversation:
        for i in range(len(conversation) - 1):
            enc = conversation[i]
            dec = conversation[i + 1]
            new_row = {'enc': enc, 'dec': dec}
            data = data.append(new_row, ignore_index=True)
    return data


def translate_ids(enc_dec_data):
    # Translates ids to tokenized lines
    pass
