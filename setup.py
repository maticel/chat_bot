from pathlib import Path

# paths setup:
BASE_DIR = Path(__file__).absolute().resolve().parent
DATA_DIR = BASE_DIR.joinpath('data')
DATA_DIRTY_DIR = DATA_DIR.joinpath('dirty')
DATA_CLEAN_DIR = DATA_DIR.joinpath('clean')

# modules/preprocessing.py load_data setup:
LINES = DATA_DIRTY_DIR.joinpath('lines.txt')
CONVERSATIONS = DATA_DIRTY_DIR.joinpath('conversations.txt')
ENC_DEC_IDS = DATA_CLEAN_DIR.joinpath('enc_dec_ids.csv')
ENCODING = 'ISO-8859-1'
SEPARATOR = r' \+{3}\$\+{3} '
PATTERN = r'L[0-9]+'