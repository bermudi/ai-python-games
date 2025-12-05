def solve():
    """
    Solve Day 1 Part 2: Count the number of times the dial points at 0
    during rotations, including both intermediate positions and final positions.
    
    The dial starts at 50 and rotates according to instructions in input.txt.
    """
    position = 50  # Starting position of the dial
    zero_count = 0  # Total count of times dial points to 0 during rotations
    
    def count_zeros_in_rotation(start, direction, distance):
        """
        Efficiently count how many times 0 is encountered during a rotation.
        
        For left rotation (L): we visit positions start-1, start-2, ..., start-distance
        These positions are 0 when (start - i) % 100 == 0, which means i ≡ start (mod 100)
        
        For right rotation (R): we visit positions start+1, start+2, ..., start+distance
        These positions are 0 when (start + i) % 100 == 0, which means i ≡ (100 - start) (mod 100)
        """
        if direction == 'L':
            # Find the first i (1 ≤ i ≤ distance) where (start - i) % 100 == 0
            # This occurs when i ≡ start (mod 100)
            first_i = start % 100
            if first_i == 0:
                first_i = 100  # Next occurrence is at i = 100
            
            if first_i > distance:
                return 0
            
            # Count: first_i, first_i+100, first_i+200, ... ≤ distance
            return 1 + (distance - first_i) // 100
            
        else:  # direction == 'R'
            # Find the first i (1 ≤ i ≤ distance) where (start + i) % 100 == 0
            # This occurs when i ≡ (100 - start) (mod 100)
            first_i = (100 - start) % 100
            if first_i == 0:
                first_i = 100  # Next occurrence is at i = 100
            
            if first_i > distance:
                return 0
            
            # Count: first_i, first_i+100, first_i+200, ... ≤ distance
            return 1 + (distance - first_i) // 100
    
    with open("input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            direction = line[0]
            distance = int(line[1:])
            
            # Count zeros during this rotation (including final position)
            zero_count += count_zeros_in_rotation(position, direction, distance)
            
            # Update position after completing the rotation
            if direction == 'L':
                position = (position - distance) % 100
            else:
                position = (position + distance) % 100
    
    print(zero_count)

if __name__ == "__main__":
    solve()
