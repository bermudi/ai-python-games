import sys
import os

K = 12                     # number of batteries to turn on


def max_subsequence_of_length_k(s: str, k: int) -> str:
    """
    Return the lexicographically largest subsequence of s with length k.
    Assumes len(s) >= k.
    """
    n = len(s)
    stack = []                     # will hold the answer characters
    for i, ch in enumerate(s):
        # try to replace smaller previous characters by the larger current one
        while stack and stack[-1] < ch and (len(stack) - 1 + (n - i)) >= k:
            stack.pop()
        if len(stack) < k:
            stack.append(ch)
    # stack now contains exactly k characters
    return ''.join(stack)


def solve() -> None:
    """
    Reads the puzzle input from 'input.txt', computes the total maximal
    joltage (12‑digit number per bank) and prints it.
    """
    lines = []
    if os.path.exists("input.txt"):
        with open("input.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    else:
        lines = sys.stdin.read().splitlines()

    total = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        # keep only digit characters (the problem guarantees digits 1‑9)
        digits = ''.join(ch for ch in line if ch.isdigit())

        if len(digits) < K:
            # According to the statement this never happens.
            # If it does, the bank cannot produce a 12‑digit number;
            # we simply ignore it (or raise an error).
            continue

        best_12 = max_subsequence_of_length_k(digits, K)
        total += int(best_12)      # Python int is arbitrary precision

    print(total)


if __name__ == "__main__":
    solve()