from argparse import ArgumentParser

from modules import preprocessing


def main(prep_data):
    ## Prepare data
    if prep_data:
        preprocessing.prep_data()
    ## Create Model
    ## Train Model
    ## Test Model


def parse_args():
    parser = ArgumentParser(description='Flip a switch by setting a flag')
    parser.add_argument('--prep_data', action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(prep_data=args.prep_data)
