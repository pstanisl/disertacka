import argparse
import codecs
import re

from collections import Counter
from math import log10

# Define script input arguments
parser = argparse.ArgumentParser(
    description='Create monophone zerogram language model in SRILM format.')

parser.add_argument('-d', '--dictionary', action='store',
                    help='path to dictionary')
parser.add_argument('-e', '--encoding', action='store',
                    help='encoding of the files')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(encoding='utf-8')
parser.set_defaults(output='./tools_lm_output.txt')


def load_dictionary(path, *, encoding='utf-8'):
    re_split = re.compile('\t+')
    with codecs.open(path, encoding=encoding) as dictionary:
        for line in dictionary.readlines():
            # Remove whitechars on the beginning and the end of the line.
            line = line.strip()
            # Skip empty lines.
            if not line:
                continue
            # Spli line word - transcription.
            yield re_split.split(line)


def count(dict_data):
    counter = Counter()

    for item in dict_data:
        counter.update(item[1].split())

    return counter


def save_lm(path, data, *, encoding='utf-8'):
    # +1 is because of </s>
    items = len(data.keys()) + 1
    counter_sum = sum(data.values())
    zerogram_value = log10(1. / items)

    with codecs.open(path, 'w', encoding=encoding) as output:
        # Header
        output.write('\n\\data\\\n')
        output.write('ngram 1={}\n'.format(items))
        # ngram 1
        output.write('\n1-grams:\n')
        output.write('{:6f}\t</s>\n'.format(zerogram_value))
        output.write('{:f}\t<s>\n'.format(-99))

        for item in sorted(data.keys()):
            output.write('{:6f}\t{}\n'.format(zerogram_value, item))

        output.write('\n\\end\\\n')


def main(args):
    dictionary = load_dictionary(args.dictionary, encoding=args.encoding)
    counter = count(dictionary)
    print(sum(counter.values()))
    print(len(counter.keys()))
    save_lm(args.output, counter, encoding=args.encoding)

if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
