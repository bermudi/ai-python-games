def max_joltage_12(bank, k=12):
    n = len(bank)
    if n < k:
        return 0
    stack = []
    for i, d in enumerate(bank):
        while stack and stack[-1] < d and len(stack) + (n - i - 1) >= k:
            stack.pop()
        stack.append(d)
    while len(stack) > k:
        stack.pop()
    num_str = ''.join(stack)
    return int(num_str)

def main():
    total = 0
    with open('input.txt', 'r') as f:
        for line in f:
            bank = line.strip()
            if bank:
                total += max_joltage_12(bank)
    print(total)

if __name__ == "__main__":
    main()