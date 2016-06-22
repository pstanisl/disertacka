import argparse
import re

from utils import load_file, save_file

# Define script input arguments
parser = argparse.ArgumentParser(
    description='Create duplicate of the item with some changes in' +
    ' transcription based on rules.')
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


def load_rules(path, *, encoding='utf-8'):
    """Load parse file with 'pseudo' tree of rules.

    Args:
        path: string with a path to the file with rules,
        encoding: encoding of the file (default='utf-8')

    Return:
        dict: dictionary with pseudo tree structure, representing
              hierarchy of rules

    NOTE:
        Expected file structure:

        +- rule1_from --> rule1_to
        |  +- sub_rule1_from --> sub_rule1_to
        |  |  +- sub_sub_rule1_from --> sub_sub_rule1_to
        +- rule2_from --> rule2_to
        +- rule3_from --> rule3_to
        |  +- sub_rule3_from --> sub_rule3_to

    """
    # Load rules from a file.
    raw_rules = load_file(path, encoding=encoding)
    # Parse rules into 'pseudo' tree structure.
    return parse_rules(list(raw_rules))


def apply_rules(text, rules):
    # TODO: Create permutation of rules
    for rule_from in sorted(rules.keys()):
        # Get 'to' part of the rule and sub-rules.
        values = rules[rule_from]
        # Get 'to' part.
        rule_to = values[0]
        # Apply rule
        yield re.sub(
            r'(\s*){}(\s)'.format(rule_from), r'\1{}\2'.format(rule_to), text)


def duplicate(content, rules):
    for item in content:
        word, transcription = re.split('\t+', item)
        # Return original unchanged item.
        yield word, transcription

        for new_transcription in apply_rules(transcription, rules):
            yield word, new_transcription


def main(args):
    content_generator = load_file(args.transcript, encoding=args.encoding)
    rules = load_rules(args.rules, encoding=args.encoding)

    duplicated = duplicate(content_generator, rules)


if __name__ == '__main__':
    from sys import exit
    # Parse run atguments.
    args = parser.parse_args()
    # Run main method
    exit(int(main(args) or 0))
