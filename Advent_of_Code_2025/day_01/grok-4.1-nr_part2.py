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
            # Right: count how many times we pass 0 going from current pos to (pos+distance)%100
            if position < 100:
                # From position to 99, then full circles, then remainder
                to_end = 100 - position
                full_circles = distance // 100
                remainder = distance % 100
                
                # Does the final position land on 0?
                final_pos = (position + distance) % 100
                if final_pos == 0:
                    zero_count += 1
                
                # Count passes through 0 during rotation
                zero_count += full_circles  # each full circle passes 0 once
                if remainder >= to_end and to_end > 0:
                    zero_count += 1  # pass 0 in first partial circle
                
            position = (position + distance) % 100
            
        else:  # 'L'
            # Left: count how many times we pass 0 going from current pos to (pos-distance)%100
            if position > 0:
                # From position to 0, then full circles, then remainder
                to_zero = position
                full_circles = distance // 100
                remainder = distance % 100
                
                # Does the final position land on 0?
                final_pos = (position - distance) % 100
                if final_pos == 0:
                    zero_count += 1
                
                # Count passes through 0 during rotation  
                zero_count += full_circles  # each full circle passes 0 once
                if remainder >= to_zero and to_zero > 0:
                    zero_count += 1  # pass 0 in first partial circle
            
            position = (position - distance) % 100
    
    print(zero_count)

if __name__ == "__main__":
    main()