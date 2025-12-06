def main():
    total = 0
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            digits = [int(ch) for ch in line]
            n = len(digits)
            if n < 2:
                continue  # Should not happen, but skip if present
            max_so_far = digits[0]
            best = 0
            for j in range(1, n):
                candidate = 10 * max_so_far + digits[j]
                if candidate > best:
                    best = candidate
                if digits[j] > max_so_far:
                    max_so_far = digits[j]
            total += best
    print(total)

if __name__ == '__main__':
    main()