import unittest

import mapping


class MappingTestCase(unittest.TestCase):

    def test_do_mapping(self):
        rules = {
            'A': ['B', {'B B': ['B', {'B C D': ['F C']}]}],
            'B': ['C'],
            'C': ['D', {'D D': ['A']}],
            'I': ['J', {'J': ['K']}],
            'Y': ['X']
        }

        content = [
            'A\t\tA B C D E',
            'B\t\tB C A B D E',
            'C\t\tA E Y',
            'D\t\tC C C',
            'E\t\tI',
            'F\t\tJ',
        ]

        expected = [
            ('A', 'F D E'),
            ('B', 'A A E'),
            ('C', 'D E X'),
            ('D', 'A D'),
            ('E', 'K'),
            ('F', 'J'),
        ]

        mapped = list(mapping.do_mapping(content, rules))

        self.assertEqual(expected, mapped)

    def test_map_text(self):
        rules = {
            'A': ['B', {'B B': ['B']}],
            'B': ['C'],
            'C': ['D', {'D D': ['A']}],
        }

        text = 'A B C D E AB'

        mapped = mapping.map_text(text, rules)

        expected = 'A D E AB'

        self.assertEqual(expected, mapped)


if __name__ == '__main__':
    unittest.main()
