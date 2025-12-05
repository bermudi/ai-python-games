#!/usr/bin/env python3
"""
Sum all invalid product IDs from ranges in input.txt using the "repeat >= 2 times" rule.

An invalid ID is any positive integer equal to some digit-sequence s (no leading zeros)
repeated k times for some k >= 2. Example: 123123 (s=123, k=2), 1111111 (s=1, k=7).
"""
import sys
from pathlib import Path

def parse_ranges(text):
    text = text.replace("\n", "").replace("\r", "")
    tokens = [t.strip() for t in text.split(",") if t.strip()]
    ranges = []
    for tok in tokens:
        if "-" not in tok:
            raise ValueError(f"Malformed token (no dash): {tok!r}")
        a, b = tok.split("-", 1)
        lo = int(a)
        hi = int(b)
        if lo > hi:
            lo, hi = hi, lo
        ranges.append((lo, hi))
    return ranges

def merge_ranges(ranges):
    if not ranges:
        return []
    rs = sorted(ranges)
    merged = [list(rs[0])]
    for lo, hi in rs[1:]:
        if lo > merged[-1][1] + 1:
            merged.append([lo, hi])
        else:
            if hi > merged[-1][1]:
                merged[-1][1] = hi
    return [(a, b) for a, b in merged]

def sum_invalid_ids(ranges):
    if not ranges:
        return 0
    ranges = merge_ranges(ranges)
    max_hi = max(hi for _, hi in ranges)
    max_len = len(str(max_hi))
    max_L = max_len // 2  # half-block length must be <= max_len//2 because k>=2

    # Precompute powers of 10
    pow10 = [1] * (max_len + 1)
    for i in range(1, max_len + 1):
        pow10[i] = pow10[i - 1] * 10

    invalid = set()

    # For each block-length L and repeat-count k >= 2, compute the multiplier (denom)
    # N = s * denom, where s has exactly L digits (no leading zero), and denom = sum_{i=0..k-1} 10^{i*L}
    for L in range(1, max_L + 1):
        s_min_len = pow10[L - 1]
        s_max_len = pow10[L] - 1
        max_k = max_len // L
        for k in range(2, max_k + 1):
            denom = (pow10[L * k] - 1) // (pow10[L] - 1)  # integer
            # For each input range, find s interval that produces N in [lo, hi]
            for lo, hi in ranges:
                s_low = max(s_min_len, (lo + denom - 1) // denom)
                s_high = min(s_max_len, hi // denom)
                if s_low > s_high:
                    continue
                # Add all N = s * denom for s in [s_low, s_high]
                for s in range(s_low, s_high + 1):
                    invalid.add(s * denom)

    return sum(invalid)

def main():
    p = Path("input.txt")
    if not p.exists():
        print("Error: input.txt not found in current directory.", file=sys.stderr)
        sys.exit(1)
    text = p.read_text().strip()
    if not text:
        print("0")
        return
    ranges = parse_ranges(text)
    total = sum_invalid_ids(ranges)
    print(total)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = (
            "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
            "1698522-1698528,446443-446449,38593856-38593862,565653-565659,"
            "824824821-824824827,2121212118-2121212124"
        )
        ranges = parse_ranges(sample)
        result = sum_invalid_ids(ranges)
        print("sample result:", result, "(expected 4174379265)")
    else:
        main()