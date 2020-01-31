#!/usr/bin/env python3
"""Convert output of AP recognizer into csv.

If --isolated is used only ACC value is used.
"""
import argparse
from functools import partial

from utils import load_file, load_mlf, save_file

parser = argparse.ArgumentParser()
parser.add_argument('mlf', help='file path to the AP decoder output')
parser.add_argument('csv', help='csv file with filenames and content')
# Isolated flag
parser.add_argument('-i', '--isolated', action='store_true',
                    help='AP decoder was in isolated regime')
# Output filepath
parser.add_argument('-o', '--output', action='store',
                    help='path to the output csv')
# Default values
parser.set_defaults(output='./output.csv')


def get_acc(index, item):
    item = item.split()
    return item[index]


def get_word(words, line_from_mlf):
    # print(words, line_from_mlf)
    word, _ = line_from_mlf.split()
    return word in words


def load_csv(path, encoding='utf-8'):
    for item in load_file(path, encoding=encoding):
        splitted = item.split(';')
        # Change to SINGLE word file format
        splitted[2] = splitted[2][:-3]
        splitted[3] = splitted[3][:-3]

        yield splitted


def process(mlf_content, csv_content, isolated=False):
    for filename, content in mlf_content:
        try:
            res_recipe = next(filter(lambda x: filename in x, csv_content))
        except:
            yield '{};;;;;;;'.format(filename)
            continue

        word_index = res_recipe.index(filename) - 1

        best_acc = float(max(map(partial(get_acc, -1), content)))

        res_content = sorted(filter(
            partial(get_word, res_recipe[:2]), content))

        if (isolated):
            res_word = list(map(partial(get_acc, 0), res_content))
            res_acc = list(map(
                lambda x: float(x), map(partial(get_acc, -1), res_content)))
            # print(res_word)
            # print(res_acc)
            if len(res_acc) == 0:
                res_acc = [0.] * 2
            elif len(res_acc) < 2:
                # Add missing probability value
                index = res_recipe.index(res_word[0])
                res_acc = [0.] + res_acc if index == 1 else res_acc + [0.]
            # Get best accuracy of filtered words (important words)
            best_word_acc = float(max(res_acc))
            # Append propability for OTHER results. Propability is appended
            # only if the best_acc is greater than 0.5 (other is less than 0.5)
            # and best_acc is also best_word_ass which is one of the
            # incriminated word in the test.
            if (best_acc < 0.5 and best_acc == best_word_acc):
                res_acc.append(0)
            else:
                res_acc.append(1 - sum(res_acc))
            # res_acc.append(1 - sum(res_acc))
            # Convert to string
            res_acc = '{d[0]:.8f};{d[1]:.8f};{d[2]:.8f}'.format(d=res_acc)

        yield '{};;{};;;{}'.format(filename, res_acc, word_index)


def main(args):
    encoding = 'utf-8'
    # Load output of AP recognizer
    mlf_content = load_mlf(args.mlf, clean=False, encoding=encoding)
    csv_content = list(load_csv(args.csv, encoding=encoding))
    # Process data and create content for output csv
    p_content = process(mlf_content, csv_content, isolated=args.isolated)
    # Save files
    save_file(args.output, p_content, encoding=encoding)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
