#!/usr/bin/env python3
"""
Sum all "invalid" product IDs from ranges in input.txt.
An "invalid" ID is any positive integer equal to some digit-sequence s repeated twice (s concatenated with s),
with no leading zeros (so s must have exactly L digits and s >= 10^(L-1)).
"""

import sys
from pathlib import Path

def main():
    p = Path("input.txt")
    if not p.exists():
        print("Error: input.txt not found in current directory.", file=sys.stderr)
        sys.exit(1)

    data = p.read_text().strip()
    # allow ranges to be split across lines in the file; remove whitespace/newlines between tokens
    data = data.replace("\n", "").replace("\r", "")
    if not data:
        print("Error: input.txt is empty.", file=sys.stderr)
        sys.exit(1)

    ranges = []
    for token in data.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" not in token:
            print(f"Warning: skipping malformed token: {token!r}", file=sys.stderr)
            continue
        a, b = token.split("-", 1)
        lo = int(a)
        hi = int(b)
        if lo > hi:
            lo, hi = hi, lo
        ranges.append((lo, hi))

    if not ranges:
        print("0")
        return

    max_hi = max(hi for _, hi in ranges)
    max_len = len(str(max_hi))
    # maximum half-length L to consider
    max_L = max_len // 2

    invalid_ids = set()

    for lo, hi in ranges:
        # For each half-length L, compute s range that yields N = s*(10^L + 1) in [lo, hi]
        for L in range(1, max_L + 1):
            base = 10 ** L
            denom = base + 1  # N = s * denom

            # s must have exactly L digits (no leading zero)
            s_min_len = 10 ** (L - 1)
            s_max_len = 10 ** L - 1

            # s must also satisfy lo <= s*denom <= hi
            # so s >= ceil(lo / denom), s <= floor(hi / denom)
            s_min_range = (lo + denom - 1) // denom  # ceil division
            s_max_range = hi // denom

            s_low = max(s_min_len, s_min_range)
            s_high = min(s_max_len, s_max_range)
            if s_low > s_high:
                continue

            # add all N = s * denom for s in [s_low, s_high]
            for s in range(s_low, s_high + 1):
                invalid_ids.add(s * denom)

    total = sum(invalid_ids)
    print(total)

if __name__ == "__main__":
    main()