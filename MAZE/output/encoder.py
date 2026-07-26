from tests.fixtures import mock_6x6

Grid = list[list[dict[str, bool]]]
WEIGHT = {"N": 1, "E": 2, "S": 4, "W": 8}


def hexa_cell(cell: dict[str, bool]) -> str:
    """Convert a cell into hexa by adding the weight of each closed wall"""
    total = 0
    for x in WEIGHT:
        if cell[x]:
            total += WEIGHT[x]
    return format(total, "X")


def hexa_grid(grid: Grid) -> str:
    """Convert a grid into hexa by adding the weight
      of each cell line per line"""
    text_lines = []
    for row in grid:
        row_text = ""
        for cell in row:
            row_text += hexa_cell(cell)
        text_lines.append(row_text)
    return "\n".join(text_lines)


def build_output(
        grid: Grid,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        solution: str
        ) -> str:
    output = []
    output.append(hexa_grid(grid) + "\n")
    output.append(f"{entry[0]},{entry[1]}")
    output.append(f"{exit_pos[0]},{exit_pos[1]}")
    output.append(solution)
    return "\n".join(output)


def write_maze_file(
        grid: Grid,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        solution: str,
        filename: str,
        ) -> None:
    content = build_output(grid, entry, exit_pos, solution)
    with open(filename, "w") as file:
        file.write(content + "\n")


if __name__ == "__main__":
    test_output = build_output(mock_6x6(), (0, 0), (5, 1), "SEE")
    print(test_output)
    write_maze_file(mock_6x6(), (0, 0), (5, 1), "SEE", "maze.txt")
