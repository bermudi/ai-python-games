import heapq
import collections
import sys

# Set higher recursion depth if needed, although BFS is iterative.
# sys.setrecursionlimit(2000) 

# Cache for BFS distances results.
# Key format: ( (start_row, start_col), (end_row, end_col), mask )
# Value: distance (int) or float('inf') if unreachable
bfs_cache = {}

# BFS function to find the shortest path distance between two points on the grid,
# considering the current set of keys (`mask`) to determine which doors are passable.
def bfs_distance(grid, H, W, start_pos, end_pos, mask, key_to_idx):
    """
    Calculates the shortest distance between start_pos and end_pos using BFS.
    Takes into account walls ('#') and locked doors ('A'-'Z').
    Doors are passable only if the corresponding key is present in the `mask`.
    Results are cached in `bfs_cache`.
    """
    cache_key = (start_pos, end_pos, mask)
    # Return cached result if available
    if cache_key in bfs_cache:
        return bfs_cache[cache_key]

    # Initialize BFS queue with starting position and distance 0
    q = collections.deque([(start_pos, 0)])
    # Keep track of visited grid cells for this specific BFS search
    visited = {start_pos}

    while q:
        (r, c), dist = q.popleft()

        # Check if we reached the target position
        if (r, c) == end_pos:
            bfs_cache[cache_key] = dist  # Cache the result
            return dist

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if not (0 <= nr < H and 0 <= nc < W):
                continue
            
            # Check if the neighbor has already been visited in this BFS run
            if (nr, nc) in visited:
                continue

            cell = grid[nr][nc]

            # Check for walls
            if cell == '#':
                continue

            # Check for doors
            if 'A' <= cell <= 'Z':
                req_key = cell.lower()
                # Check if the corresponding key character exists in our key map
                if req_key in key_to_idx:
                     req_key_idx = key_to_idx[req_key]
                     # Check if the required key bit is set in the mask
                     if not (mask & (1 << req_key_idx)):
                         # Door is locked, cannot pass
                         continue
                else: 
                     # If a door exists but its key is not on the map, treat it as a wall.
                     continue

            # If the cell is passable ('.', '@', a key, or an open door)
            visited.add((nr, nc))
            q.append(((nr, nc), dist + 1))

    # If the queue becomes empty and the target was not reached, it's unreachable
    bfs_cache[cache_key] = float('inf') # Cache the unreachable result
    return float('inf')

# Main solver function using Dijkstra on a state graph representing key collection progress.
# This approach models the problem like a variation of the Traveling Salesperson Problem (TSP),
# where we need to visit all key locations.
def solve_grid_tsp_like(grid_str):
    """
    Solves the key collection puzzle using Dijkstra's algorithm on a state space.
    State: (current_location_POI_index, collected_keys_mask)
    Transitions involve moving from the current location to an uncollected key's location.
    The cost of a transition is the BFS distance, considering currently held keys.
    """
    grid = grid_str.strip().split('\n')
    H = len(grid)
    W = len(grid[0])

    start_pos = None
    key_locs = {}
    keys_on_map = set()

    # Parse the grid to find the start position '@', key locations ('a'-'z'),
    # and build the set of all unique keys present on the map.
    for r in range(H):
        for c in range(W):
            char = grid[r][c]
            if 'a' <= char <= 'z':
                key_locs[char] = (r, c)
                keys_on_map.add(char)
            elif char == '@':
                start_pos = (r, c)

    num_keys = len(keys_on_map)
    # Target mask represents having collected all keys.
    target_mask = (1 << num_keys) - 1
    
    # Create a mapping from key character to a unique bit index (0 to num_keys-1).
    # Sorting ensures consistent indexing.
    sorted_keys = sorted(list(keys_on_map))
    key_to_idx = {key: i for i, key in enumerate(sorted_keys)}

    # Define Points of Interest (POIs): the start position and all key locations.
    # Assign index 0 to the start position '@'.
    # Assign indices 1 to num_keys to the keys based on their sorted order.
    poi_locs = {0: start_pos}
    # Optional: Map POI index (1+) back to the key index (0+) for mask manipulation if needed later.
    # poi_idx_to_key_idx = {} 
    for key_char, key_idx in key_to_idx.items():
         poi_idx = key_idx + 1 
         poi_locs[poi_idx] = key_locs[key_char]
         # poi_idx_to_key_idx[poi_idx] = key_idx

    # Dijkstra state: (distance, current_poi_idx, mask)
    # `min_dist` stores the minimum distance found so far to reach a state (poi_idx, mask).
    min_dist = {}
    # Priority queue stores states to visit, ordered by distance.
    # Initial state: distance 0, at POI 0 (start position), with mask 0 (no keys collected).
    pq = [(0, 0, 0)] 
    min_dist[(0, 0)] = 0 

    # Clear the BFS cache before starting a new puzzle solve.
    bfs_cache.clear() 

    # Main Dijkstra loop
    while pq:
        # Pop the state with the smallest distance from the priority queue.
        dist, curr_poi_idx, mask = heapq.heappop(pq)
        
        # If we've already found a shorter path to this state, skip processing.
        if dist > min_dist.get((curr_poi_idx, mask), float('inf')):
             continue

        # Check if all keys have been collected (target mask reached).
        if mask == target_mask:
            # Because Dijkstra explores states in increasing order of distance,
            # the first time we reach the target mask, we have found the shortest path.
            return dist

        # Get the grid coordinates of the current POI.
        curr_pos = poi_locs[curr_poi_idx]

        # Explore possible transitions: move to collect any uncollected key.
        for next_key_idx in range(num_keys):
            # Check if the key corresponding to `next_key_idx` is NOT already collected.
            if not (mask & (1 << next_key_idx)):
                # Determine the POI index for this key.
                next_poi_idx = next_key_idx + 1
                # Get the grid coordinates of the key's location.
                next_pos = poi_locs[next_poi_idx]
                
                # Calculate the shortest path cost from the current position to the key's location.
                # This uses BFS and considers the current key `mask` for door access.
                path_cost = bfs_distance(grid, H, W, curr_pos, next_pos, mask, key_to_idx)

                # If the key is reachable (path_cost is not infinity)
                if path_cost != float('inf'):
                    # Calculate the total distance to the new state.
                    new_dist = dist + path_cost
                    # Create the new mask representing the state after collecting the key.
                    new_mask = mask | (1 << next_key_idx)
                    
                    # Define the new state key: (POI index of the collected key, new mask)
                    state_key = (next_poi_idx, new_mask)
                    
                    # Check if this path to `state_key` is shorter than any previously found path.
                    if new_dist < min_dist.get(state_key, float('inf')):
                        # Update the minimum distance to this state.
                        min_dist[state_key] = new_dist
                        # Add the new state to the priority queue for exploration.
                        heapq.heappush(pq, (new_dist, next_poi_idx, new_mask))

    # If the loop finishes without reaching the target mask, it means not all keys are reachable.
    return -1 


# Main execution block
if __name__ == '__main__':
    # Read the puzzle input from the 'input.txt' file.
    try:
        with open('Advent_of_Code_2019-day18/input.txt', 'r') as f:
            puzzle_input_str = f.read()
    except FileNotFoundError:
        print("Error: Input file 'input.txt' not found.")
        sys.exit(1)

    # Solve the puzzle using the TSP-like approach.
    print("Solving puzzle... This may take a while.")
    result = solve_grid_tsp_like(puzzle_input_str)
    
    # Print the final result.
    if result != -1:
        print(f"The shortest path to collect all keys takes {result} steps.")
    else:
        print("Could not find a path to collect all keys.")
