import multiprocessing as mp
from argparse import ArgumentParser
from modules import preprocessing

from setup import ENC_DEC


def main(prep_data):
    # Prepare data
    if prep_data:
        enc_dec_data = preprocessing.prep_data()
    else:
        enc_dec_data = preprocessing.load_data(ENC_DEC, sep=',', header=0)
    # Create Model
    # Train Model
    # Test Model


def parse_args():
    parser = ArgumentParser(description='Flip a switch by setting a flag')
    parser.add_argument('--prep_data', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    mp.set_start_method('spawn')
    args = parse_args()
    main(prep_data=args.prep_data)
