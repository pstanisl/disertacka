import unittest

import mapping


class MappingTestCast(unittest.TestCase):

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
