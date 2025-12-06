def solve_battery_puzzle():
    total_output_joltage = 0
    
    try:
        with open('input.txt', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: 'input.txt' not found. Please ensure the file exists.")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Convert the line string into a list of integers
        batteries = [int(d) for d in line if d.isdigit()]
        
        # If a line has fewer than 2 batteries, we can't turn on two.
        if len(batteries) < 2:
            continue
            
        max_joltage_for_bank = 0
        
        # Iterate through possible first digits from 9 down to 1
        for d1 in range(9, 0, -1):
            if d1 in batteries:
                # Find the index of the first occurrence of d1
                first_idx = batteries.index(d1)
                
                # Get all batteries that appear after this d1
                suffix = batteries[first_idx + 1:]
                
                # If there are batteries remaining, pick the largest one as d2
                if suffix:
                    d2 = max(suffix)
                    max_joltage_for_bank = d1 * 10 + d2
                    
                    # Since we are checking d1 from largest to smallest, 
                    # the first valid pair we find is guaranteed to be the maximum.
                    break
        
        total_output_joltage += max_joltage_for_bank

    print(f"Total Output Joltage: {total_output_joltage}")

if __name__ == "__main__":
    solve_battery_puzzle()