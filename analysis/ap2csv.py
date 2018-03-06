#!/usr/bin/env python3
"""Convert output of AP recognizer into csv.

If --isolated is used only ACC value is used.
"""
import argparse

from utils import load_mlf, save_file

parser = argparse.ArgumentParser()
parser.add_argument('mlf', help='file path to the AP decoder output')
# Isolated flag
parser.add_argument('-i', '--isolated', action='store_true',
                    help='AP decoder was in isolated regime')
# Output filepath
parser.add_argument('-o', '--output', action='store',
                    help='path to the output csv')
# Default values
parser.set_defaults(output='./output.csv')


def get_acc(item):
    item = item.split()
    return item[-1]


def process_data(data, isolated=False):
    # from pprint import pprint
    for filename, content in data:
        # Sort by alphabet
        content.sort()
        # Get only ACC value if the items were isolated
        if (isolated):
            content = list(map(get_acc, content))
        yield filename, content


def content2csv(data):
    for filename, conent in data:
        line = '{};;;'.format(filename)
        line += ';'.join(conent)
        yield line


def main(args):
    encoding = 'utf-8'
    # Load output of AP recognizer
    mlf_content = load_mlf(args.mlf, clean=False, encoding=encoding)
    # Get important data from loaded content
    processed = process_data(mlf_content, args.isolated)
    # Convert data into csv content
    csv_data = content2csv(processed)
    # Save files
    save_file(args.output, csv_data, encoding=encoding)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
