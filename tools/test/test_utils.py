import unittest

import utils

from os.path import dirname, join


class UtilsTestCase(unittest.TestCase):

    def test_load_mlf(self):
        test_mlf = join(dirname(__file__), 'test.mlf')

        mlf = list(utils.load_file(test_mlf))
        control_content = [
            '#!MLF!#',
            '"*/klic1.rec"',
            '00000 8200000 A',
            '8200000 12100000 B',
            '12100000 22000000 C',
            '36500000 43700000 D',
            '43700000 46000000 E',
            '.',
            '"*/klic2.rec"',
            'F',
            'G',
            '.'
        ]

        self.assertEqual(mlf, control_content)


if __name__ == '__main__':
    unittest.main()
