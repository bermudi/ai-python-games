# Read input
with open("input.txt") as f:
    line = f.read().strip()

# Parse ranges
ranges = []
for part in line.split(','):
    a, b = map(int, part.split('-'))
    ranges.append((a, b))

# Function to check if a number is in any range
def in_ranges(n, ranges):
    for a, b in ranges:
        if a <= n <= b:
            return True
    return False

# Collect all invalid IDs
invalid_ids = set()

# Generate all possible invalid IDs (xx) up to a safe limit
# Try base numbers from 1-digit to 5-digit (since max ID is ~1e9)
for length in range(1, 6):
    start = 10**(length - 1)
    end = 10**length - 1
    for i in range(start, end + 1):
        s = str(i)
        # Skip if base number has leading zero (though it won't due to range)
        if s[0] == '0':
            continue
        candidate = s + s
        num = int(candidate)
        if in_ranges(num, ranges):
            invalid_ids.add(num)

# Sum and print result
print(sum(invalid_ids))