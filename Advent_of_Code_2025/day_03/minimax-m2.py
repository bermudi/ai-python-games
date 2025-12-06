import sys
import os

def max_two_digit_number(s: str) -> int:
    """
    Given a string s containing only digits '1'..'9',
    return the maximum two‑digit number that can be formed by
    picking two positions i < j: 10*digit[i] + digit[j].
    """
    # convert characters to integer digits
    digits = [int(ch) for ch in s]
    n = len(digits)
    if n < 2:
        # not enough batteries, but per problem statement this never happens
        return 0

    # suffix_max[i] = max digit among positions i .. n-1
    suffix_max = [0] * (n + 1)        # suffix_max[n] is a dummy zero
    for i in range(n - 1, -1, -1):
        suffix_max[i] = max(digits[i], suffix_max[i + 1])

    best = 0
    # consider every possible tens digit (except the last position)
    for i in range(n - 1):
        candidate = digits[i] * 10 + suffix_max[i + 1]
        if candidate > best:
            best = candidate
    return best


def solve() -> None:
    """
    Reads the puzzle input from "input.txt", computes the total
    output joltage and prints it.
    """
    # Try to open input.txt; fall back to stdin if not present.
    lines = []
    if os.path.exists("input.txt"):
        with open("input.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    else:
        lines = sys.stdin.read().splitlines()

    total = 0
    for raw in lines:
        # ignore completely empty lines
        line = raw.strip()
        if not line:
            continue

        # keep only digit characters (the problem guarantees only 1..9,
        # but this also removes any stray whitespace or separators)
        digits_only = "".join(ch for ch in line if ch.isdigit())
        total += max_two_digit_number(digits_only)

    print(total)


if __name__ == "__main__":
    solve()