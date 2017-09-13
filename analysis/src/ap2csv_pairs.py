#!/usr/bin/env python3
"""Convert output of AP recognizer into csv.
This is a special variant for processing pairs
result of the human vs machine experiment.

If --isolated is used only ACC value is used.
"""
import argparse
from itertools import chain, product

from utils import load_mlf, save_file

parser = argparse.ArgumentParser()
parser.add_argument('mlf', help='file path to the AP decoder output')
# Output filepath
parser.add_argument('-o', '--output', action='store',
                    help='path to the output csv')
# Default values
parser.set_defaults(output='./output.csv')


def process(mlf_content):
    for filename, content in mlf_content:
        d_results = dict(map(lambda item: item.split(), content))
        # Parse the keys in format 'word1_word2' and get set of the words
        keys = set(
            # Flatten the array
            chain.from_iterable(
                # Parse the keys
                map(lambda key: key.split('_'), d_results.keys())))
        # Get all variants of words (possibly decoded in the test)
        keys_product = sorted(
            map(lambda pair: '_'.join(pair), product(keys, keys)))
        # Initialize list with decoded accuracy
        res_acc = [0.0] * len(keys_product)
        # Fill in list with real accuracy, if the value is missing use 0.0
        for index in range(len(keys_product)):
            key = keys_product[index]
            # Get the value from the results
            try:
                res_acc[index] = d_results[key]
            except:
                # The word combination is not in the results
                continue

        try:
            yield '{};;;;{r[0]};{r[1]};{r[2]};{r[3]};'.format(
                filename, r=res_acc)
        except IndexError:
            # In the results only combination of word1: 'word1_word1'
            print(f'WARNING: unable to get proper result format for file: {filename}')
            yield '{};;;;{r[0]};-1;-1;-1;'.format(filename, r=res_acc)


def main(args):
    encoding = 'utf-8'
    # Load output of AP recognizer
    mlf_content = load_mlf(args.mlf, clean=False, encoding=encoding)
    # csv_content = list(load_csv(args.csv, encoding=encoding))
    # Process data and create content for output csv
    p_content = process(mlf_content)
    # Save files
    save_file(args.output, p_content, encoding=encoding)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
