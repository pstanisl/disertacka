from __future__ import print_function


def lcs_mat(seq1, seq2):
    """Create LCS table (stored as matrix) with lengths of subsequences."""
    m = len(seq1)
    n = len(seq2)
    # Construct the matrix, of all zeroes.
    mat = [[0] * (n+1) for row in range(m+1)]
    # Populate the matrix, iteratively
    for row in xrange(1, m+1):
        for col in xrange(1, n+1):
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
    """Find all longest common subsequences."""
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
    """
    Get all longest common subsequences of two sequences.
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
