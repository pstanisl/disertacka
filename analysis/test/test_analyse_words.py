import unittest

import analyse
from lcs import lcs_mat


class AnalyseTetstCase(unittest.TestCase):

    def test_get_diffs(self):
        # ex1 - 'ABCD' vs. 'ABED'
        ref = 'ABCD'
        rec = 'ABED'
        # Get LCS matrix.
        matrix = lcs_mat(ref, rec)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, ref, rec))
        # Compare
        self.assertEqual([(['C'], ['E'])], diffs)
        # ex2 - 'A B C D' vs. 'A B C1 C2 D'
        ref = 'ABCD'
        rec = ['A', 'B', 'C1', 'C2', 'D']
        # Get LCS matrix.
        matrix = lcs_mat(ref, rec)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, ref, rec))
        # Compare
        self.assertEqual([(['C'], ['C1', 'C2'])], diffs)
        # ex3 - 'A B C1 C2 D' vs. 'A B C D'
        # Get LCS matrix.
        matrix = lcs_mat(rec, ref)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, rec, ref))
        # expected = [(['C1', 'C2'], ['C'])]
        # Compare
        self.assertEqual([(['C1', 'C2'], ['C'])], diffs)
        # ex4 - 'A B C D' vs. 'A B D'
        ref = 'ABCD'
        rec = 'ABD'
        # Get LCS matrix.
        matrix = lcs_mat(ref, rec)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, ref, rec))
        # Compare
        self.assertEqual([(['C'], [])], diffs)
        # ex5 - 'A B D' vs. 'A B C D'
        # Get LCS matrix.
        matrix = lcs_mat(rec, ref)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, rec, ref))
        # Compare
        self.assertEqual([([], ['C'])], diffs)
        # ex5 - 'A B C D E F' vs. 'A B C1 C2 D G F'
        ref = 'ABCDEF'
        rec = ['A', 'B', 'C1', 'C2', 'D', 'G', 'F']
        # Get LCS matrix.
        matrix = lcs_mat(ref, rec)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, ref, rec))
        # Compare
        self.assertEqual([(['E'], ['G']), (['C'], ['C1', 'C2'])], diffs)
        # ex6 - 'A B C1 C2 D G F' vs. 'A B C D E F'
        # Get LCS matrix.
        matrix = lcs_mat(rec, ref)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, rec, ref))
        # Compare
        self.assertEqual([(['G'], ['E']), (['C1', 'C2'], ['C'])], diffs)
        # ex7 - 'ABCD' vs. 'FBCD'
        ref = 'ABCD'
        rec = 'FBCD'
        # Get LCS matrix.
        matrix = lcs_mat(ref, rec)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, ref, rec))
        # Compare
        self.assertEqual([(['A'], ['F'])], diffs)
        # ex8 - 'AGDBCD' vs. 'FBCD'
        ref = 'AGDBCD'
        rec = 'FBCD'
        # Get LCS matrix.
        matrix = lcs_mat(ref, rec)
        # Find all differences.
        diffs = list(analyse.get_diffs(matrix, ref, rec))
        # Compare
        self.assertEqual([(['A', 'G', 'D'], ['F'])], diffs)


if __name__ == '__main__':
    unittest.main()
