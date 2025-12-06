total = 0
with open('input.txt', 'r') as f:
    for line in f:
        s = line.strip()
        if not s:
            continue
        n = len(s)
        if n < 12:
            continue  # unlikely, but skip
        result = []
        pos = 0
        for step in range(12):
            remaining_after = 11 - step
            end = n - remaining_after - 1
            if end < pos:
                # impossible
                break
            max_d = -1
            best_i = -1
            for i in range(pos, end + 1):
                d = int(s[i])
                if d > max_d:
                    max_d = d
                    best_i = i
            result.append(s[best_i])
            pos = best_i + 1
        jolt = int(''.join(result))
        total += jolt
print(total)
