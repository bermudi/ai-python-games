def max_joltage(bank):
    n = len(bank)
    if n < 2:
        return 0
    # Compute max_suffix[i] = max(bank[i..n-1])
    max_suffix = [0] * n
    max_suffix[n-1] = int(bank[n-1])
    for i in range(n-2, -1, -1):
        max_suffix[i] = max(max_suffix[i+1], int(bank[i]))
    # Now find the max joltage
    max_val = 0
    for i in range(n-1):
        val = int(bank[i]) * 10 + max_suffix[i+1]
        if val > max_val:
            max_val = val
    return max_val

def main():
    total = 0
    with open('input.txt', 'r') as f:
        for line in f:
            bank = line.strip()
            if bank:
                total += max_joltage(bank)
    print(total)

if __name__ == "__main__":
    main()