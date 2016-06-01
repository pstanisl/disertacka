import argparse

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


def compare(reference, recognized):
    for rec_key, rec_values in recognized.items():
        if (rec_key not in reference):
            print('[WARNING] - key', rec_key, 'is not in reference mlf.')
            # TODO: Add to the statistics.
            continue
        # Get values from reference.
        ref_values = reference[rec_key]

        print(rec_key)
        print(len(rec_values), '-', rec_values)
        print(len(ref_values), '-', ref_values)
        print('\n')

        lcs_sequence = lcs(ref_values, rec_values)
        lcs_mats = lcs_mat(ref_values, rec_values)

        print(lcs_sequence)
        pprint(lcs_mats)


def main(args):
    reference = load_mlf_to_dict(args.reference, encoding=args.encoding)
    recognized = load_mlf_to_dict(args.recognized, encoding=args.encoding)

    compare(reference, recognized)


if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
