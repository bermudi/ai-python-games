import sys
import itertools

def get_prime_factors(n):
    """Returns a sorted list of unique prime factors of n."""
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return sorted(list(factors))

def merge_ranges(ranges):
    """Merges overlapping or adjacent ranges."""
    if not ranges:
        return []
    # Sort by start
    ranges.sort(key=lambda x: x[0])
    merged = []
    current_start, current_end = ranges[0]
    
    for i in range(1, len(ranges)):
        next_start, next_end = ranges[i]
        # Merge if they overlap or are adjacent (e.g. 1-2, 3-4 -> 1-4)
        if next_start <= current_end + 1: 
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end
    merged.append((current_start, current_end))
    return merged

def solve_for_len(length, ranges):
    """Calculates sum of invalid IDs of a specific length within ranges."""
    # Find prime factors of length
    primes = get_prime_factors(length)
    if not primes:
        return 0
    
    total_sum = 0
    
    # Inclusion-Exclusion Principle
    # We want the sum of numbers that are periodic with repetition count k,
    # where k is a multiple of some prime factor of length.
    # We iterate through all combinations of prime factors to handle overlaps.
    for r in range(1, len(primes) + 1):
        for combo in itertools.combinations(primes, r):
            k = 1
            for p in combo:
                k *= p
            
            # Base block length L
            L = length // k
            
            # Multiplier M such that N = X * M
            # M = 100...0100...01... (k times)
            M = (10**length - 1) // (10**L - 1)
            
            # Bounds for X (must be an L-digit number)
            min_X_digits = 10**(L-1)
            max_X_digits = 10**L - 1
            
            term_sum = 0
            
            # Sum valid N in ranges
            for start, end in ranges:
                # Restrict range to numbers of current length
                r_min = max(start, 10**(length-1))
                r_max = min(end, 10**length - 1)
                
                if r_min > r_max:
                    continue
                
                # We need N = X * M to be in [r_min, r_max]
                # So X must be in [ceil(r_min/M), floor(r_max/M)]
                x_min = (r_min + M - 1) // M
                x_max = r_max // M
                
                # Intersect with valid L-digit bounds
                valid_x_min = max(x_min, min_X_digits)
                valid_x_max = min(x_max, max_X_digits)
                
                if valid_x_min <= valid_x_max:
                    # Sum of arithmetic progression: sum(X * M)
                    count = valid_x_max - valid_x_min + 1
                    sum_X = count * (valid_x_min + valid_x_max) // 2
                    sum_N = sum_X * M
                    term_sum += sum_N
            
            # Add or subtract based on size of set (Inclusion-Exclusion)
            if r % 2 == 1:
                total_sum += term_sum
            else:
                total_sum -= term_sum
                
    return total_sum

def main():
    try:
        with open('input.txt', 'r') as f:
            data = f.read().strip()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    ranges_raw = data.split(',')
    ranges = []
    for r in ranges_raw:
        if not r.strip(): continue
        s, e = map(int, r.strip().split('-'))
        ranges.append((s, e))
    
    # Merge ranges to handle overlaps correctly
    ranges = merge_ranges(ranges)
    
    if not ranges:
        print(0)
        return

    # Determine min and max length to check
    min_val = min(r[0] for r in ranges)
    max_val = max(r[1] for r in ranges)
    
    min_len = len(str(min_val))
    max_len = len(str(max_val))
    
    grand_total = 0
    for length in range(min_len, max_len + 1):
        grand_total += solve_for_len(length, ranges)
        
    print(grand_total)

if __name__ == '__main__':
    main()
