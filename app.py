from argparse import ArgumentParser

from modules import preprocessing


def main():
    ## Prepare data
    preprocessing.prep_data()
    ## Create Model
    ## Train Model
    ## Test Model


def parse_args():
    parser = ArgumentParser(description='')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main()
