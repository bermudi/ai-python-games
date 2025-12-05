def is_invalid_id(id_str):
    n = len(id_str)
    # Check all possible pattern lengths from 1 to n//2
    for pattern_len in range(1, n // 2 + 1):
        if n % pattern_len != 0:
            continue  # pattern must divide the length evenly
        pattern = id_str[:pattern_len]
        repetitions = n // pattern_len
        if repetitions >= 2 and pattern * repetitions == id_str:
            return True
    return False

def sum_invalid_ids(input_line):
    total_sum = 0
    
    # Split the input line by commas to get all ranges
    ranges = input_line.strip().split(',')
    
    for range_str in ranges:
        # Split the range by dash to get the start and end
        start, end = map(int, range_str.split('-'))
        
        # Iterate through all IDs in the range
        for id_num in range(start, end + 1):
            # Convert the ID to a string
            id_str = str(id_num)
            
            # Check if the ID is invalid
            if is_invalid_id(id_str):
                total_sum += id_num
    
    return total_sum

# Read the input
with open('input.txt', 'r') as f:
    input_line = f.readline().strip()

# Calculate the sum of invalid IDs
result = sum_invalid_ids(input_line)

# Print the result
print(result)