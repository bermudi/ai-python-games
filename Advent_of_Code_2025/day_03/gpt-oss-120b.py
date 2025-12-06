#!/usr/bin/env python3
"""
Puzzle: 2020‑Advent‑of‑Code – Day 10 variant.
Find, for each line of digits, the largest two‑digit number obtainable by
choosing two positions i < j and concatenating the digits.
Sum those maxima over all lines.

Usage:
    python3 solve.py          # reads input.txt in the same directory
"""

import sys
from pathlib import Path

def max_two_digit(line: str) -> int:
    """
    Return the maximum two‑digit number that can be formed from the digits
    of `line` while preserving order.
    """
    max_left = -1   # largest digit seen so far (candidate for the tens place)
    best = -1       # best two‑digit value found

    for ch in line.strip():
        digit = ord(ch) - 48          # faster than int(ch) but same effect
        if max_left != -1:            # we already have a possible tens digit
            cand = 10 * max_left + digit
            if cand > best:
                best = cand
        if digit > max_left:
            max_left = digit
    # By problem statement each line contains at least two digits,
    # so `best` will be set.
    return best

def main():
    input_path = Path("input.txt")
    if not input_path.is_file():
        sys.stderr.write("Error: input.txt not found in the current directory.\n")
        sys.exit(1)

    total = 0
    with input_path.open("r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:               # skip empty lines
                continue
            total += max_two_digit(line)

    print(total)

if __name__ == "__main__":
    main()