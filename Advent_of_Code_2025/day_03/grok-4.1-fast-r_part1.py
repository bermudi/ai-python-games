total = 0
with open('input.txt', 'r') as f:
    for line in f:
        s = line.strip()
        if not s:
            continue
        n = len(s)
        if n < 2:
            continue
        max_after = [0] * n
        max_after[n-1] = 0  # not used
        for i in range(n-2, -1, -1):
            max_after[i] = max(int(s[i+1]), max_after[i+1])
        bank_max = 0
        for i in range(n-1):
            cand = 10 * int(s[i]) + max_after[i]
            if cand > bank_max:
                bank_max = cand
        total += bank_max
print(total)