import unittest

import create_pairs


class CratePairsTestCase(unittest.TestCase):

    def test_reduce_pairs(self):
        pairs = [
            ('A', 'B', '1'),
            ('D', 'E', '2'),
            ('G', 'F', '3'),
            ('B', 'A', '4'),
            ('F', 'G', '5'),
            ('E', 'D', '6')
        ]

        expected = [
            'A;B;1;4',
            'D;E;2;6',
            'G;F;3;5'
        ]

        reduced = list(create_pairs.reduce_pairs(pairs))

        self.assertEqual(expected, reduced)


if __name__ == '__main__':
    unittest.main()
