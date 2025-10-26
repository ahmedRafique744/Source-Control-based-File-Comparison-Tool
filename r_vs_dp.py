import time  
import sys  
sys.setrecursionlimit(10000)  # just in case recursion goes deep (esp when we are processing bigger strings)

# --- Recursive Implementation ---
def edit_distance_recursive(s, t):
    # base case: if s is empty, insert all of t (each insert = 2)
    if len(s) == 0:
        return 2 * len(t)
    # base case: if t is empty, delete all of s (each delete = 2)
    if len(t) == 0:
        return 2 * len(s)
    # if last chars match, move on with no cost
    if s[-1] == t[-1]:
        return edit_distance_recursive(s[:-1], t[:-1])
    else:
        # if last chars differ: try replace (3), delete (2), insert (2), pick min
        return min(
            3 + edit_distance_recursive(s[:-1], t[:-1]),  # replace
            2 + edit_distance_recursive(s[:-1], t),        # delete
            2 + edit_distance_recursive(s, t[:-1])         # insert
        )


def edit_distance_iterative(s, t):
    n = len(s)  # length of source
    m = len(t)  # length of target
    A = [[0 for _ in range(n + 1)] for _ in range(m + 1)]  # init DP table

    # fill first row – deleting from s to empty t
    for i in range(n + 1):
        A[0][i] = 2 * i
    # fill first col – inserting into empty s to make t
    for j in range(m + 1):
        A[j][0] = 2 * j

    # fill rest of the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if t[i - 1] == s[j - 1]:
                A[i][j] = A[i - 1][j - 1]  # match: no cost
            else:
                # take min cost of replace (3), insert (2), delete (2)
                A[i][j] = min(
                    3 + A[i - 1][j - 1],
                    2 + A[i - 1][j],
                    2 + A[i][j - 1]
                )
    return A[m][n]  # final result is in bottom-right corner


def benchmark(s, t):
    print(f"\nTesting strings of length {len(s)}")

    try:
        # run and time the recursive version
        start = time.time()
        rec_result = edit_distance_recursive(s, t)
        rec_time = time.time() - start
        print(f"Recursive result: {rec_result} in {rec_time:.5f} seconds")
    except RecursionError:
        # handles stack overflow for deep recursions
        print("Recursive: RecursionError (too deep)")

    # run and time the DP version
    start = time.time()
    dp_result = edit_distance_iterative(s, t)
    dp_time = time.time() - start
    print(f"Iterative DP result: {dp_result} in {dp_time:.5f} seconds")

if __name__ == '__main__':
    # try increasing sizes and compare both implementations
    for size in range(2, 13):  # Recursive gets slow >12
        s = "a" * size  # string of a's
        t = "b" * size  # string of b's
        benchmark(s, t)  # run both versions and compare time
