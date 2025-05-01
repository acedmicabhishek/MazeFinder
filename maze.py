import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    """ Frontier for DFS (LIFO Stack) """
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        return self.frontier.pop()  # LIFO (DFS)

class QueueFrontier(StackFrontier):
    """ Frontier for BFS (FIFO Queue) """
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        return self.frontier.pop(0)  # FIFO (BFS)

class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")  # Wall
                elif (i, j) == self.start:
                    print("A", end="")  # Start
                elif (i, j) == self.goal:
                    print("B", end="")  # Goal
                elif solution is not None and (i, j) in solution:
                    print("*", end="")  # Solution path
                else:
                    print(" ", end="")  # Empty space
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self, algorithm="dfs"):
        """ Solves the maze using DFS (Stack) or BFS (Queue) """

        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None)

        if algorithm.lower() == "bfs":
            frontier = QueueFrontier()  # BFS uses Queue
        else:
            frontier = StackFrontier()  # DFS uses Stack

        frontier.add(start)
        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("No solution")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python maze.py maze.txt [dfs|bfs]")

    algorithm = sys.argv[2].lower()
    if algorithm not in ["dfs", "bfs"]:
        sys.exit("Error: Algorithm must be 'dfs' or 'bfs'")

    m = Maze(sys.argv[1])
    print("Maze:")
    m.print()
    print(f"Solving using {algorithm.upper()}...")
    m.solve(algorithm)
    print("Solved:")
    m.print()
