import argparse
import codecs

from collections import Set
from numpy import int, zeros

from utils import load_file

# Define script input arguments
parser = argparse.ArgumentParser(
    description='Convert output of pyeval.py into confusion matrix.')
parser.add_argument('input', action='store',
                    help='path to an output file of pyeval')
parser.add_argument('-e', '--encoding', action='store',
                    help='encoding of the files')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(encoding='utf-8')
parser.set_defaults(output='./output.txt')


def load_pyeval(path, *, encoding='utf-8'):
    for line in load_file(path, encoding=encoding):
        splitted = line.split()

        yield splitted[:-1] + [int(splitted[-1])]


def create_confusion_matrix(data):
    # Get all 'legend' items for matrix.
    content_legend = sorted(list(set([item[0] for item in data])))
    count = len(content_legend)
    # Initialize matrix with zeros.
    matrix = zeros((count, count), dtype=int)
    # Yield first row (legend of the matrix).
    yield content_legend
    # Fill in matrix.
    for row_item, col_item, count in data:
        # Get index of a corresponding row.
        row_index = content_legend.index(row_item)
        # Get index of a corresponding column.
        col_index = content_legend.index(col_item)
        # Set item in the matrix.
        matrix[row_index, col_index] = count
    # Yield content of the matrix
    for row in matrix.tolist():
        yield row


def save_confusion_matrix(path, data, *, encoding='utf-8'):
    legend = []
    with codecs.open(path, 'wb', encoding=encoding) as output:
        for index, row in enumerate(data):
            if not index:
                legend = [''] + row

            row_str = ';'.join([str(i) for i in row])

            output.write('{};{}\n'.format(legend[index], row_str))


def main(args):
    data = list(load_pyeval(args.input, encoding=args.encoding))
    matrix = create_confusion_matrix(data)

    save_confusion_matrix(args.output, matrix, encoding=args.encoding)

if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
