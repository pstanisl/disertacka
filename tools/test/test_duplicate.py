import unittest

import duplicate


class DuplicateTestCase(unittest.TestCase):

    def test_apply_rules(self):
        rules = {
            'A': ['B'],  # 1
            'B': ['C'],  # 2
            'C': ['D'],  # 3
        }

        text = 'A B C D E'

        expected = [
            # O1 -> 1
            'B B C D E',
            # O1 -> 2
            'A C C D E',
            # O1 -> 3
            'A B D D E',
            # O1 -> 1 + 2
            'B C C D E',
            # O1 -> 1 + 3
            'B B D D E',
            # O1 -> 1 + 2 + 3
            'B C D D E',
            # O1 -> 2 + 3
            'A C D D E',
        ]

        applied = list(duplicate.apply_rules(text, rules))

        self.assertEqual(expected, applied)

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
            ('B', 'B C A B D E'),
            # O2
            ('B', 'B C A B D E'),
            # 02 -> 1
            ('B', 'B C B B D E'),
            # 02 -> 2
            ('B', 'C C A C D E'),
            # O2 -> 3
            ('B', 'B D A B D E'),
            # O2 -> 1 + 2
            ('B', 'C C B C D E'),
            # O2 -> 1 + 3
            ('B', 'B D B B D E'),
            # O2 -> 2 + 3
            ('B', 'C D A C D E')
        ]

        duplicated = list(duplicate.duplicate(content, rules))

        self.assertEqual(expected, duplicated)

if __name__ == '__main__':
    unittest.main()
