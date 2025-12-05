# Read input
with open("input.txt") as f:
    line = f.read().strip()

# Parse ranges
ranges = []
for part in line.split(','):
    a, b = map(int, part.split('-'))
    ranges.append((a, b))

# Function to check if a number is invalid (repeated at least twice)
def is_invalid(n):
    s = str(n)
    length = len(s)
    for k in range(1, length // 2 + 1):
        if length % k == 0:
            part = s[:k]
            if part * (length // k) == s:
                return True
    return False

# Collect all invalid IDs
total = 0
for a, b in ranges:
    for n in range(a, b + 1):
        if is_invalid(n):
            total += n

# Print result
print(total)
