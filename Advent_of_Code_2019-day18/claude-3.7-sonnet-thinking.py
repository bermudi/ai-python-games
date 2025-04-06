from collections import deque
import heapq

def shortest_path_to_collect_all_keys(maze_lines):
    # Parse the maze
    maze = [list(line) for line in maze_lines]
    start_pos = None
    keys = {}
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            cell = maze[i][j]
            if cell == '@':
                start_pos = (i, j)
            elif 'a' <= cell <= 'z':
                keys[cell] = (i, j)
    
    # Compute shortest paths between points of interest
    distances, doors_needed = compute_shortest_paths(maze, start_pos, keys)
    
    # Dijkstra's algorithm to find the shortest path to collect all keys
    total_keys = len(keys)
    heap = [(0, '@', frozenset())]  # (total_distance, current_position, keys_collected)
    visited = set()
    
    while heap:
        total_dist, pos, keys_collected = heapq.heappop(heap)
        
        # If we've collected all keys, return the distance
        if len(keys_collected) == total_keys:
            return total_dist
        
        # Skip if we've already visited this state
        state = (pos, keys_collected)
        if state in visited:
            continue
        visited.add(state)
        
        # Try to collect each remaining key
        for key in keys:
            if key not in keys_collected and key in distances[pos]:
                # Skip if the path to this key is blocked by doors
                if any(door not in keys_collected for door in doors_needed[pos][key]):
                    continue
                
                # Add to the heap
                new_keys = keys_collected.union({key})
                new_dist = total_dist + distances[pos][key]
                heapq.heappush(heap, (new_dist, key, new_keys))
    
    return -1  # If no path is found

def compute_shortest_paths(maze, start_pos, keys):
    # Compute distances and doors between start and keys, and between keys
    distances = {}
    doors_needed = {}
    
    # Add start position with label '@'
    points = {'@': start_pos}
    points.update(keys)
    
    # Create a mapping from positions to labels
    pos_to_label = {pos: label for label, pos in points.items()}
    
    for src, src_pos in points.items():
        distances[src] = {}
        doors_needed[src] = {}
        
        # BFS from src_pos
        queue = deque([(src_pos, 0, set())])
        visited = {src_pos}
        
        while queue:
            pos, dist, doors = queue.popleft()
            
            # If we found a point of interest, record the path
            if pos in pos_to_label and pos != src_pos:
                target = pos_to_label[pos]
                distances[src][target] = dist
                doors_needed[src][target] = doors
            
            # Try all four directions
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_r, new_c = pos[0] + dr, pos[1] + dc
                new_pos = (new_r, new_c)
                
                if 0 <= new_r < len(maze) and 0 <= new_c < len(maze[0]) and maze[new_r][new_c] != '#' and new_pos not in visited:
                    visited.add(new_pos)
                    
                    # Check if this position has a door
                    new_doors = doors.copy()
                    if 'A' <= maze[new_r][new_c] <= 'Z':
                        new_doors.add(maze[new_r][new_c].lower())
                    
                    queue.append((new_pos, dist + 1, new_doors))
    
    return distances, doors_needed

# Read the input from file
with open("Advent_of_Code_2019-day18/input.txt", "r") as f:
    input_lines = f.read().strip().split('\n')

# Find the shortest path
result = shortest_path_to_collect_all_keys(input_lines)
print(result)
