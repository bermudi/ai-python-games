def process_rotations(input_file):
    # Initialize the dial at 50
    dial_position = 50
    # Initialize the count of times the dial points at 0
    count_zero = 0
    
    with open(input_file, 'r') as file:
        for line in file:
            # Extract the direction and distance from the line
            direction, distance = line.strip().split()
            distance = int(distance)
            
            # Calculate the new position of the dial
            if direction == 'L':
                dial_position = (dial_position - distance) % 100
            elif direction == 'R':
                dial_position = (dial_position + distance) % 100
            
            # Check if the dial points at 0
            if dial_position == 0:
                count_zero += 1
    
    return count_zero

# Call the function and print the result
password = process_rotations('input.txt')
print(password)
