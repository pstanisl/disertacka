#!/usr/bin/env python3
import argparse
from os.path import join
from utils import load_file, save_file

parser = argparse.ArgumentParser()
parser.add_argument('w1', help='first word of pair')
parser.add_argument('w2', help='second word of pair')
parser.add_argument('f1', help='first filename with pair')
parser.add_argument('f2', help='second filename eith complement pair')
parser.add_argument('dict', help='file with phonetic trascription')
parser.add_argument(
    '-d', '--htkdir', action='store', help='path to the htk directory')
parser.add_argument(
    '-s', '--outscp', action='store', help='path to the output scp file')
parser.add_argument(
    '-v', '--outvocab', action='store', help='path to the output vocab file')
# Set default values
parser.set_defaults(htkdir='./')
parser.set_defaults(outscp='./output.scp')
parser.set_defaults(outvocab='./vocab')


def load_dict(path, encoding='utf-8'):
    for line in load_file(path, encoding=encoding):
        yield line.split('\t')


def make_vocab(dict_content, w1, w2):
    dict_w1 = next(filter(lambda x: x[0] == w1, dict_content))
    dict_w2 = next(filter(lambda x: x[0] == w2, dict_content))

    yield '{}_{}\tpt={}#{}'.format(
        w1, w1, dict_w1[1].replace(' ', ''), dict_w1[1].replace(' ', ''))
    yield '{}_{}\tpt={}#{}'.format(
        w1, w2, dict_w1[1].replace(' ', ''), dict_w2[1].replace(' ', ''))
    yield '{}_{}\tpt={}#{}'.format(
        w2, w1, dict_w2[1].replace(' ', ''), dict_w1[1].replace(' ', ''))
    yield '{}_{}\tpt={}#{}'.format(
        w2, w2, dict_w2[1].replace(' ', ''), dict_w2[1].replace(' ', ''))


def make_scp(data_dir, files):
    for file in files:
        yield join(data_dir, file)


def main(args):
    encoding = 'utf-8'
    # Make scp
    scp_content_gen = make_scp(args.htkdir, [args.f1, args.f2])
    save_file(args.outscp, scp_content_gen, encoding=encoding)
    # Make vocab
    dict_content = list(load_dict(args.dict, encoding=encoding))
    vocab_gen = make_vocab(dict_content, args.w1, args.w2)
    save_file(args.outvocab, vocab_gen, encoding=encoding)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
