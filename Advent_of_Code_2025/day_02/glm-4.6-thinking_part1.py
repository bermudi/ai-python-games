def is_invalid_id(id_str):
    # Check if the length is even
    if len(id_str) % 2 != 0:
        return False
    
    # Split the ID in the middle
    half_len = len(id_str) // 2
    first_half = id_str[:half_len]
    second_half = id_str[half_len:]
    
    # Check if the two halves are equal
    return first_half == second_half

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