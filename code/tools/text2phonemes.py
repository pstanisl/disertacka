import argparse
import io

from glob import glob
from os.path import basename, join, splitext

parser = argparse.ArgumentParser()

parser.add_argument('directory', help='path to the directory with txt files')
parser.add_argument(
    'dict', help='path to the dictionary with word to phoneme mapping')
parser.add_argument('-o', '--output', action='store',
                    help='output file with phonemes')

parser.set_defaults(output='./phonemes.txt')


def load_dict(path, encoding='utf-8'):
    with io.open(path, 'r', encoding=encoding) as fr:
        for line in fr:
            if not line.strip():
                continue

            yield line.strip().split('\t')


def load_txt(path, encoding='utf-8'):
    for file in glob(join(path, '*.txt')):
        # print(file)
        with io.open(file, 'r', encoding=encoding) as fw:
            yield splitext(basename(file))[0], ''.join(fw.readlines()).strip()


def save(path, content, encoding='utf-8'):
    with io.open(path, 'w', encoding=encoding) as fw:
        for name, phonemes in content:
            fw.write(f'{name}\t{phonemes}\n')


def convert(contents, mapping):
    for name, content in contents:
        words_in_phonemes = [mapping[word] for word in content.split(', ')]
        yield name, ' '.join(words_in_phonemes)


def main(directory, dictionary, output):
    mapping = dict(load_dict(dictionary, encoding='cp1250'))
    names_contents = load_txt(directory)
    phonemes = convert(names_contents, mapping)
    save(output, phonemes)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.directory, args.dict, args.output)
