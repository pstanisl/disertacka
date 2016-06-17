import unittest

import mapping


class MappingTestCast(unittest.TestCase):

    def test_do_mapping(self):
        rules = {
            'A': ['B', {'B B': ['B', {'B C D': ['F C']}]}],
            'B': ['C'],
            'C': ['D', {'D D': ['A']}],
        }

        content = [
            'A\t\tA B C D E',
            'B\t\tB C A B D E'
        ]

        expected = [
            ('A', 'F D E'),
            ('B', 'A A E')
        ]

        mapped = list(mapping.do_mapping(content, rules))

        self.assertEqual(expected, mapped)

    def test_format_data(self):
        data = [
            ('A', 'F D E'),
            ('B', 'A A E')
        ]

        expected = [
            'A\t\tF D E',
            'B\t\tA A E'
        ]

        formatted = list(mapping.format_data(data))

        self.assertEqual(expected, formatted)

    def test_map_text(self):
        rules = {
            'A': ['B', {'B B': ['B']}],
            'B': ['C'],
            'C': ['D', {'D D': ['A']}],
        }

        text = 'A B C D E'

        mapped = mapping.map_text(text, rules)

        expected = 'A D E'

        self.assertEqual(expected, mapped)

    def test_parse(self):
        input = [
            '+- A --> B',
            '|  +- AA --> BB',
            '|  |  +- AAA --> BBB',
            '|  +- BB --> A',
            '+- B --> C',
            '+- C --> D',
            '|  +- CC --> DD',
        ]

        parsed = mapping.parse(input)

        expected = {
            'A': ['B', {
                'AA': ['BB', {'AAA': ['BBB']}],
                'BB': ['A']
                }],
            'B': ['C'],
            'C': ['D', {'CC': ['DD']}],
        }

        self.assertEqual(expected, parsed)


if __name__ == '__main__':
    unittest.main()
