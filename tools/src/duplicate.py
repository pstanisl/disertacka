import argparse
import re

from functools import reduce
from itertools import combinations, chain

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


def get_combinations(rules):
    """Create posible combinations of rules keys.

    Args:
        rules: list of items to combine.

    Yield:
        list: single combination of rules.

    Note:
        Methods retunds all posible combinations, e.g.
        'ABC' -> 'A', 'B', 'C', 'AB', 'AC', 'BC', 'ABC'
    """
    # Sort items -> to ensure determinism
    items = sorted(rules)
    # Create list of all combinations. It contains iterators.
    all_combinations = [
        combinations(items, r) for r in range(1, len(items) + 1)
    ]
    # Chain iterators and yield a single rule.
    for rule in reduce(lambda x, y: chain(x, y), chain(all_combinations)):
        yield sorted(rule)


def get_rule_to(re_result, rules):
    rule_from = re_result.group(0).strip()
    rule_to = rules[rule_from][0]

    return re_result.group(0).replace(rule_from, rule_to)


def apply_rules(text, rules):
    """Apply all possible combinations of the rules. All result in combination
    are applied at the same time.

    Args:
        text: text where the rules will be applied,
        rules: dictionary ('pseudo' tree) with rules.

    Yield:
        string: text after application of a rule.
    """
    # Create all posible rule combinations and applied them.
    for rule_keys in get_combinations(rules.keys()):
        # Convert 'from' part of the every rule in a combination and create
        # regular expression pattern with all rules from combination.
        mapped = map(lambda item: r'(\s*){}(\s)'.format(item), rule_keys)
        rule_from = reduce(lambda x, y: r'{}|{}'.format(x, y), mapped)
        # Apply rules. Because regular expression contains multiple rules
        # so as a to pattern is used a function where is physically
        # replaced substring corresponding to the rule in the pattern.
        yield re.sub(rule_from, lambda m: get_rule_to(m, rules), text)


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
