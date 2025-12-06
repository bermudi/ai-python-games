#!/usr/bin/env python3
"""
Advent of Code – Day X Part 2 (variant)

Task:
  For each line of digits in input.txt select exactly 12 digits (keeping order)
  to form the largest possible number.  Sum those numbers and output the total.

The solution uses the greedy monotonic‑stack algorithm described in the
explanation above.
"""

import sys
from pathlib import Path

K = 12                       # number of batteries to turn on per bank


def max_subseq_k(s: str, k: int) -> str:
    """
    Return the lexicographically largest subsequence of length k
    from the digit string s.
    """
    n = len(s)
    stack = []                # will contain characters

    for i, ch in enumerate(s):
        # While we can improve the stack by discarding a smaller digit
        while (stack and
               stack[-1] < ch and
               (len(stack) - 1 + (n - i)) >= k):
            stack.pop()

        # Take the current digit if we still need more characters
        if len(stack) < k:
            stack.append(ch)

    # stack length is exactly k (Lemma 3)
    return ''.join(stack)


def main() -> None:
    input_path = Path("input.txt")
    if not input_path.is_file():
        sys.stderr.write("Error: input.txt not found in the current directory.\n")
        sys.exit(1)

    total = 0
    with input_path.open() as f:
        for raw in f:
            line = raw.strip()
            if not line:                # skip blank lines
                continue
            subseq = max_subseq_k(line, K)
            total += int(subseq)        # Python supports arbitrary‑size ints

    print(total)


if __name__ == "__main__":
    main()