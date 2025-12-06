def sum_invalid_ids(input_str):
    # Parse the input ranges
    ranges = []
    for range_str in input_str.strip().split(','):
        if range_str:
            start, end = map(int, range_str.split('-'))
            ranges.append((start, end))
    
    total_sum = 0
    
    for start, end in ranges:
        # For each possible half-length k
        max_digits = len(str(end))
        
        for k in range(1, max_digits // 2 + 1):
            multiplier = 10 ** k + 1
            
            # n must have exactly k digits (no leading zeros)
            min_n = 10 ** (k - 1)
            max_n = 10 ** k - 1
            
            # The generated number is n * multiplier
            # We need start <= n * multiplier <= end
            
            # Find n_min such that n_min * multiplier >= start
            n_min = max(min_n, (start + multiplier - 1) // multiplier)  # ceiling division
            
            # Find n_max such that n_max * multiplier <= end
            n_max = min(max_n, end // multiplier)  # floor division
            
            # If there are valid n values
            if n_min <= n_max:
                # Sum of arithmetic series: n * multiplier for n from n_min to n_max
                count = n_max - n_min + 1
                total_sum += multiplier * (n_min + n_max) * count // 2
    
    return total_sum

# Test with the example
example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
print(f"Example result: {sum_invalid_ids(example)}")

# Read from input.txt
with open('input.txt', 'r') as f:
    input_data = f.read().strip()

print(f"Actual result: {sum_invalid_ids(input_data)}")