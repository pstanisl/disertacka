import argparse
import re
import sys
from os import system
from os.path import abspath, dirname, join
from subprocess import call
# Get SRC directory path of TOOLS modul.
TOOLS_SRC_DIR = abspath(join(dirname(__file__), '../../tools', 'src'))
# Add src dir into PATHs.
sys.path.append(TOOLS_SRC_DIR)
from utils import load_file

parser = argparse.ArgumentParser()
parser.add_argument(
    'list', help='path to the file with pairs of files to concatenate')
parser.add_argument('-d', '--htkdir', action='store',
                    help='path to the directory with htk files')
parser.add_argument('-o', '--output', action='store',
                    help='path to the output directory')
# parser.add_argument()
parser.set_defaults(htkdir='./')
parser.set_defaults(output='./')


def get_pairs(path, *, encoding='utf-8'):
    lines = load_file(args.list, encoding=encoding)
    for line in lines:
        sent1, sent2 = line.split(';')
        yield (sent1, sent2)


def concatenate(pairs, htkdir, output):
    re_number = re.compile('(\d+)')
    for sent1, sent2 in pairs:
        # Get path to the file in the HTK dir
        sent1_path = join(htkdir, sent1 + '.htk')
        sent2_path = join(htkdir, sent2 + '.htk')
        # Get number of file, expecting format aaaaaXXXXXX
        sent1_number = re_number.search(sent1).group(1)
        sent2_number = re_number.search(sent2).group(1)
        # Create path to output file
        sent_concat_path = join(
            output, 'sent{}_{}.htk'.format(sent1_number, sent2_number))
        # Run HCopy to concatenate the files
        system('HCopy {} + {} {}'.format(
            sent1_path, sent2_path, sent_concat_path))


def main(args):
    pairs = get_pairs(args.list)
    concatenate(pairs, args.htkdir, args.output)


if __name__ == '__main__':
    args = parser.parse_args()

    main(args)
