def edit_distance_cost(s, t):
    """Compute weighted edit‐distance DP table (insert/delete=2, replace=3)."""

    # get lengths of string s and string t to build 2D array
    n, m = len(s), len(t)

    # build (m+1)x(n+1) array for DP, where each cell is min cost to transform prefixes
    A = [[0]*(n+1) for _ in range(m+1)]

    # first row: cost of inserting all of s into empty t (so only inserts)
    for j in range(n+1):
        A[0][j] = 2*j
    # first column: cost of deleting all of t to match empty s
    for i in range(m+1):
        A[i][0] = 2*i

    # fill the rest of the DP table using weighted ops
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[j-1] == t[i-1]:
                A[i][j] = A[i-1][j-1]  # chars match, no cost
            else:
                A[i][j] = min(
                    3 + A[i-1][j-1],  # replace
                    2 + A[i-1][j],    # insert
                    2 + A[i][j-1],    # delete
                )
    return A, s, t


def backtrack(A, s, t):
    """Line‐ or character‐level backtrace."""
    i, j = len(t), len(s)
    changes = []
    # start from bottom-right of DP table and trace back changes
    while i > 0 and j > 0:
        if s[j-1] == t[i-1]:
            i, j = i-1, j-1  # match, move diagonally
        elif A[i][j] == 3 + A[i-1][j-1]:
            changes.append(('replace', j-1, i-1, s[j-1], t[i-1]))  # replace s with t
            i, j = i-1, j-1
        elif A[i][j] == 2 + A[i-1][j]:
            changes.append(('insert', j, i-1, t[i-1]))  # insert t[i-1] into s
            i -= 1
        else:
            changes.append(('delete', j-1, i, s[j-1]))  # delete s[j-1]
            j -= 1

    # if anything left in t, those are insertions
    while i > 0:
        changes.append(('insert', 0, i-1, t[i-1]))
        i -= 1
    # if anything left in s, those are deletions
    while j > 0:
        changes.append(('delete', j-1, 0, s[j-1]))
        j -= 1

    return changes[::-1]  # reverse to get top-down changes


def first_code_column(line):
    """Index of first non‐whitespace character, 1‐based."""
    for idx, ch in enumerate(line):
        if ch not in (' ', '\t'):
            return idx + 1
    return 1  # empty or all whitespace line


def format_change_log(op, old_i, new_i, old_line, new_line, log):
    # format the diff into a clear log with line/column numbers and old/new values
    old = old_line.rstrip('\n').rstrip()
    new = new_line.rstrip('\n').rstrip()

    if op == 'replace':
        old_col = first_code_column(old)
        new_col = first_code_column(new)
    elif op == 'delete':
        old_col = first_code_column(old)
    else:  # insert
        new_col = first_code_column(new)

    print("########################################", file=log)
    print({'replace': "Changed", 'insert': "Added", 'delete': "Deleted"}[op], file=log)

    if op in ('replace', 'delete'):
        print("----------------------------------------", file=log)
        print(old, file=log)
        print("----------------------------------------", file=log)
        if op == 'replace':
            print(f"at line {old_i+1} on column {old_col} in fib1.py to", file=log)
        else:
            print(f"at line {old_i+1} on column {old_col} in fib1.py", file=log)

    if op in ('replace', 'insert'):
        print("----------------------------------------", file=log)
        print(new, file=log)
        print("----------------------------------------", file=log)
        if op == 'replace':
            print(f"in line {new_i+1} column {new_col} in fib2.py", file=log)
        else:
            print(f"at line {new_i+1} on column {new_col} in fib2.py", file=log)

    print("########################################\n", file=log)


if __name__ == "__main__":

    # open both versions of the file to diff
    with open("fib1.py") as f1, open("fib2.py") as f2:
        lines1, lines2 = f1.readlines(), f2.readlines()

    # compute the edit distance and get the cost matrix
    A_lines, s_lines, t_lines = edit_distance_cost(lines1, lines2)
    # get the actual list of changes from backtracking
    line_changes = backtrack(A_lines, s_lines, t_lines)

    # for context we are just unpacking each line of line_changes
    # which is our line by line change outputted by backtracking
    # oi is old index, ni is new index, old_l and new_l self explanatory
    # depending on action we use old_l or new_l
    # if insert, old_l was nothing so empty string
    # if delete, new_l is nothing
    # replace -> new_l becomes our change

    with open("diff_outpust.txt", "w") as out:
        for change in line_changes:
            op = change[0]
            if op == 'replace':
                _, oi, ni, old_l, new_l = change
            elif op == 'insert':
                _, oi, ni, new_l = change
                old_l = ""
            else:  # delete
                _, oi, ni, old_l = change
                new_l = ""

            format_change_log(op, oi, ni, old_l, new_l, out)
