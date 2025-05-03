import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y)
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_search(grid, start, end):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    end_node = Node(end)
    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)

        if current.position == end_node.position:
            # Reconstruct path
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        closed_set.add(current.position)

        # Explore neighbors
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:  # 4 directions
            neighbor_pos = (current.position[0] + dx, current.position[1] + dy)

            if (0 <= neighbor_pos[0] < len(grid) and
                0 <= neighbor_pos[1] < len(grid[0]) and
                grid[neighbor_pos[0]][neighbor_pos[1]] == 0 and
                neighbor_pos not in closed_set):

                neighbor = Node(neighbor_pos, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(neighbor_pos, end)
                neighbor.f = neighbor.g + neighbor.h

                if any(n.position == neighbor.position and n.f <= neighbor.f for n in open_list):
                    continue

                heapq.heappush(open_list, neighbor)

    return None  # No path found

# Example grid (0 = walkable, 1 = wall)
grid = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]

start = (0, 0)
end = (3, 3)
path = astar_search(grid, start, end)

print("Path:", path)
