import re
import multiprocessing as mp
import pandas as pd
import time

from setup import LINES, CONVERSATIONS, ENCODING, SEPARATOR, ENC_DEC_IDS, ENC_DEC


# TODO: Whole process of data preprocessing could be optimized

def prep_data():
    # Load data
    lines = load_data(LINES)
    conversations = load_data(CONVERSATIONS)
    # Clean data
    print('[{}]Cleaning data...'.format(time.strftime('%H:%M:%S')))
    lines = clean_lines(lines)
    conversations = clean_conversations(conversations)
    # Encode|Decode data
    print('[{}]Generating encode|decode data frame...'.format(time.strftime('%H:%M:%S')))
    enc_dec_data_ids = multi_process(conversations, generate_enc_dec_data_ids, ())
    save_data(enc_dec_data_ids, ENC_DEC_IDS)
    # Translate ids
    print('[{}]Translating ids of encode|decode data frame to corresponding lines...'.format(time.strftime('%H:%M:%S')))
    enc_dec_data = multi_process(enc_dec_data_ids, translate_ids, (lines,))
    save_data(enc_dec_data, ENC_DEC)
    return enc_dec_data


def load_data(path, sep=SEPARATOR, header=None):
    print('[{}]Loading file:{}'.format(time.strftime('%H:%M:%S'), path))
    data = pd.read_csv(path, engine='python', encoding=ENCODING, header=header, sep=sep)
    return data


def save_data(df, path):
    print('[{}]Saving to:{}'.format(time.strftime('%H:%M:%S'), path))
    df.to_csv(path, encoding=ENCODING, sep=',', header=True, index=None)


def clean_lines(lines):
    # Drop useless columns
    lines = lines.drop([1, 2, 3], axis=1)
    # Rename headers
    lines.columns = ['id_line', 'line']
    # Tokenize sentences
    lines.line = lines.line.apply(lambda line: tokenize(line))
    return lines


def tokenize(line):
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


def multi_process(df, target, args_tuple):
    slice_size = int(df.shape[0] / mp.cpu_count())

    manager = mp.Manager()
    return_list = manager.list()

    processes = []
    for i in range(mp.cpu_count()):
        x = i * slice_size
        y = (i + 1) * slice_size
        slice_df = df.iloc[x:y, :]
        args = (slice_df,) + args_tuple + (return_list,)
        process = mp.Process(target=target, args=args)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return_df = pd.concat(return_list, ignore_index=True)
    return return_df


def generate_enc_dec_data_ids(conversations, return_list):
    # Generates data frame of encode|decode lines ids
    enc_dec_data_ids = pd.DataFrame(columns=['enc', 'dec'])
    for conversation in conversations.conversation:
        for i in range(len(conversation) - 1):
            enc = conversation[i]
            dec = conversation[i + 1]
            new_row = {'enc': enc, 'dec': dec}
            enc_dec_data_ids = enc_dec_data_ids.append(new_row, ignore_index=True)
    return_list.append(enc_dec_data_ids)


def translate_ids(enc_dec_data_ids, lines, return_list):
    # Translates encode|decode ids of lines to tokenized lines
    enc_dec_data_ids.enc = enc_dec_data_ids.enc.apply(lambda x: lines.loc[lines['id_line'] == x].iloc[0, 1])
    enc_dec_data_ids.dec = enc_dec_data_ids.dec.apply(lambda x: lines.loc[lines['id_line'] == x].iloc[0, 1])
    return_list.append(enc_dec_data_ids)
