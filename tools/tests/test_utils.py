import unittest

import utils

from os.path import dirname, join


class UtilsTestCase(unittest.TestCase):

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

        cleaned = list(utils.clean(items))

        self.assertEqual(expected, cleaned)

    def test_mlf_format_data(self):
        items = [
            ('A', 'A B C D'),
            ('A', 'A C B D'),
            ('B', 'A B C D'),
            ('B', 'A C B D')
        ]

        expected = [
            'A\t\tA B C D',
            'A\t\tA C B D',
            'B\t\tA B C D',
            'B\t\tA C B D'
        ]

        formatted = list(utils.mlf_format_data(items))

        self.assertEqual(expected, formatted)

    def test_load_mlf(self):
        test_mlf = join(dirname(__file__), 'test.mlf')

        mlf = list(utils.load_file(test_mlf))
        control_content = [
            '#!MLF!#',
            '"*/klic1.rec"',
            '00000 8200000 A',
            '8200000 12100000 B',
            '12100000 22000000 C',
            '36500000 43700000 D',
            '43700000 46000000 E',
            '.',
            '"*/klic2.rec"',
            'F',
            'G',
            '.'
        ]

        self.assertEqual(mlf, control_content)


    def test_parse_rules(self):
        input = [
            '+- A --> B',
            '|  +- AA --> BB',
            '|  |  +- AAA --> BBB',
            '|  +- BB --> A',
            '+- B --> C',
            '+- C --> D',
            '|  +- CC --> DD',
        ]

        parsed = utils.parse_rules(input)

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
