from __future__ import print_function

import argparse
import codecs
import csv
import re

from itertools import product
from os.path import splitext
# from lcs import lcs
from tools import fn_timer

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
    """Cluster all the words with the same transcription.

    Examples:
        >>> vocabs = [('b', 'a'), ('c', 'a'), ('B', 'a'), ('a', 'b')]
        >>> clustering(vocabs)
        {'a': set(['c', 'b']), 'b': set(['a'])}
    """
    clusters = {}

    for n, (word, transcript) in enumerate(vocabs):

        if transcript not in clusters:
            clusters[transcript] = set([])

        clusters[transcript].update([word.lower()])

    return clusters


def combine(clusters):
    """Create all combinations of cluster keys.

    Note:
        Nomber of generated item is equal to

            count * (count - 1) / 2,

        if `count` is equal to number of keys in clusters.


    Args:
        clusters: dictionary with `key` equal to transcription and `value` to
            set of all words corresponding to the transcription
    Yields:
        tuple: combination of two keys from the cluster
    """
    # Get all keys from clusters.
    content = list(clusters.keys())
    # Get number of keys in the clusters.
    count = len(content)
    # Show progress if it's available.
    if (SHOW_PROGRESS):
        maxval = count * (count - 1) / 2
        pbar = ProgressBar(maxval=maxval).start()

    cycles = 0
    # Create all combinations.
    for x in range(count):
        x_transcript = content[x]

        for y in range(x + 1, count):
            yield x_transcript, content[y]

            cycles += 1
            # Update progressbar on the screen
            if SHOW_PROGRESS:
                pbar.update(cycles)
    # Finish progressbar
    if SHOW_PROGRESS:
        pbar.finish()


def get_index(l, x):
    """Get index of an item `x` in the list `l`. If the
    item is not in the list return `-1`.

    Examples:
        >>> l = [1, 2, 3, 4]
        >>> get_index(l, 1)
        0
        >>> get_index(l, 5)
        -1
    """
    return l.index(x) if x in l else -1


def get_interesting(combinations, phoneme_pairs):
    """Find all `interesting` words pairs.

    Args:
        combinations: iterator with all word combinations,
        phoneme_pairs: list of all `interestiong` phoneme paisr,
            e.g. voicing + voiceless

    Yields:
        tuple: pair of two `interesting words`
    """
    # Unzip list with phoneme pairs.
    pair_left, pair_right = zip(*phoneme_pairs)
    # Concatenate left and right part of phoneme pairs.
    phonemes = [ord(char) for char in pair_left + pair_right]
    # Concatenate right and left part of phoneme pairs.
    phonemes_reverse = [ord(char) for char in pair_right + pair_left]
    # Go through all word combinations.
    for first, second in combinations:
        # Check if the differences between words corresond to
        # some phoneme pair.
        if (len(first) == len(second) and
                is_voicing(first, second, phonemes, phonemes_reverse)):
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
        # Get product of two sets,
        # e.q (1, 2), (3, 4) -> (1, 3), (1, 4), (2, 3), (2, 4).
        c_product = product(clusters[transcript1], clusters[transcript2])
        # Go through all word combinations from both transcriptions.
        for word1, word2 in c_product:
            # Skip the same words.
            if (word1 == word2):
                continue
            # Put both words into sorted tuple - sorting eliminating
            # problems with order.
            together = tuple(sorted((word1, word2)))
            # Skip if the words combination was already used.
            if (together in words):
                continue
            # Store words in set (used during checking).
            words.update([together])

            yield together


def is_voicing(first, second, phonemes, phonemes_reverse):
    """Check if the difference in two words corresponds to some phoneme pair.

    Args:
        first: fisrt word,
        second: second word,
        phonemes: list with concatenated left and right parts of all
            phoneme pairs,
        phonemes_reverse: list with concatenated right and left parts all
            phoneme pairs

    Note:
        `phonemes` and `phonemes_reverse` are lists created from phoneme pair
        list (e.g. [('p', 'b'), ('s', 'z')]). So `phonemes` is concatenated
        left and right parts of the pairs (e.g ['p', 's', 'b', 'z']) and
        `phonemes_reverse` on the other hand is rigth + left part
        (e.g ['b', 'z', 'p', 's']), i.e. an item on index in `phoneme`
        corresponds to the opposite item in `phoneme_reverse` and vice versa.

    Returns:
        bool: True if all the differences correscpons to some pair,
            otherwise False. False is also returned if `first` and `second`
            are the same.
    """
    if (first == second):
        return False

    ret = True

    for char1, char2 in zip(first, second):
        # Skip if the chars are the same.
        if (char1 == char2):
            continue
        # Get index of the char in the list with 'interestiong' phonemes. If
        # the char is not in the list methods return -1.
        index1 = get_index(phonemes, ord(char1))
        index2 = get_index(phonemes_reverse, ord(char2))
        # One of the char is not in a list.
        if (index1 == -1 or index2 == -1):
            ret &= False
            continue
        # Check if the char difference coresponds to a phoneme pair.
        ret &= index1 == index2

    return ret


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
        for word1, word2 in words:
            interesting.write(u'{} - {}\n'.format(word1, word2))


@fn_timer
def main(args):
    phoneme_pairs = load_pairs(args.phonemes, args.delimiter, args.pairs)
    vocabs = load_vocabs(args.path, args.pattern, args.input)

    clusters = clustering(vocabs)

    combinations = combine(clusters)

    interesting = get_interesting(combinations, phoneme_pairs)

    words = get_words(clusters, interesting)

    save_interesting(args.path, words, args.output, args.suffix)


if __name__ == "__main__":
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
