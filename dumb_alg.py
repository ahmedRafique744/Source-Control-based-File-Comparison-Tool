def backtrack(A, s, t):
    # we're doing this char by char, tracing back from bottom-right of the DP table
    i = len(t)
    j = len(s)
    changes = []

    while i > 0 and j > 0:
        if s[j - 1] == t[i - 1]:
            i -= 1  # match, move diagonally
            j -= 1
        elif A[i][j] == 3 + A[i - 1][j - 1]:
            changes.append(('replace', j - 1, i - 1, s[j - 1], t[i - 1]))  # replace char in s with one from t
            i -= 1
            j -= 1
        elif A[i][j] == 2 + A[i - 1][j]:
            changes.append(('insert', j, i - 1, t[i - 1]))  # insert char from t into s
            i -= 1
        elif A[i][j] == 2 + A[i][j - 1]:
            changes.append(('delete', j - 1, i, s[j - 1]))  # delete char from s
            j -= 1

    # left-over chars in t → insert them into s
    while i > 0:
        changes.append(('insert', 0, i - 1, t[i - 1]))
        i -= 1
    # left-over chars in s → delete them
    while j > 0:
        changes.append(('delete', j - 1, 0, s[j - 1]))
        j -= 1

    return changes[::-1]  # reverse it to report top-down


def edit_distance_cost(s, t):
    # get lengths of both strings
    n = len(s)
    m = len(t)
    
    # set up a DP table where A[i][j] is cost to convert s[0..j] to t[0..i]
    A = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # fill first row – need to insert to get from empty to s
    for i in range(n + 1):
        A[0][i] = 2 * i
    # fill first col – need to delete to get from t to empty
    for i in range(m + 1):
        A[i][0] = 2 * i

    # fill in the rest of the table with min cost ops
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[j - 1] == t[i - 1]:
                A[i][j] = A[i - 1][j - 1]  # chars match, no cost
            else:
                A[i][j] = min(
                    3 + A[i - 1][j - 1],  # replace cost
                    2 + A[i - 1][j],     # insert cost
                    2 + A[i][j - 1]      # delete cost
                )

    return A, s, t  # return the matrix and both strings


def read_file(path):
    # quick file read helper
    with open(path, 'r') as f:
        return f.read()


def format_changes(changes):
    # turn change tuples into readable lines
    output = []
    for change in changes:
        if change[0] == 'replace':
            output.append(f"Changed character '{change[3]}' at position {change[1]} to '{change[4]}'")
        elif change[0] == 'insert':
            output.append(f"Inserted character '{change[3]}' at position {change[1]}")
        elif change[0] == 'delete':
            output.append(f"Deleted character '{change[3]}' from position {change[1]}")
    return output


def compare_files(file1_path, file2_path):
    # load both files as full strings
    s = read_file(file1_path)
    t = read_file(file2_path)

    # get edit distance matrix and backtrace changes
    A, s, t = edit_distance_cost(s, t)
    changes = backtrack(A, s, t)

    # format changes into readable lines
    formatted = format_changes(changes)

    # write them to output file
    with open('sampleOutput.txt', 'w') as out:
        for line in formatted:
            out.write(line + '\n')


# Example usage
if __name__ == '__main__':
    # call the function with the two file paths
    compare_files('fib1.py', 'fib2.py')
