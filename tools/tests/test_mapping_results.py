import unittest

import mapping_results as mapping


class MappingResultsTestCase(unittest.TestCase):

    def test_do_mapping(self):
        rules = {
            'A': ['B', {'B': ['E']}],
            'D': ['F']
        }

        content = [
            '#!MLF!#',
            '"\'*\'/test.rec"',
            '0 1 A 1234.000',
            '1 2 B 2234.000',
            '3 4 C 3234.000',
            '5 6 D 4234.000',
            '.',
        ]

        expected = [
            ('#!MLF!#',),
            ('"\'*\'/test.rec"',),
            ('0', '1', 'E', '1234.000'),
            ('1', '2', 'B', '2234.000'),
            ('3', '4', 'C', '3234.000'),
            ('5', '6', 'F', '4234.000'),
            ('.',)
        ]

        mapped = list(mapping.do_mapping(content, rules))

        self.assertEqual(expected, mapped)

        content = [
            '#!MLF!#',
            '"\'*\'/test.rec"',
            'A',
            'B',
            'C',
            'D',
            '.',
        ]

        expected = [
            ('#!MLF!#',),
            ('"\'*\'/test.rec"',),
            ('E',),
            ('B',),
            ('C',),
            ('F',),
            ('.',)
        ]

        mapped = list(mapping.do_mapping(content, rules))

        self.assertEqual(expected, mapped)


if __name__ == '__main__':
    unittest.main()
