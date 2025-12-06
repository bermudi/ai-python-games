def main():
    # Read input from input.txt
    with open('input.txt', 'r') as f:
        rotations = [line.strip() for line in f.readlines()]
    
    # Start at position 50
    position = 50
    zero_count = 0
    
    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # number of clicks
        
        if direction == 'R':
            # Right: increase position (wrap around at 100)
            position = (position + distance) % 100
        else:  # 'L'
            # Left: decrease position (wrap around at 0)
            position = (position - distance) % 100
        
        # Check if we're at 0 after this rotation
        if position == 0:
            zero_count += 1
    
    print(zero_count)

if __name__ == "__main__":
    main()