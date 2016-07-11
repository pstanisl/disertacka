import argparse

from utils import load_file, parse_rules, save_file


def do_mapping(content, rules):
    pass


def main(args):
    content_generator = load_file(args.transcript, encoding=args.encoding)
    rules = load_rules(args.rules, encoding=args.encoding)

    mapped = do_mapping(content_generator, rules)


if __name__ == '__main__':
    from sys import exit
    # Parse run atguments.
    args = parser.parse_args()
    # Run main method
    exit(int(main(args) or 0))
