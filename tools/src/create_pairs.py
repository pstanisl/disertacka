#!/usr/bin/env python3
"""
Generate file with pairs of words and filename for every variant (2).
It takes file with already defined pairs and corresponding filename, it
find same pairs (diferent order of words, but content is based on same
audio files) and saves it as one line in output file.

w1;w2;f1 + w2;w1;f2 -> w1;w2;f1;f2
"""
import argparse

from utils import load_file, save_file

parser = argparse.ArgumentParser()
parser.add_argument(
    'list', help='path to the file with word pairs and corresponding file')
parser.add_argument(
    '-o', '--output', action='store', help='path to the output file')
parser.set_defaults(output='./output.csv')


def load_pairs(path, encoding='utf-8'):
    for line in load_file(path, encoding=encoding):
        w1, w2, f1, _ = line.split(';')
        yield w1, w2, f1


def get_pairs(pairs):
    while len(pairs) > 0:
        # Get pair from the top of the list, it contains word pair and on filename
        w1, w2, f1 = pairs.pop(0)
        # Find complementary item to the current pair
        complement = next(filter(lambda x: x[0] == w2 and x[1] == w1, pairs))
        # Get index of complementary item in the list
        complement_idx = pairs.index(complement)
        # Return as a line (string) for CSV
        yield ';'.join([w1, w2, f1, complement[-1]])
        # Remove complementary item from the list of pairs.
        pairs.pop(complement_idx)


def main(args):
    encoding = 'utf-8'
    # Load content of the file with all pairs.
    loaded_pairs = list(load_pairs(args.list, encoding=encoding))
    # Reduce pairs -> concatenate pair + complement
    new_pairs_gen = get_pairs(loaded_pairs)
    # Save into output file
    save_file(args.output, new_pairs_gen, encoding=encoding)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
