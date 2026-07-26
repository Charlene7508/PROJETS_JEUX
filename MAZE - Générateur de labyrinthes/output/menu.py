from tests.fixtures import mock_6x6
from output.display import build_screen, markers, path, render, COLORS, Grid
from typing import Callable


def menu(generate: Callable[[], Grid], entry_pos: tuple[int, int],
         exit_pos: tuple[int, int], solution: str) -> None:
    """"Menu display for players"""
    grid = generate()
    paint_index = 0
    show_path = False
    while True:
        screen = build_screen(grid)
        if show_path:
            path(screen, entry_pos, solution)
        markers(screen, entry_pos, exit_pos)
        print(render(screen, COLORS[paint_index]))

        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Change maze wall colors")
        print("4. Quit")
        try:
            choice = input("Choice? (1-4): ")
            if choice == "1":
                grid = generate()
            if choice == "2":
                if not show_path:
                    show_path = True
                else:
                    show_path = False
            if choice == "3":
                paint_index = (paint_index + 1) % len(COLORS)
            if choice == "4":
                break
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    menu(mock_6x6, (0, 0), (1, 5), "ESESEESSWWSW")
