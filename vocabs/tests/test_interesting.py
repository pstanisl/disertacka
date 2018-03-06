import unittest

import interesting


class InterestingTestCase(unittest.TestCase):

    def test_clustering(self):
        vocabs = [('b', 'a'), ('c', 'a'), ('B', 'a'), ('a', 'b')]

        result = {'a': set(['b', 'c', 'b']), 'b': set(['a'])}

        self.assertEqual(interesting.clustering(vocabs), result)

    def test_combine(self):
        clusters = {'a': 'a', 'b': 'b', 'c': 'c'}

        result = sorted([('a', 'c'), ('a', 'b'), ('b', 'c')])
        # Eliminate error if the data are not well sorted.
        combined = sorted(
            map(lambda x: tuple(sorted(x)), interesting.combine(clusters)))

        self.assertEqual(combined, result)

    def test_get_index(self):
        l = [1, 2, 3, 4]
        # Test existing item
        self.assertEqual(interesting.get_index(l, 2), 1)
        # Test non-exiting item
        self.assertEqual(interesting.get_index(l, 5), -1)

    def test_get_interesting(self):
        combinations = [('ab', 'cb'), ('db', 'eb'), ('cb', 'bb')]
        phoneme_pairs = [('a', 'c'), ('d', 'e')]

        result = [('ab', 'cb'), ('db', 'eb')]

        self.assertEqual(
            list(interesting.get_interesting(combinations, phoneme_pairs)),
            result)

    def test_get_output_path(self):
        path = './test.txt'
        suffix = '_suffix'

        result = './test_suffix.txt'

        self.assertEqual(interesting.get_output_path(path, suffix), result)

    def test_get_words(self):
        clusters = {
            'a': set(['aa', 'ab']),
            'b': set(['ba', 'bb']),
            'c': set(['ca']),
            'd': set(['da']),
            'e': set(['aa', 'ab'])
        }
        interes = [('a', 'c'), ('a', 'd'), ('a', 'e')]

        result = [('aa', 'ca'), ('aa', 'da'), ('ab', 'ca'), ('ab', 'da')]
        words = interesting.get_words(clusters, interes)

        self.assertEqual(sorted(words), result)

    def test_is_voicing(self):
        first = 'abcd'
        second = 'acbd'

        phoneme = [ord('a'), ord('b'), ord('e'), ord('c')]
        phoneme_reverse = [ord('e'), ord('c'), ord('a'), ord('b')]

        self.assertTrue(interesting.is_voicing(
            first, second, phoneme, phoneme_reverse))

        phoneme = [ord('a'), ord('e'), ord('c'), ord('d')]
        phoneme_reverse = [ord('c'), ord('d'), ord('a'), ord('e')]

        self.assertFalse(interesting.is_voicing(
            first, second, phoneme, phoneme_reverse))

if __name__ == "__main__":
    unittest.main()
