import random
from collections import deque

Grid = list[list[dict[str, bool]]]


def create_grid(width: int, height: int) -> Grid:
    grid = []

    y = 0
    while y < height:
        line = []
        x = 0
        while x < width:
            cell = {"N": True, "E": True, "S": True, "W": True}
            line.append(cell)
            x += 1
        grid.append(line)
        y += 1
    return grid


def remove_wall(grid: Grid, a: tuple[int, int], b: tuple[int, int]) -> None:
    xa, ya = a
    xb, yb = b

    if xb == xa + 1:
        grid[ya][xa]["E"] = False
        grid[yb][xb]["W"] = False
    if xb == xa - 1:
        grid[ya][xa]["W"] = False
        grid[yb][xb]["E"] = False
    if yb == ya + 1:
        grid[ya][xa]["S"] = False
        grid[yb][xb]["N"] = False
    if yb == ya - 1:
        grid[ya][xa]["N"] = False
        grid[yb][xb]["S"] = False


def get_unvisited_cells(
        grid: Grid, x: int, y: int,
        visited: set[tuple[int, int]]) -> list[tuple[int, int]]:
    '''Return list of unvisited neighbors cells'''
    unvisited = []

    if y - 1 >= 0 and (x, y - 1) not in visited:
        unvisited.append((x, y - 1))
    if y + 1 < len(grid) and (x, y + 1) not in visited:
        unvisited.append((x, y + 1))
    if x - 1 >= 0 and (x - 1, y) not in visited:
        unvisited.append((x - 1, y))
    if x + 1 < len(grid[0]) and (x + 1, y) not in visited:
        unvisited.append((x + 1, y))

    return unvisited


def generate_maze(width: int, height: int) -> Grid:
    '''Dig the maze inside the grid'''
    grid = create_grid(width, height)
    visited = {(0, 0)}
    stack = [(0, 0)]

    if width >= 4 and height >= 5:
        y = (height - 3) // 2
        x = (width - 2) // 2
        pattern = [(x, y), (x + 1, y), (x, y + 1), (x, y + 2), (x + 1, y + 2)]
        visited.update(pattern)
    else:
        print("Build a greater maze if you want to have a pattern in center")

    while stack:
        current = stack[-1]
        x, y = current

        next_potential = get_unvisited_cells(grid, x, y, visited)

        if not next_potential:
            stack.pop()

        else:
            next_cell = random.choice(next_potential)
            remove_wall(grid, current, next_cell)
            stack.append(next_cell)
            visited.add(next_cell)

    return grid


def get_accessible_cells(grid: Grid, x: int, y: int) -> list[tuple[int, int]]:
    access_ok = []

    if not grid[y][x]["N"] and y - 1 >= 0:
        access_ok.append((x, y - 1))
    if not grid[y][x]["E"] and x + 1 < len(grid[0]):
        access_ok.append((x + 1, y))
    if not grid[y][x]["S"] and y + 1 < len(grid):
        access_ok.append((x, y + 1))
    if not grid[y][x]["W"] and x - 1 >= 0:
        access_ok.append((x - 1, y))

    return access_ok


def breadth_first_search(grid: Grid, entry: tuple[int, int],
                         exit: tuple[int, int]) -> dict[tuple[int, int],
                                                        tuple[int, int]]:
    '''Explore the maze in breadth-first order until the exit is reached.'''
    queue = deque([entry])
    visited = {entry}
    came_from = {}
    bfs = {}

    while queue:
        current = queue.popleft()
        x, y = current

        if current == exit:
            while current != entry:
                bfs[current] = came_from[current]
                current = came_from[current]

        else:
            neighbors = get_accessible_cells(grid, x, y)
            for c in neighbors:
                if c not in visited:
                    visited.add(c)
                    queue.append(c)
                    came_from[c] = current

    return bfs


def shortest_path(bfs: dict[tuple[int, int], tuple[int, int]],
                  entry: tuple[int, int], exit: tuple[int, int]) -> str:
    '''Reconstruct the shortest path from the bfs dictionary'''
    current = exit
    path = [(exit)]
    directions = []

    while current != entry:
        previous_cell = bfs[current]
        path.append(previous_cell)

        x, y = previous_cell
        X, Y = current
        if X > x:
            directions.append("E")
        if X < x:
            directions.append("W")
        if Y > y:
            directions.append("S")
        if Y < y:
            directions.append("N")

        current = previous_cell
    directions.reverse()

    return "".join(directions)


if __name__ == "__main__":
    maze = generate_maze(7, 7)
    result = breadth_first_search(maze, (0, 0), (6, 0))
    print("Solution:", shortest_path(result, (0, 0), (6, 0)))
