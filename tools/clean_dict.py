import argparse
import re

from utils import load_file, save_file

# Define script input arguments
parser = argparse.ArgumentParser(
    description='Clean dictionary with transcription from unwanted items.')
parser.add_argument('input', action='store',
                    help='path to a dictionary with the transcription ')
parser.add_argument(
    'pattern', action='store',
    help='regular expression pattern describing unwanted items')
parser.add_argument('-e', '--encoding', action='store',
                    help='encoding of the files')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(encoding='utf-8')
parser.set_defaults(output='./output.txt')


def clean(data, pattern):
    """Clean data from unwanted items.

    Args:
        data: itertor of a string content
        pattern: string with a regular expression describing unvanted items
    """
    re_clean_pattern = re.compile(pattern, re.IGNORECASE)

    for line in data:
        # Skip line if regular expression find the pattern.
        if (re_clean_pattern.search(line)):
            continue
        # Line does not match with the pattern.
        yield line


def main(args):
    # Load file content.
    content = load_file(args.input, encoding=args.encoding)
    # Clean content.
    cleaned = clean(content, args.pattern)
    # Save cleaned content.
    save_file(args.output, cleaned, encoding=args.encoding)


if __name__ == '__main__':
    from sys import exit
    # Parse run atguments.
    args = parser.parse_args()
    # Run main method
    exit(int(main(args) or 0))
