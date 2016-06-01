import unittest

import utils

from os.path import dirname, join


class UtilsTestCase(unittest.TestCase):

    def test_clean_mlf_content(self):
        # Test content with useless time marks.
        content = '00000 8200000 A'
        cleaned = utils.clean_mlf_content(content)
        self.assertEqual('A', cleaned)
        # Test content with only import content.
        cleaned = utils.clean_mlf_content('A')
        self.assertEqual('A', cleaned)
        # Test empty content.
        cleaned = utils.clean_mlf_content('')
        self.assertEqual('', cleaned)

    def test_clean_mlf_key(self):
        # Test full key path.
        cleaned = utils.clean_mlf_key('"*/klic.rec"')
        self.assertEqual('klic', cleaned)
        # Test only basename path.
        cleaned = utils.clean_mlf_key('"klic.rec"')
        self.assertEqual('klic', cleaned)
        # Test path without file extension.
        cleaned = utils.clean_mlf_key('"*/klic"')
        self.assertEqual('klic', cleaned)

    def test_load_mlf(self):
        test_mlf = join(dirname(__file__), 'test.mlf')

        mlf = list(utils.load_mlf(test_mlf))
        control_content = [
            ('klic1', ['A', 'B', 'C', 'D', 'E']),
            ('klic2', ['F', 'G'])
        ]

        self.assertEqual(mlf, control_content)


if __name__ == '__main__':
    unittest.main()
