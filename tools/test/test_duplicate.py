import unittest

import duplicate


class DuplicateTestCase(unittest.TestCase):

    def test_duplicate(self):
        rules = {
            'A': ['B'],  # 1
            'B': ['C'],  # 2
            'C': ['D'],  # 3
        }

        content = [
            'A\t\tA B C D E',
            'B\t\tB C A B D E'
        ]

        expected = [
            # O1
            ('A', 'A B C D E'),
            # O1 -> 1
            ('A', 'B B C D E'),
            # O1 -> 2
            ('A', 'A C C D E'),
            # O1 -> 3
            ('A', 'A B D D E'),
            # O1 -> 1 + 2
            ('A', 'B C C D E'),
            # O1 -> 1 + 3
            ('A', 'B B D D E'),
            # O1 -> 1 + 2 + 3
            ('A', 'B C D D E'),
            # O1 -> 2 + 3
            ('A', 'A C D D E'),
            # O2
            ('B', 'B C A B D E')
        ]

if __name__ == '__main__':
    unittest.main()
