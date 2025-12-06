import sys

def parse_input():
    """
    Reads the whole input file `input.txt`.  If the file does not exist,
    falls back to standard input.
    Returns a list of (low, high) integer ranges.
    """
    try:
        with open('input.txt') as f:
            raw = f.read()
    except FileNotFoundError:
        raw = sys.stdin.read()

    # Remove all whitespace – the data may be wrapped for readability.
    raw = ''.join(raw.split())
    # Remove a possible trailing comma.
    if raw.endswith(','):
        raw = raw[:-1]

    parts = raw.split(',') if raw else []
    ranges = []
    for part in parts:
        if not part:
            continue
        if '-' not in part:
            continue          # ignore malformed entries (should not happen)
        lo, hi = part.split('-')
        ranges.append((int(lo), int(hi)))
    return ranges


def ceil_div(a: int, b: int) -> int:
    """Return ceil(a / b) for positive integers."""
    return -((-a) // b)


def sum_invalid_in_range(lo: int, hi: int) -> int:
    """Sum of all invalid ids inside [lo, hi]."""
    total = 0
    k = 1
    while True:
        pow10k = 10 ** k          # 10^k
        pow10km1 = 10 ** (k - 1)  # 10^(k-1)

        base = pow10k + 1         # 10^k + 1
        # Smallest possible id for this k
        min_id = pow10km1 * base
        if min_id > hi:
            break                 # larger k cannot contribute

        # Bounds for the half‑part s
        s_low = max(pow10km1, ceil_div(lo, base))
        s_high = min(pow10k - 1, hi // base)

        if s_low <= s_high:
            cnt = s_high - s_low + 1
            # sum of consecutive integers from s_low to s_high
            sum_s = (s_low + s_high) * cnt // 2
            total += sum_s * base

        k += 1
    return total


def solve() -> None:
    ranges = parse_input()
    answer = 0
    for lo, hi in ranges:
        answer += sum_invalid_in_range(lo, hi)
    print(answer)


if __name__ == "__main__":
    solve()