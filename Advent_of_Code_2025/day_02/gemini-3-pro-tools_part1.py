def solve():
    try:
        with open('input.txt', 'r') as f:
            data = f.read().strip()
    except FileNotFoundError:
        print("Error: 'input.txt' not found. Please ensure the file is in the same directory.")
        # For demonstration, we use the example from the prompt if file is missing
        print("Using example data from prompt...")
        data = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

    ranges = data.split(',')
    total_sum = 0
    
    for r in ranges:
        if not r.strip(): continue
        start_s, end_s = r.strip().split('-')
        start = int(start_s)
        end = int(end_s)
        
        len_start = len(start_s)
        len_end = len(end_s)
        
        # We need to find numbers N formed by repeating a sequence X (N = X concatenated with X)
        # such that start <= N <= end.
        # If X has length L, then N has length 2L.
        # N = X * (10^L + 1)
        
        # Iterate over possible lengths L for the half-sequence X
        # The total length 2L must be between len_start and len_end (roughly)
        min_L = (len_start + 1) // 2
        max_L = len_end // 2
        
        for L in range(min_L, max_L + 1):
            # X must be an L-digit number: [10^(L-1), 10^L - 1]
            lower_bound_X_digits = 10**(L-1)
            upper_bound_X_digits = 10**L - 1
            
            factor = 10**L + 1
            
            # Calculate the range of X values that produce N within [start, end]
            # start <= X * factor <= end
            # X >= ceil(start / factor)
            # X <= floor(end / factor)
            
            min_X_val = (start + factor - 1) // factor
            max_X_val = end // factor
            
            # Intersect the valid digit range with the target value range
            actual_min = max(lower_bound_X_digits, min_X_val)
            actual_max = min(upper_bound_X_digits, max_X_val)
            
            if actual_min <= actual_max:
                # Sum of arithmetic progression: sum(k * factor) for k in [min, max]
                # = factor * sum(k)
                count = actual_max - actual_min + 1
                sum_X = count * (actual_min + actual_max) // 2
                term_sum = sum_X * factor
                total_sum += term_sum

    print(f"Total sum of invalid IDs: {total_sum}")

if __name__ == '__main__':
    solve()