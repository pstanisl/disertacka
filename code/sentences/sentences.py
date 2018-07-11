import argparse

import codecs

from tools import fn_timer

try:
    from progressbar import ProgressBar
    SHOW_PROGRESS = True
except:
    SHOW_PROGRESS = False

# Define script input arguments
parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output', action='store',
                    help='path to the file with combined vocabs and sentences')
parser.add_argument('-s', '--sentences', action='store',
                    help='path to the file with sentences')
parser.add_argument('-v', '--vocabs', action='store',
                    help='path to the file with vocabs')

parser.set_defaults(output='./output.txt')


def get_sentences(path, *, encoding='utf-8'):
    """Load sentences from file. Every sentence on a single file.

    Args:
        path: path to the file with sentences,
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        sentence: string with loaded sentence
    """
    with codecs.open(path, encoding=encoding) as sentences:
        for sentence in sentences.readlines():
            # Remove white space from the beginning and the end.
            sentence = sentence.strip()
            # Skip empty sentence.
            if not sentence:
                continue
            # Return loaded sentence.
            yield sentence


def get_vocabs(path, *, encoding='utf-8'):
    """Load vocabs from file. Every vocab pair on a single file.

    Args:
        path: path to the file with sentences,
        encoding: encoding of the content in the file (default=utf-8)

    Yields:
        vocab: string with loaded vocabs pair
    """
    with codecs.open(path, encoding=encoding) as vocabs:
        for vocab in vocabs.readlines():
            # Remove white space from the beginning and the end.
            vocab = vocab.strip()
            # Skip empty line.
            if not vocab:
                continue
            # Return loaded vocabs pair.
            yield vocab


def find_sentences(vocabs, sentences):
    """Find all sentences for vocab1 and vocab2.

    Args:
        vocabs: iterable with vocab pairs,
        sentences: iterable with sentences.

    Yields:
        tuple: vocab pair + sentences1 + sentences2
    """
    for vocab in vocabs:
        vocab1, vocab2 = vocab.lower().split(' - ')
        # Find all sentences with the vocab. It is not optimal but
        # performance is not bad at all.
        filtered1 = filter(
            lambda sentence: vocab1 in sentence.lower().split(), sentences)
        filtered2 = filter(
            lambda sentence: vocab2 in sentence.lower().split(), sentences)
        # Return vocab and all related sentences.
        yield vocab, filtered1, filtered2


def save_senteces(path, combined, *, encoding='utf-8'):
    """Save found senteces for vocabs. Data are saved with vocab paisr in format:
        '## vobab1 - vocab2'
        '# - 1'
        'sentences for the vocab1'
        '# - 2'
        'sentences for the vocab2'

    Note:
        If there is no sentences for a vocab the pair is skipped.

    Args:
        path: path to the output file,
        combined: iterable with vocab pair, sentences for vocab1, sentences for vocab2,
        encoding: encoding of the output file
    """
    with codecs.open(path, 'w', encoding=encoding) as output:
        for vocab, sentences1, sentences2 in combined:
            sentences1 = list(sentences1)
            sentences2 = list(sentences2)
            # Skip if one of the list is empty. Imposible to find sentences
            # for a vocab.
            if len(sentences1) == 0 or len(sentences2) == 0:
                continue
            # Save into a file.
            output.write('## {}\n'.format(vocab))
            # Save sentences for the first vocab.
            output.write('# - 1\n')
            for sentence in sentences1:
                output.write('{}\n'.format(sentence))
            # Save sentences for the second vocab.
            output.write('# - 2\n')
            for sentence in sentences2:
                output.write('{}\n'.format(sentence))


@fn_timer
def main(args):
    sentences = list(get_sentences(args.sentences))
    vocabs = get_vocabs(args.vocabs)

    combined = find_sentences(vocabs, sentences)

    save_senteces(args.output, combined)

if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
