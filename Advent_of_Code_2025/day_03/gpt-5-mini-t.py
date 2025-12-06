#!/usr/bin/env python3
"""
Read input from input.txt (or a file path given as first argument).
Each non-empty line is a bank: a string of digits. From each bank choose
exactly two digits (keeping their order) to form a two-digit number;
take the maximum such number for that bank and sum them all. Print the sum.
"""

import sys
from pathlib import Path

def max_two_digit_from_line(s: str) -> int:
    if len(s) < 2:
        raise ValueError("Each bank must contain at least two digits.")
    maxv = -1
    # use ord to avoid repeated int() conversions
    for i in range(len(s) - 1):
        di = ord(s[i]) - 48
        for j in range(i + 1, len(s)):
            val = di * 10 + (ord(s[j]) - 48)
            if val > maxv:
                maxv = val
                if maxv == 99:  # early exit: cannot beat 99
                    return 99
    return maxv

def main(path: str = "input.txt") -> int:
    p = Path(path)
    if not p.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2

    total = 0
    with p.open("r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            if not line.isdigit():
                raise ValueError(f"Invalid characters on line {lineno}: {line!r}")
            total += max_two_digit_from_line(line)

    print(total)
    return 0

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    sys.exit(main(filename))