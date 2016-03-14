import unittest

import lcs


class LCSTestCase(unittest.TestCase):
    """Test for `lcs.py`."""

    def test_lcs_abcd_acbd(self):
        seq1 = 'abcd'
        seq2 = 'acbd'

        result = [['a', 'c', 'd'], ['a', 'b', 'd']]

        self.assertEqual(lcs.lcs(seq1, seq2), result)

    def test_lcs_acbd_empty(self):
        seq1 = 'acbd'
        seq2 = ''

        result = [[]]

        self.assertEqual(lcs.lcs(seq1, seq2), result)

    def test_lcs_empty_acbd(self):
        seq1 = ''
        seq2 = 'acbd'

        result = [[]]

        self.assertEqual(lcs.lcs(seq1, seq2), result)

    def test_lcs_kosa_koza(self):
        seq1 = 'kosa'
        seq2 = 'koza'

        result = [['k', 'o', 'a']]

        self.assertEqual(lcs.lcs(seq1, seq2), result)

    def test_lcs_mat_abcd_acbd(self):
        seq1 = 'abcd'
        seq2 = 'acbd'

        result = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 1, 1, 2, 2],
            [0, 1, 2, 2, 2],
            [0, 1, 2, 2, 3]
        ]

        self.assertEqual(lcs.lcs_mat(seq1, seq2), result)

    def test_lcs_mat_empty_acbd(self):
        seq1 = ''
        seq2 = 'acbd'

        result = [
            [0, 0, 0, 0, 0]
        ]

        self.assertEqual(lcs.lcs_mat(seq1, seq2), result)

    def test_lcs_mat_acbd_empty(self):
        seq1 = 'acbd'
        seq2 = ''

        result = [[0], [0], [0], [0], [0]]

        self.assertEqual(lcs.lcs_mat(seq1, seq2), result)

    def test_lcs_mat_acbd_acbd(self):
        seq1 = 'acbd'
        seq2 = 'acbd'

        result = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 1, 2, 2, 2],
            [0, 1, 2, 3, 3],
            [0, 1, 2, 3, 4]
        ]

        self.assertEqual(lcs.lcs_mat(seq1, seq2), result)


if __name__ == "__main__":
    unittest.main()
