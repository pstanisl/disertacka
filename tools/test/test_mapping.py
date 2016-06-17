import unittest

import mapping


class MappingTestCast(unittest.TestCase):

    def test_parse(self):
        input = [
            '+- A --> B',
            '|  +- AA --> BB',
            '|  |  +- AAA --> BBB',
            '+- B --> C',
            '+- C --> D',
            '|  +- CC --> DD',
        ]

        parsed = mapping.parse(input)

        expected = {
            'A': ['B', {'AA': ['BB', {'AAA': ['BBB']}]}],
            'B': ['C'],
            'C': ['D', {'CC': ['DD']}],
        }

        self.assertEqual(expected, parsed)


if __name__ == '__main__':
    unittest.main()
