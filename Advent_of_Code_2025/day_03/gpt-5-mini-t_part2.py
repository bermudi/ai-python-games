#!/usr/bin/env python3
"""
Read input from input.txt (or a file path given as first argument).
Each non-empty line is a bank: a string of digits. From each bank choose
exactly K digits (keeping their order) to form a K-digit number;
take the maximum such number for that bank and sum them all. Print the sum.

Usage:
  python3 part2.py          # reads input.txt, uses K = 12
  python3 part2.py input.txt 12
"""
import sys
from pathlib import Path

def max_k_subsequence(s: str, k: int) -> str:
    n = len(s)
    if k < 0 or k > n:
        raise ValueError(f"Cannot select {k} digits from a string of length {n}.")
    to_remove = n - k
    stack = []
    for ch in s:
        # pop smaller digits while we still can remove digits
        while to_remove > 0 and stack and stack[-1] < ch:
            stack.pop()
            to_remove -= 1
        stack.append(ch)
    # if removals remain, drop from the end
    if to_remove > 0:
        stack = stack[:-to_remove]
    return ''.join(stack[:k])

def main(path: str = "input.txt", k: int = 12) -> int:
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
            if len(line) < k:
                raise ValueError(f"Line {lineno} is too short ({len(line)}) for k={k}.")
            max_digits = max_k_subsequence(line, k)
            total += int(max_digits)

    print(total)
    return 0

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    k_arg = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    sys.exit(main(filename, k_arg))