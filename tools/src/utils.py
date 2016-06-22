import codecs
import re

def load_file(path, *, encoding='utf-8'):
    """Load raw text content of the file.

    Args:
        path: path to the file
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        str: non empty lines
    """
    with codecs.open(path, encoding=encoding) as input_file:
        for line in input_file.readlines():
            # Remove whitechars, line endings, etc. from the
            # beginning and the end of a line.
            line = line.strip()
            # Skip empty lines.
            if not line:
                continue
            yield line


def save_file(path, data, *, encoding='uft-8'):
    """Save items from an iterator into a file. On the end of the
    file is empty line.

    Args:
        path: path to the output file
        data: an iterator with content
        encoding: encoding of the output file
    """
    with codecs.open(path, 'w', encoding=encoding) as target:
        for item in data:
            target.write('{}\n'.format(item))


# -- Rules parsing -- #

def parse_rules(content, replace=0):
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
        subtree = parse_rules(content, replace + 1)
        # Add result of sub-rule parsing into current rule.
        if len(current[current_key]) == 1:
            # Add
            current[current_key].append(subtree)
        else:
            # Update dictionary with previous rule.
            current[current_key][1].update(subtree)

    return rules
