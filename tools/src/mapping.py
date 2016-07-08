import argparse
import re

from utils import load_file, mlf_format_data, parse_rules, save_file

# Define script input arguments
parser = argparse.ArgumentParser(
    description='Make phoneme mapping in phoneme transcription.')
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


# -- Rules loading and parsing -- #


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


# -- Text transforming based on rules -- #


def get_rule_to(re_result, rules):
    rule_from = re_result.group(0).strip()
    rule_to = rules[rule_from][0]

    return re_result.group(0).replace(rule_from, rule_to)


def map_text(text, rules):
    """Change text based on the rules.

    Args:
        text: string with the original text,
        rules: dictionary ('pseudo tree') with rules.

    Returns:
        string: 'transformed' string based on rules

    NOTE:
        The rules are applied in the alphabetical order.
    """
    # Go through all the rules (alphabetically). The algorithm is
    # equivalent to 'depth first traversal'.
    for rule_from in sorted(rules.keys()):
        # Get 'to' part of the rule and sub-rules.
        values = rules[rule_from]
        # Get 'to' part.
        rule_to = values[0]
        # 'Apply' the rule.
        text = re.sub(
            r'(^|\s){}(?=\s|$)'.format(rule_from), lambda m: get_rule_to(m, rules), text)
        # Use sub-rules if there are some.
        if len(values) > 1:
            text = map_text(text, values[1])
    # Return transformed text.
    return text


def do_mapping(content, rules):
    """Apply rules on all items in the iterator.

    Args:
        content: iterator with loaded data,
        rules: dictionary ('pseudo' tree) with rules.

    Yield:
        tuple: (0) - not changed word from loaded data, (1) transformed part
    """
    for item in content:
        word, transcription = re.split('\t+', item)

        yield word, map_text(transcription, rules)


def main(args):
    content_generator = load_file(args.transcript, encoding=args.encoding)
    rules = load_rules(args.rules, encoding=args.encoding)

    mapped = do_mapping(content_generator, rules)

    formatted = mlf_format_data(mapped)

    save_file(args.output, formatted, encoding=args.encoding)


if __name__ == '__main__':
    from sys import exit
    # Parse run atguments.
    args = parser.parse_args()
    # Run main method
    exit(int(main(args) or 0))
