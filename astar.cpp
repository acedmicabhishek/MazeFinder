#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>
#include <unordered_set>

using namespace std;

struct Node {
    int x, y;
    int g, h;
    Node* parent;

    Node(int x, int y, int g = 0, int h = 0, Node* p = nullptr)
        : x(x), y(y), g(g), h(h), parent(p) {}

    int f() const { return g + h; }

    bool operator>(const Node& other) const {
        return f() > other.f();
    }
};

int heuristic(int x1, int y1, int x2, int y2) {
    return abs(x1 - x2) + abs(y1 - y2); // Manhattan distance
}

bool isValid(int x, int y, const vector<vector<int>>& grid) {
    return x >= 0 && y >= 0 && x < grid.size() && y < grid[0].size()
           && grid[x][y] == 0;
}

vector<pair<int, int>> astar(const vector<vector<int>>& grid,
                              pair<int, int> start,
                              pair<int, int> goal) {
    int rows = grid.size(), cols = grid[0].size();
    auto cmp = [](Node* a, Node* b) { return *a > *b; };
    priority_queue<Node*, vector<Node*>, decltype(cmp)> open(cmp);
    vector<vector<bool>> closed(rows, vector<bool>(cols, false));

    Node* startNode = new Node(start.first, start.second);
    startNode->h = heuristic(start.first, start.second, goal.first, goal.second);
    open.push(startNode);

    while (!open.empty()) {
        Node* current = open.top();
        open.pop();

        int x = current->x, y = current->y;
        if (closed[x][y]) continue;
        closed[x][y] = true;

        if (x == goal.first && y == goal.second) {
            vector<pair<int, int>> path;
            while (current) {
                path.push_back({current->x, current->y});
                current = current->parent;
            }
            reverse(path.begin(), path.end());
            return path;
        }

        for (auto [dx, dy] : vector<pair<int, int>>{{0,1},{1,0},{0,-1},{-1,0}}) {
            int nx = x + dx, ny = y + dy;
            if (isValid(nx, ny, grid) && !closed[nx][ny]) {
                int g = current->g + 1;
                int h = heuristic(nx, ny, goal.first, goal.second);
                Node* neighbor = new Node(nx, ny, g, h, current);
                open.push(neighbor);
            }
        }
    }

    return {}; // No path found
}

int main() {
    vector<vector<int>> grid = {
        {0, 0, 0, 0},
        {1, 1, 0, 1},
        {0, 0, 0, 0},
        {0, 1, 1, 0}
    };

    pair<int, int> start = {0, 0};
    pair<int, int> goal = {3, 3};

    vector<pair<int, int>> path = astar(grid, start, goal);

    if (path.empty()) {
        cout << "No path found\n";
    } else {
        for (auto [x, y] : path)
            cout << "(" << x << "," << y << ") ";
        cout << "\n";
    }

    return 0;
}
