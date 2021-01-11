from pathlib import Path

BASE_DIR = Path(__file__).absolute().resolve().parent

DATA_DIR = BASE_DIR.joinpath('data')
LINES = DATA_DIR.joinpath('lines.txt')
CONVERSATIONS = DATA_DIR.joinpath('conversations.txt')

ENCODING = 'ISO-8859-1'
HEADER = None
SEPARATOR = r' \+{3}\$\+{3} '
PATTERN = r'L[0-9]+'