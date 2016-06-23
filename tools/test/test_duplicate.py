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

        expected = sorted([
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
        ])

        applied = sorted(duplicate.apply_rules(text, rules))

        self.assertEqual(expected, applied)

    def test_clean(self):
        items = [
            ('A', 'A B C D'),
            ('A', 'A B C D'),
            ('A', 'A C B D'),
            ('B', 'A B C D'),
            ('B', 'A C B D'),
            ('A', 'A C B D')
        ]

        expected = [
            ('A', 'A B C D'),
            ('A', 'A C B D'),
            ('B', 'A B C D'),
            ('B', 'A C B D')
        ]

        cleaned = list(duplicate.clean(items))

        self.assertEqual(expected, cleaned)

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

        expected = sorted([
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
            ('B', 'C D A C D E'),
            # O2 -> 1 + 2 + 3
            ('B', 'C D B C D E')
        ])

        duplicated = sorted(duplicate.duplicate(content, rules))

        self.assertEqual(expected, duplicated)

    def test_get_combinations(self):
        rules = {
            'A': ['B'],  # 1
            'B': ['C'],  # 2
            'C': ['D'],  # 3
        }

        expected = sorted([
            ['A', ],
            ['B', ],
            ['C', ],
            ['A', 'B'],
            ['A', 'C'],
            ['B', 'C'],
            ['A', 'B', 'C']
        ], key=lambda item: (len(item), item[0]))

        combinations = sorted(duplicate.get_combinations(rules.keys()),
                              key=lambda item: (len(item), item[0]))

        self.assertEqual(expected, combinations)


if __name__ == '__main__':
    unittest.main()
