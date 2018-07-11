import argparse

from mapping import load_rules, map_text
from utils import load_file, parse_rules, save_file

# Define script input arguments
parser = argparse.ArgumentParser(
    description='Make phoneme mapping in result file from HTK.')
parser.add_argument('transcript', action='store',
                    help='path to a dictionary with the transcription')
parser.add_argument('rules', action='store',
                    help='path to file with mapping rules')
parser.add_argument('-e', '--encoding', action='store',
                    help='encoding of the files')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(encoding='utf-8')
parser.set_defaults(output='./output.txt')


def do_mapping(content, rules):
    """Apply rules on all items in the iterator.

    Args:
        content: iterator with loaded data,
        rules: dictionary ('pseudo' tree) with rules.

    Yield:
        A) in case of mlf with results
            tuple: (0) and (1) - not changed items from loaded data, (2) transformed part, (3) confidence
        B) in case of transcript
            tuple: (0) transformed part
    """
    for item in content:
        if item.startswith('#') or item.startswith('"') or item.startswith('.'):
            yield (item, )
            continue

        splitted = item.split()

        if len(splitted) == 4:
            # Data from mlf with result.
            t1, t2, result, confidence = item.split()

            yield t1, t2, map_text(result, rules), confidence
        else:
            # Data from mlf with transcript.
            yield (map_text(item, rules), )


def format_data(data):
    for item in data:
        yield ' '.join(item)


def main(args):
    content_generator = load_file(args.transcript, encoding=args.encoding)
    rules = load_rules(args.rules, encoding=args.encoding)

    mapped = list(do_mapping(content_generator, rules))
    formatted = format_data(mapped)

    save_file(args.output, formatted, encoding=args.encoding)


if __name__ == '__main__':
    from sys import exit
    # Parse run atguments.
    args = parser.parse_args()
    # Run main method
    exit(int(main(args) or 0))
