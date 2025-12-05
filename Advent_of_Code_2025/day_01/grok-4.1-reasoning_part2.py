def main():
    # Read input from input.txt
    with open('input.txt', 'r') as f:
        rotations = [line.strip() for line in f.readlines() if line.strip()]
    
    # Start at position 50
    position = 50
    zero_count = 0
    
    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # number of clicks
        
        if direction == 'R':
            # Count passes over 0 during RIGHT rotation
            r = (100 - position) % 100
            if r == 0:
                zero_count += distance // 100
            elif r <= distance:
                zero_count += (distance - r) // 100 + 1
            
            # Update position
            position = (position + distance) % 100
            
        else:  # 'L'
            # Count passes over 0 during LEFT rotation
            s = position % 100
            if s == 0:
                zero_count += distance // 100
            elif s <= distance:
                zero_count += (distance - s) // 100 + 1
            
            # Update position
            position = (position - distance) % 100
    
    print(zero_count)

if __name__ == "__main__":
    main()