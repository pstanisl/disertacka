import argparse
import codecs

from collections import Counter
from os.path import splitext
from pprint import pprint

from lcs import lcs, lcs_mat
from utils import load_mlf_to_dict

# Define script input arguments
parser = argparse.ArgumentParser()

parser.add_argument('-e', '--encoding', action='store',
                    help='encoding of the files')
parser.add_argument('-r', '--reference', action='store',
                    help='path to the file with reference word transctiption')
parser.add_argument('-c', '--recognized', action='store',
                    help='path to the file with recognized words')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(encoding='utf-8')
parser.set_defaults(output='./output.txt')


def save_diffs(path, compare_iterable, *, encoding='utf-8'):
    c_diff_seq1 = Counter()
    c_diff_seq2 = Counter()

    with codecs.open(path, 'w', encoding=encoding) as output:
        for key, seq1, seq2, diffs in compare_iterable:
            output.write('"{}"\n'.format(key))

            output.write('# s1: "{}"\n'.format(' '.join(seq1)))
            output.write('# s2: "{}"\n'.format(' '.join(seq2)))

            for diff_seq1, diff_seq2 in diffs:
                # Update counters with errors.
                c_diff_seq1.update(diff_seq1)
                c_diff_seq2.update(diff_seq2)
                # Create 'readable' texts.
                diff_seq1 = ' '.join(diff_seq1)
                diff_seq2 = ' '.join(diff_seq2)
                # Save into the file.
                output.write('- "{}" - "{}"\n'.format(diff_seq1, diff_seq2))

            output.write('.\n'.format(key))
    # Save counters.
    filename, ext = splitext(path)

    with codecs.open('{}.ref_counter{}'.format(filename, ext),
                     'w', encoding=encoding) as c_output:
        for k, v in c_diff_seq1.most_common():
            c_output.write('{} {}\n'.format(k, v))

    with codecs.open('{}.rec_counter{}'.format(filename, ext),
                     'w', encoding=encoding) as c_output:
        for k, v in c_diff_seq2.most_common():
            c_output.write('{} {}\n'.format(k, v))


def get_diffs(matrix, seq1, seq2):
    """ Get all diferences between sequences. Insertion and deletation
    are grouped.

    Args:
        matrix: list of lists representing LCS between seq1 and seq2.
        seq1: iterable representing first sequence (rows in the matrix).
        seq2: iterable representing second sequence (columns in the matrix).

    Yields:
        tuple: with diferences between seq1 and seq2.

    NOTE:
        Algorithm yields diffs in different order (first are the
        last diferences).
    """
    rows = len(seq1)
    cols = len(seq2)
    # Initialize list with diferences.
    diff_seq1 = []
    diff_seq2 = []

    while (rows > 0 and cols > 0):
        # Get submatrix around current element.
        elem_left, elem_curr = matrix[rows][cols-1: cols+1]
        elem_diag, elem_top = matrix[rows - 1][cols-1: cols+1]
        # Diff elements in the matrix on the same position.
        if (elem_curr == elem_diag):
            diff_seq1.insert(0, seq1[rows - 1])
            diff_seq2.insert(0, seq2[cols - 1])
            # Move diagonally in the matrix.
            cols -= 1
            rows -= 1
            # Continue in processing.
            continue
        # Diff elements - missing element in seq1.
        if (elem_left > elem_diag):
            diff_seq2.insert(0, seq2[cols - 1])
            cols -= 1
            continue
        # Diff elements - missing element in seq2.
        if (elem_top > elem_diag):
            diff_seq1.insert(0, seq1[rows - 1])
            rows -= 1
            continue
        # -- Same elements in sequences -- #
        # Yield current differences in sequences.
        if (len(diff_seq1 + diff_seq2)):
            yield diff_seq1, diff_seq2
        # Reset list with diferences.
        diff_seq1 = []
        diff_seq2 = []
        # Move diagonally in the matrix.
        cols -= 1
        rows -= 1
    # Yield last differences.
    if (len(diff_seq1 + diff_seq2)):
        yield diff_seq1, diff_seq2


def compare(reference, recognized):
    # Sort by keys -> better for later.
    for rec_key in sorted(recognized.keys()):
        # Get recognized data.
        rec_values = recognized[rec_key]
        # Check key in reference -> only precaution.
        if (rec_key not in reference):
            print('[WARNING] - key', rec_key, 'is not in reference mlf.')
            # TODO: Add to the statistics.
            continue
        # Get values from reference.
        ref_values = reference[rec_key]

        matrix = lcs_mat(ref_values, rec_values)

        # Diffs - iterator
        diffs = list(get_diffs(matrix, ref_values, rec_values))

        if (not diffs):
            continue

        yield (
            # Source file key
            rec_key,
            # First sequence (reference)
            ref_values,
            # Second sequence (recognized)
            rec_values,
            # reversed(diffs)
            diffs[::-1]
        )


def main(args):
    reference = load_mlf_to_dict(args.reference, encoding=args.encoding)
    recognized = load_mlf_to_dict(args.recognized, encoding=args.encoding)

    compare_iterable = compare(reference, recognized)

    save_diffs(args.output, compare_iterable, encoding=args.encoding)

if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
