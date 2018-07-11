import argparse
import codecs

try:
    from progressbar import ProgressBar
    SHOW_PROGRESS = True
except:
    SHOW_PROGRESS = False

# Define script input arguments
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', action='store',
                    help='path to the file with vocabs + sentences')
parser.add_argument('-o', '--output', action='store',
                    help='path to the file with vocabs pair from file with vocabs + sentences')

parser.set_defaults(output='./output.txt')


def get_content(path, *, encoding='utf-8'):
    """Load content from the file with vocabs + sentences and filter
     only vocab pairs.

    Args:
        path: path to the file
        encoding: encoding of the file

    Yields:
        string: cleaned vocab pair
    """
    with codecs.open(path, encoding=encoding) as content:
        # Load all lines from the file.
        lines = content.readlines()
        # Initialize progress bar.
        if (SHOW_PROGRESS):
            pbar = ProgressBar(maxval=len(lines)).start()
        # Go through all the lines in the file and filter only
        # lines representing vocabs pairs.
        for n, line in enumerate(lines):
            # Remove white characters on the beginning and the end of the line.
            line = line.strip()
            # Skip line if the line is not vocabs pair.
            if not line.startswith('##'):
                continue
            # Clean pair
            yield line.replace('##', '').strip()
            # Update progress
            if SHOW_PROGRESS:
                pbar.update(n)
    # Finish progressbar
    if SHOW_PROGRESS:
        pbar.finish()


def save_pairs(path, data, *, encoding='utf-8'):
    """Save filtered content into a file.

    Args:
        path: path to the output file
        data: iterable with filtered data
        encoding: encoding of the output file
    """
    with codecs.open(path, 'w', encoding=encoding) as output:
        for pair in data:
            output.write('{}\n'.format(pair))


def main(args):
    content_gen = get_content(args.input)
    save_pairs(args.output, content_gen)


if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
