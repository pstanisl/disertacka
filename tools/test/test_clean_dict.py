import unittest

import clean_dict


class CleanDictTestCase(unittest.TestCase):

    def test_clean(self):
        data = ['a b c', 'a a a', 'a c d', 'e f g', 'i j k', 'a _a_ a']
        pattern = 'b|e|k|_a_'

        cleaned = list(clean_dict.clean(data, pattern))

        expected = ['a a a', 'a c d']

        self.assertEqual(expected, cleaned)


if __name__ == '__main__':
    unittest.main()
