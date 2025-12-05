import sys
import bisect

# ------------------------------------------------------------
def parse_ranges():
    """
    Reads the whole file input.txt (or stdin) and returns a list of
    (low, high) integer intervals.
    """
    try:
        data = open('input.txt').read()
    except FileNotFoundError:
        data = sys.stdin.read()

    # remove all whitespace – the description may wrap the line
    data = ''.join(data.split())
    # strip a possible trailing comma
    if data.endswith(','):
        data = data[:-1]

    ranges = []
    for part in data.split(','):
        if not part:
            continue
        lo_s, hi_s = part.split('-')
        ranges.append((int(lo_s), int(hi_s)))
    return ranges


# ------------------------------------------------------------
def solve() -> None:
    ranges = parse_ranges()
    if not ranges:
        print(0)
        return

    # global upper bound
    max_b = max(hi for _, hi in ranges)
    max_len = len(str(max_b))

    # powers of ten up to max_len
    pow10 = [1] * (max_len + 1)
    for i in range(1, max_len + 1):
        pow10[i] = pow10[i - 1] * 10

    # --------------------------------------------------------
    # generate every integer that is a repetition of a block
    candidates = set()

    for L in range(2, max_len + 1):                # total length
        tenL = pow10[L]                           # 10**L
        for d in range(1, L // 2 + 1):            # block length
            if L % d != 0:
                continue
            ten_d = pow10[d]                      # 10**d
            # factor F(L,d) = (10**L - 1) / (10**d - 1)
            factor = (tenL - 1) // (ten_d - 1)

            p_start = pow10[d - 1]                # smallest d‑digit number
            # largest p that still keeps the product ≤ max_b
            p_end = min(pow10[d] - 1, max_b // factor)

            if p_start > p_end:
                continue

            for p in range(p_start, p_end + 1):
                candidates.add(p * factor)

    # --------------------------------------------------------
    # turn the set into a sorted list and build prefix sums
    cand = sorted(candidates)
    pref = [0] * (len(cand) + 1)
    for i, v in enumerate(cand, 1):
        pref[i] = pref[i - 1] + v

    # --------------------------------------------------------
    answer = 0
    for lo, hi in ranges:
        left = bisect.bisect_left(cand, lo)
        right = bisect.bisect_right(cand, hi)
        answer += pref[right] - pref[left]

    print(answer)


# ------------------------------------------------------------
if __name__ == '__main__':
    solve()
