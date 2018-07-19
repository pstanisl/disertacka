import argparse
import io
import xml.etree.cElementTree as ET

from os.path import join

parser = argparse.ArgumentParser()

parser.add_argument('phrases', help='path to the PhraseRecorser XML file')
parser.add_argument('-o', '--output', action='store',
                    help='output directory for txt files')

parser.set_defaults(output='./')


def get_phrases(phrases):
    for phrase in phrases:
        yield phrase.get('ID'), phrase.find('ortho').text


def save_into_txt(output, phrases, encoding='utf-8'):
    for id, phrase in phrases:
        print(id, phrase)
        with io.open(join(output, f'{id}_00.txt'), 'w', encoding=encoding) as fw:
            fw.write(phrase)


def main(phrases, output):
    tree = ET.parse(phrases)
    i_phrases = get_phrases(tree.getroot())
    save_into_txt(output, i_phrases)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.phrases, args.output)
