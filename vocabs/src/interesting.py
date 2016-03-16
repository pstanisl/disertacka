from __future__ import print_function

import argparse
import codecs
import csv
import re

from os.path import splitext

from lcs import lcs

try:
    from progressbar import ProgressBar
    SHOW_PROGRESS = True
except:
    SHOW_PROGRESS = False

KKY_PATTERN = '([^\t]+)\t+([^$]+)'

# Define script input arguments
parser = argparse.ArgumentParser()
parser.add_argument('path', help='path to the file with vocabs')
parser.add_argument('phonemes',
                    help='path to the file with interestiong phoneme pairs')
parser.add_argument(
    '-a', '--pairs', action='store',
    help='encoding of the file with phoneme pairs (default=UTF-8)')
parser.add_argument('-d', '--delimiter', action='store',
                    help='delimiter used for parsing pairs (default=\',\')')
parser.add_argument('-i', '--input', action='store',
                    help='encoding of the file with vocabs (default=UTF-8)')
parser.add_argument('-o', '--output', action='store',
                    help='encoding of the output file (default=UTF-8)')
parser.add_argument(
    '-p', '--pattern', action='store',
    help='regex pattern used for parsing vocabs (default=\'{}\')'.format(
        KKY_PATTERN))
parser.add_argument(
    '-s', '--suffix', action='store',
    help='suffix appended to the vocabs file name (default=\'_interesting\')')

# Default paramets
parser.set_defaults(delimiter=',')
parser.set_defaults(input='utf-8')
parser.set_defaults(output='utf-8')
parser.set_defaults(pairs='utf-8')
parser.set_defaults(pattern=KKY_PATTERN)
parser.set_defaults(suffix='_interersing')


def clustering(vocabs):
    """Cluster all the words with the same transcription"""
    clusters = {}

    for n, (word, transcript) in enumerate(vocabs):

        if transcript not in clusters:
            clusters[transcript] = set([])

        clusters[transcript].update([word.lower()])

    return clusters


def diff(clusters):
    content = list(clusters.iteritems())
    count = len(content)

    if (SHOW_PROGRESS):
        maxval = count * (count - 1) / 2
        pbar = ProgressBar(maxval=maxval).start()

    for x in xrange(count):
        x_transcript = content[x][0]

        for y in xrange(x + 1, count):
            y_transcript = content[y][0]

            alcs = lcs(x_transcript, y_transcript)

            yield (x_transcript, y_transcript), alcs

            if SHOW_PROGRESS:
                pbar.update(x + y)

    pbar.finish()

def get_index(l, x):
    """Get index of an item `x` in the list `l`. If the
    item is not in the list return `-1`.
    """
    try:
        return l.index(x)
    except:
        return -1


def get_interesting(diffs, phoneme_pairs):
    # Unzip list with phoneme pairs.
    pair_left, pair_right = zip(*phoneme_pairs)

    for (first, second), diff in diffs:

        if (len(first) == len(second) and
                is_voicing(first, second, pair_left, pair_right)):
            yield (first, second)


def get_output_path(vocabs_path, suffix='_interersing'):
    """Create path to the output file. Output file is in the
    same directory as input file with vocabs, but the name of
    the file is extended by the suffix.

    Args:
        vocabs_path: path to the input file with vocabs,
        suffix: string to extending file name of the original file

    Returns:
        string: path to the output file based on the input path.
    """
    # Split the path by the extension -> returns part
    # before extension, extension with dot
    path, extension = splitext(vocabs_path)
    # Join all parts back together.
    return ''.join([path, suffix, extension])
    # return '{}{}{}'.format(path, suffix, extension)


def get_words(clusters, interesting):
    words = set([])
    for (transcript1, transcript2) in interesting:
        # Check if the transcriptions are not from the same words.
        if (clusters[transcript1] == clusters[transcript2]):
            continue
        # Go through all words for both transcriptions, operator
        # `|` concatenate two sets.
        for word in clusters[transcript1] | clusters[transcript2]:
            # Skip the world if the it was already seen.
            if (word in words):
                continue
            # Add world into set.
            words.update([word])

            yield word


def is_voicing(first, second, pair_left, pair_right):
    """Check if the difference in two words corresponds to some phoneme pair.

    Args:
        first: fisrt word,
        second: second word,
        pair_left: list with all the left parts of all phoneme pairs,
        pair_right: list with all the right parts of all phoneme pairs

    Returns:
        bool: True if all the differences correscpons to some pair,
            otherwise False
    """
    zipped = zip(first, second)
    # Concate phonemes.
    phonemes = pair_left + pair_right
    phonemes_reverse = pair_right + pair_left
    # Get list with indexes matching chars. List contains
    # `-1` if the chars are the same, otherwise `index`.
    indexes = map(
        lambda (index, x): -1 if x[0] == x[1] else index, enumerate(zipped))
    # Remove `-1` values.
    filtered = filter(lambda item: item > -1, indexes)
    # Exchange `index` for the pair of different chars.
    mapped = map(lambda index: zipped[index], filtered)
    # Get list with bool values, True if diff chars are `voice - voiceless`
    # pair, otherwise False.
    match = map(
        lambda (char1, char2): get_index(phonemes, char1) == get_index(
            phonemes_reverse, char2), mapped)
    # Reduce list into single value (AND logic operator).
    return reduce(lambda a, b: a and b, match)


def load_pairs(path, delimiter=',', encoding='utf-8'):
    """Load pairs of phoneme. Mostly voiced and voicels.

    Args:
        path: path to the csv file with pairs,
        delimiter: delimiter used in the csv file,
        encoding: type of encoding of the file

    Yields:
        list: the pair of phonemes, e.g.:

        ['s', 'z']
    """
    with codecs.open(path, 'rb', encoding) as pairs:
        # Load CSV
        reader = csv.reader(pairs, delimiter=delimiter)
        for row in reader:
            yield row


def load_vocabs(path, pattern, encoding='utf-8'):
    """Load word and transcription from the file with vocabs. The
    file contains a word and his transcription. On every line is one
    word and transcription. Format of the pair is described in `pattern`.

    Args:
        path: string with the path to the file,
        pattern: string with regular expression describing format of a
            line in the file,
        encoding: encoding type of the text file

    Yields:
        tuple: the pair of word + transcription, e.g.:

        (word, transcription)
    """
    # Precompile regular expression from the pattern.
    re_compiled = re.compile(pattern)
    # Load and process the data from the file.
    with codecs.open(path, 'r', encoding) as vocabs:
        while True:
            line = vocabs.readline().strip()
            # Stop the loop if the file does not contains line.
            if not line:
                break
            # Parse the line.
            match = re_compiled.match(line)
            # Skip yielding if the file does not correspong to
            # the pattern.
            if not match:
                continue
            # Yield word + transcription
            yield match.groups()


def save_interesting(vocabs_path, words, encoding='utf-8',
                     suffix='_interersing'):
    """Save found interesting words into the file. Data are
    saved into same directory as the original vocabs file is,
    but the name of the file is extended with suffix. Output
    file can also be in a different encoding.

    Args:
        vocabs_path - path to the original file with vocabs,
        words: interable with found `interesting` words,
        encoding: encoding of the created file,
        suffix: string with suffix added to original file name
    """
    # Create output path -> add suffix to the vocabs path.
    path = get_output_path(vocabs_path, suffix)
    # Save words into file on the disk.
    with codecs.open(path, 'w', encoding) as interesting:
        for word in words:
            interesting.write(u'{}\n'.format(word))


def main(args):
    phoneme_pairs = load_pairs(args.phonemes, args.delimiter, args.pairs)
    vocabs = load_vocabs(args.path, args.pattern, args.input)

    clusters = clustering(vocabs)

    diffs = diff(clusters)

    interesting = get_interesting(diffs, phoneme_pairs)

    words = get_words(clusters, interesting)

    save_interesting(args.path, words, args.output, args.suffix)

if __name__ == "__main__":
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
