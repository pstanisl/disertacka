import argparse

# Define script input arguments
parser = argparse.ArgumentParser()

parser.add_argument('-r', '--reference', action='store',
                    help='path to the file with reference word transctiption')
parser.add_argument('-c', '--recognized', action='store',
                    help='path to the file with recognized words')
parser.add_argument('-o', '--output', action='store',
                    help='output file')

parser.set_defaults(output='./output.txt')


def main(args):
    print('INFO', args)

if __name__ == '__main__':
    from sys import exit

    args = parser.parse_args()

    exit(int(main(args) or 0))
