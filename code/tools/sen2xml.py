import argparse
import io
import numpy as np
import xml.etree.cElementTree as ET

parser = argparse.ArgumentParser()

parser.add_argument('sentences', help='path to the file with sentences')
parser.add_argument('-s', '--shuffle', help='shuffle loaded sentences',
                    action='store_true')
parser.add_argument('-o', '--output', action='store',
                    help='path to the file with XMl for PhraseRecorder')

parser.set_defaults(output='./phrases.xml')
parser.set_defaults(shuffle=False)


def load(path, encoding='utf-8'):
    with io.open(path, 'r', encoding=encoding) as fr:
        for line in fr:
            yield line.strip()


def save(output, data, encoding='utf-8'):
    phrases = ET.Element('phrases')

    for n, item in enumerate(data):
        index = n + 1
        # ET.SubElement(root, "doc")
        phrase = ET.SubElement(phrases, 'phrase', ID=f'{index:03}',
                               level='1', order='0')
        ET.SubElement(phrase, 'ortho').text = item
        ET.SubElement(phrase, 'phone', type='')

    xmlstr = ET.tostring(phrases, encoding='unicode', method='xml')
    with io.open(output, 'w', encoding=encoding) as fw:
        fw.write(xmlstr)


def main(sentences, output, shuffle):
    l_sentences = list(load(sentences))
    # print(l_sentences)
    np.random.shuffle(l_sentences)
    # print(l_sentences)
    save(output, l_sentences)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args.sentences, args.output, args.shuffle)
