import argparse
import re

from utils import load_file

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


def parse(content, replace=0):
    """Parse loaded content from the file with rules. Method can
    be called recursively, because the rules can be in tree structure.

    Args:
        content: list with lines representing tree of rules,
        replace: string replaced on the begining of the rule. In
                 most cases it is used for child rules.

    Return:
        dict: dictionary with pseudo tree structure, representing
              hierarchy of rules

    Note: Example of expected tree format.

        +- rule1_from --> rule1_to
        |  +- sub_rule11_from --> sub_rule11_to
        |  |  +- sub_sub_rule1_from --> sub_sub_rule1_to
        |  +- sub_rule12_from --> sub_rule12_to
        +- rule2_from --> rule2_to
        +- rule3_from --> rule3_to
        |  +- sub_rule3_from --> sub_rule3_to
    """
    # Regular expression for parsing rule.
    re_rule = re.compile(r'\b([\w|\s]+) --> ([\w|\s]+)\b')
    # Dictionary with all parsed rule (some pseudo tree structure).
    rules = {}
    # Curently processed rule.
    current = {}
    # Key representing key of the current rule.
    current_key = None
    # Regular expression for child rules.
    re_replace = re.compile(r'\|\s+' * replace)
    # Go through all loaded lines from the file with the rule.
    while content:
        rule = content.pop(0)
        # Previous rule was su-brule and the current rule is a 'parent'
        # rule. Return from recursion call.
        # print(replace, re_replace.search(rule))
        if replace and not re_replace.search(rule):
            content.insert(0, rule)
            return rules
        # Remove sub-rule mark from the start.
        cleaned_rule = re_replace.sub('', rule, 1)
        # Add rule into a dictionary.
        if (cleaned_rule.startswith('+-')):
            # Parse rule.
            parsed = re_rule.search(rule)
            current_key = parsed.group(1)
            # Create dictionary representing the rule.
            current = {current_key: [parsed.group(2)]}
            # Update dictionary with all rules.
            rules.update(current)
            # Continue with next rule.
            continue
        # Insert sub-rule back into a list and call 'parse' again (recursion).
        content.insert(0, rule)
        # Parse sub-rules.
        subtree = parse(content, replace + 1)
        # Add result of sub-rule parsing into current rule.
        if len(current[current_key]) == 1:
            # Add
            current[current_key].append(subtree)
        else:
            # Update dictionary with previous rule.
            current[current_key][1].update(subtree)

    return rules


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
    return parse(list(raw_rules))


def map_transcription(transcription, rules):
    """
    NOTE:
        The rules are applied in the alphabetical order.
    """
    for key in sorted(rules.keys()):
        # print(key)
        break

    return transcription


def do_mapping(content, rules):
    for item in content:
        word, transcription = re.split('\s\s+', item)

        yield word, map_transcription(transcription, rules)


def main(args):
    content_generator = load_file(args.transcript, encoding=args.encoding)
    rules = load_rules(args.rules, encoding=args.encoding)

    mapped = do_mapping(content_generator, rules)

    print(list(mapped))


if __name__ == '__main__':
    from sys import exit
    # Parse run atguments.
    args = parser.parse_args()
    # Run main method
    exit(int(main(args) or 0))
