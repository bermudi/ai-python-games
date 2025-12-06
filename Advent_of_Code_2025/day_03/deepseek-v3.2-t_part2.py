def main():
    k = 12
    total = 0
    with open('input.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            digits = [int(ch) for ch in line]
            n = len(digits)
            if n < k:
                # Not enough digits to form a k-digit number
                continue
            to_remove = n - k
            stack = []
            for digit in digits:
                while stack and to_remove > 0 and stack[-1] < digit:
                    stack.pop()
                    to_remove -= 1
                stack.append(digit)
            # If stack is longer than k, take the first k digits
            if len(stack) > k:
                stack = stack[:k]
            # Form the number from the selected digits
            num = 0
            for d in stack:
                num = num * 10 + d
            total += num
    print(total)

if __name__ == '__main__':
    main()