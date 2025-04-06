import heapq
from collections import deque

def solve():
    with open("Advent_of_Code_2019-day18/input.txt") as f:
        grid = [list(line.strip()) for line in f.readlines()]

    # Find all key and door positions, and the starting position
    start_pos = None
    keys = {}
    doors = {}
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            c = grid[y][x]
            if c == '@':
                start_pos = (x, y)
            elif c.islower():
                keys[c] = (x, y)
            elif c.isupper():
                doors[c] = (x, y)
    total_keys = len(keys)

    # Precompute distances between all pairs of keys (and start position)
    # Also note the doors that block the path

    # For each key/start, BFS to find reachable keys and required keys to pass doors
    def bfs(start):
        x, y = start
        visited = {}
        queue = deque()
        queue.append((x, y, 0, frozenset()))  # (x, y, steps, needed_keys)
        visited[(x, y)] = (0, frozenset())
        reachable = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            cx, cy, steps, needed = queue.popleft()
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]):
                    cell = grid[ny][nx]
                    if cell == '#':
                        continue
                    new_needed = set(needed)
                    if cell.isupper():
                        new_needed.add(cell.lower())
                    if (nx, ny) not in visited or visited[(nx, ny)][0] > steps + 1:
                        visited[(nx, ny)] = (steps + 1, frozenset(new_needed))
                        if cell.islower() or cell == '@' or cell == '.':
                            pass  # continue exploring
                        queue.append((nx, ny, steps + 1, frozenset(new_needed)))
        # Now, collect reachable keys and their steps and required keys
        for key, pos in keys.items():
            if pos in visited:
                steps, needed = visited[pos]
                reachable[key] = (steps, needed)
        return reachable

    # Also include '@' as a pseudo-key for the start
    key_positions = {'@': start_pos}
    key_positions.update(keys)
    key_distances = {}
    for key1 in key_positions:
        pos1 = key_positions[key1]
        reachable = bfs(pos1)
        key_distances[key1] = {}
        for key2 in reachable:
            if key2 == key1:
                continue
            steps, needed = reachable[key2]
            key_distances[key1][key2] = (steps, needed)

    # Now perform Dijkstra's algorithm to find the minimal path collecting all keys
    # Priority queue elements: (steps, current_key, collected_keys_bitmask)
    heap = []
    # The bitmask represents which keys are collected. Bit 0 is 'a', bit 1 is 'b', etc.
    initial_bitmask = 0
    heapq.heappush(heap, (0, '@', initial_bitmask))
    visited = {}
    # The visited dictionary keeps track of the minimal steps to reach (current_key, bitmask)
    visited[('@', initial_bitmask)] = 0
    all_keys_mask = (1 << total_keys) - 1

    while heap:
        current_steps, current_key, bitmask = heapq.heappop(heap)
        if bitmask == all_keys_mask:
            return current_steps
        if visited.get((current_key, bitmask), float('inf')) < current_steps:
            continue
        # Explore all adjacent keys
        for next_key in key_distances[current_key]:
            if next_key == current_key:
                continue
            steps, needed_keys = key_distances[current_key][next_key]
            # Check if we have all needed keys to pass the doors
            can_pass = True
            for needed_key in needed_keys:
                if not (bitmask & (1 << (ord(needed_key) - ord('a')))):
                    can_pass = False
                    break
            if not can_pass:
                continue
            # Compute new bitmask if next_key is a key (not '@')
            new_bitmask = bitmask
            if next_key != '@':
                key_index = ord(next_key) - ord('a')
                new_bitmask |= (1 << key_index)
            new_steps = current_steps + steps
            if (next_key, new_bitmask) not in visited or new_steps < visited.get((next_key, new_bitmask), float('inf')):
                visited[(next_key, new_bitmask)] = new_steps
                heapq.heappush(heap, (new_steps, next_key, new_bitmask))
    return -1

print(solve())
