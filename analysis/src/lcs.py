# Based on https://github.com/man1/Python-LCS
from __future__ import print_function


def lcs_mat(seq1, seq2):
    """Create LCS table (stored as matrix) with lengths of subsequences.

    Args:
        seq1: first sequence (e.q. list, string, etc.)
        seq2: second sequence (e.q. list, string, etc.)

    Returns:
        A list of lists with lengtht of all common subsequences. For example:

        [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 1, 2, 2, 2],
            [0, 1, 2, 3, 3],
            [0, 1, 2, 3, 4]
        ]

        If the `seq1='abcd'` and `seq2='acbd'`.

    Examples:
        >>> lcs_mat('ac', 'ac')
        [[0, 0, 0], [0, 1, 1], [0, 1, 2]]
    """
    m = len(seq1)
    n = len(seq2)
    # Construct the matrix, of all zeroes.
    mat = [[0] * (n+1) for row in range(m+1)]
    # Populate the matrix, iteratively
    for row in range(1, m+1):
        for col in range(1, n+1):
            if seq1[row - 1] == seq2[col - 1]:
                # If it's the same element, it's one longer than the LCS of
                # the truncated lists.
                mat[row][col] = mat[row - 1][col - 1] + 1
            else:
                # They're not the same, so it's the the maximum of the lengths
                # of the LCSs of the two options (different list truncated in
                # each case).
                mat[row][col] = max(mat[row][col - 1], mat[row - 1][col])
    # The matrix is complete
    return mat


def all_lcs(lcs_dict, mat, seq1, seq2, index1, index2):
    """Find all longest common subsequences. Method is using recursiveness.

    Args:
        lcs_dict: dictionary with subsequences
        mat: matrix with lengthts of subsequences (fron `lcs_mat`)
        seq1: first sequence (e.q. list, string, etc.)
        seq2: second sequence (e.q. list, string, etc.)
        index1: length of the first sequence
        index2: length of the second sequence

    Returns:
        A list of lists with lengtht of all common subsequences. For example:

        [['a', 'c', 'd'], ['a', 'b', 'd']]

        If the `seq1='abcd'` and `seq2='acbd'`.

    Examples:
        >>> all_lcs({}, lcs_mat('ac', 'ac'), 'ac', 'ac', 2, 2)
        [['a', 'c']]
        >>> all_lcs({}, lcs_mat('abcd', 'acbd'), 'abcd', 'acbd', 4, 4)
        [['a', 'c', 'd'], ['a', 'b', 'd']]
        >>> all_lcs({}, lcs_mat('ac', 'bd'), 'ac', 'bd', 2, 2)
        [[]]
    """
    # If we've calculated it already, just return that
    if (index1, index2) in lcs_dict:
        return lcs_dict[(index1, index2)]
    # Otherwise, calculate it recursively
    if (index1 == 0) or (index2 == 0):  # Base case
        return [[]]
    elif seq1[index1 - 1] == seq2[index2 - 1]:
        # Elements are equal! Add it to all LCSs that pass through
        # these indices
        lcs_dict[(index1, index2)] = [
            prevs + [seq1[index1 - 1]] for prevs in all_lcs(
                lcs_dict, mat, seq1, seq2, index1 - 1, index2 - 1)
        ]
        return lcs_dict[(index1, index2)]
    else:
        lcs_list = []  # Set of sets of LCSs from here.
        # Not the same, so follow longer path recursively
        if mat[index1][index2 - 1] >= mat[index1 - 1][index2]:
            before = all_lcs(lcs_dict, mat, seq1, seq2, index1, index2 - 1)
            for series in before:  # Iterate through all those before.
                # and if it's not already been found, append to lcs_list
                if series not in lcs_list:
                    lcs_list.append(series)
        if mat[index1 - 1][index2] >= mat[index1][index2 - 1]:
            before = all_lcs(lcs_dict, mat, seq1, seq2, index1 - 1, index2)
            for series in before:
                if series not in lcs_list:
                    lcs_list.append(series)
        lcs_dict[(index1, index2)] = lcs_list
        return lcs_list


def lcs(seq1, seq2):
    """Get all longest common subsequences of two sequences.

    Args:
        seq1: first sequence (e.q. list, string, etc.)
        seq2: second sequence (e.q. list, string, etc.)

    Returns:
        A list of lists with lengtht of all common subsequences. For example:

        [['a', 'c', 'd'], ['a', 'b', 'd']]

        If the `seq1='abcd'` and `seq2='acbd'`.

    Examples:
        >>> lcs('ac', 'ac')
        [['a', 'c']]
        >>> lcs('abcd', 'acbd')
        [['a', 'c', 'd'], ['a', 'b', 'd']]
        >>> lcs('ac', 'bd')
        [[]]
    """
    # Mapping of indices to list of LCSs, so we can cut down recursive
    # calls enormously
    mapping = dict()
    matrix = lcs_mat(seq1, seq2)
    # Start the process...
    return all_lcs(mapping, matrix, seq1, seq2, len(seq1), len(seq2))


def main():
    str1 = 'abcd'
    str2 = 'acbd'
    # str1 = 'kosa'
    # str2 = 'koza'

    print(lcs(str1, str2))

if __name__ == '__main__':
    import sys
    sys.exit(int(main() or 0))
