from tests.fixtures import mock_2x2, mock_6x6


Grid = list[list[dict[str, bool]]]
WALL = "█"
EMPTY = " "
ENTRY = "E"
EXIT = "S"
PATH = "*"
PATTERN = "4"
RED = "\033[31m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
WHITE = "\033[37m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
PINK = "\033[95m"
GREEN = "\033[32m"
GREY = "\033[90m"
RESET = "\033[0m"

COLORS = [
    {"wall": WHITE, "path": BLUE, "entry": PURPLE, "exit": RED,
     "pattern": GREY},
    {"wall": BLUE, "path": WHITE, "entry": YELLOW, "exit": RED,
     "pattern": GREY},
    {"wall": GREEN, "path": PINK, "entry": WHITE, "exit": CYAN,
     "pattern": GREY},
]


def build_screen(grid: Grid) -> list[list[str]]:
    """Build the grid with walls everywhere and after dig the path"""
    total_col = 2 * len(grid[0]) + 1
    total_row = 2 * len(grid) + 1

    screen = [[WALL] * total_col for _ in range(total_row)]

    y = 0
    while y < len(grid):
        x = 0
        while x < len(grid[0]):
            Y = y * 2 + 1
            X = x * 2 + 1
            screen[Y][X] = EMPTY
            if not grid[y][x]["N"]:
                screen[Y - 1][X] = EMPTY
            if not grid[y][x]["E"]:
                screen[Y][X + 1] = EMPTY
            if not grid[y][x]["S"]:
                screen[Y + 1][X] = EMPTY
            if not grid[y][x]["W"]:
                screen[Y][X - 1] = EMPTY
            x += 1
        y += 1
    return screen


def pattern_cells(screen: list[list[str]],
                  pattern: list[tuple[int, int]]) -> None:
    """Mark the '42' pattern cells so they can be colored distinctly."""
    for row, col in pattern:
        Y = row * 2 + 1
        X = col * 2 + 1
        screen[Y][X] = PATTERN


def markers(screen: list[list[str]], entry_pos: tuple[int, int],
            exit_pos: tuple[int, int]) -> None:
    """Print markers of entry and exit in game"""
    x = entry_pos[0]
    y = entry_pos[1]
    Y = y * 2 + 1
    X = x * 2 + 1
    screen[Y][X] = ENTRY
    x = exit_pos[0]
    y = exit_pos[1]
    Y = y * 2 + 1
    X = x * 2 + 1
    screen[Y][X] = EXIT


def path(screen: list[list[str]], entry_pos: tuple[int, int],
         solution: str) -> None:
    """Print the path solution on the maze"""
    x = entry_pos[0]
    y = entry_pos[1]
    for d in solution:
        Y = y * 2 + 1
        X = x * 2 + 1
        if d == "N":
            screen[Y - 1][X] = PATH
            y = y - 1
        if d == "E":
            screen[Y][X + 1] = PATH
            x = x + 1
        if d == "S":
            screen[Y + 1][X] = PATH
            y = y + 1
        if d == "W":
            screen[Y][X - 1] = PATH
            x = x - 1
        screen[y * 2 + 1][x * 2 + 1] = PATH


def colorize(c: str, paint: dict[str, str]) -> str:
    """Colorize entry, exit and path"""
    color = {
        ENTRY: paint["entry"],
        EXIT: paint["exit"],
        PATH: paint["path"],
        WALL: paint["wall"],
        PATTERN: paint["pattern"],
    }
    if c in color:
        return color[c] + WALL * 2 + RESET
    return c * 2


def render(screen: list[list[str]], paint: dict[str, str]) -> str:
    """Join all list and all characters - Dupplicate char for a better view """
    return ("\n".join("".join(colorize(c, paint) for c in each_row)
            for each_row in screen))


if __name__ == "__main__":
    screen = build_screen(mock_2x2())
    path(screen, (0, 0), "ESW")
    markers(screen, (0, 0), (0, 1))
    print(render(screen, COLORS[0]))
    print()
    screen = build_screen(mock_6x6())
    path(screen, (0, 0), "ESESEESSWWSW")
    markers(screen, (0, 0), (1, 5))
    print(render(screen, COLORS[0]))
