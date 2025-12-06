def max_subsequence(digits: str, k: int) -> str:
    """Return the largest number possible by choosing exactly k digits in order."""
    n = len(digits)
    to_remove = n - k
    stack = []
    for digit in digits:
        # While we can remove digits and current digit is larger than stack top
        while to_remove > 0 and stack and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)
    # If still need to remove, remove from the end
    while to_remove > 0:
        stack.pop()
        to_remove -= 1
    return ''.join(stack)

# Read input
with open("input.txt") as f:
    banks = [line.strip() for line in f if line.strip()]

total = 0
for bank in banks:
    best = max_subsequence(bank, 12)
    total += int(best)

print(total)