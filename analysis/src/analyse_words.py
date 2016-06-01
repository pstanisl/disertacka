import argparse
import codecs

# Define script input arguments
parser = argparse.ArgumentParser()

parser.add_argument('-r', '--reference', action='store',
                    help='path to the file with reference word transctiption')
parser.add_argument('-c', '--recognized', action='store',
                    help='path to the file with recognized words')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(output='./output.txt')


def load_mlf(path, *, encoding='utf-8'):
    """Load and clean mlf file.

    Args:
        path: path to the mlf file
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        tuple: filename + list of words
    """
    with codecs.open(path, encoding=encoding) as mlf_file:
        for line in mlf_file.readlines():
            # Remove white space from the beginning and the end.
            line = line.strip()
            # Skip empty line.
            if not line:
                continue
            # Skip comments.
            if line.startswith('#'):
                continue
            yield line


def main(args):
    print('INFO', args)

if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
