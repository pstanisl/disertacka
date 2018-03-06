import unittest

from os.path import dirname, join

import pyeval2matrix as pe2mx


class Pyeval2MatrixTestCase(unittest.TestCase):

    def test_load_pyeval(self):
        test_file = join(dirname(__file__), 'pyeval_output.test.txt')

        expected = [
            ['a', 'a',  2],
            ['a', 'b', -1],
            ['a', 'c', -2],
            ['b', 'a',  1],
            ['b', 'b',  3],
            ['b', 'c', -1],
            ['c', 'a',  2],
            ['c', 'b',  1],
            ['c', 'c',  4],
        ]

        loaded = list(pe2mx.load_pyeval(test_file))

        self.assertEqual(expected, loaded)

    def test_create_confusion_matrix(self):
        input = [
            ['a', 'a',  2],
            ['a', 'b', -1],
            ['a', 'c', -2],
            ['b', 'a',  1],
            ['b', 'b',  3],
            ['b', 'c', -1],
            ['c', 'a',  2],
            ['c', 'b',  1],
            ['c', 'c',  4],
            ['a', 'd',  1],
        ]

        expected = [
            ['a', 'b', 'c', 'd'],
            [2, -1, -2, 1],
            [1,  3, -1, 0],
            [2,  1,  4, 0],
            [0,  0,  0, 0],
        ]
        # Get matrix
        matrix = list(pe2mx.create_confusion_matrix(input))
        # Compare
        self.assertEqual(expected, matrix)


if __name__ == '__main__':
    unittest.main()
