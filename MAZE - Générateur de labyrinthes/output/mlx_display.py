import sys
from typing import Any
from mlx import Mlx  # type: ignore
from mazegen.mazegen import generate_maze, breadth_first_search, shortest_path
from config_loader import load_config
from output.display import build_screen, markers, path, WALL, PATH, ENTRY, EXIT


CELL_SIZE = 40
MENU_WIDTH = 400

BLUE = 0xFF0000FF
WHITE = 0xFFFFFFFF
GREEN = 0xFF00FF00
BLACK = 0xFF000000
GREY = 0xFF808080

COLORS = [
    {"wall": WHITE, "path": GREY, "entry": BLACK, "exit": BLACK},
    {"wall": GREY, "path": WHITE, "entry": BLACK, "exit": BLACK},
    {"wall": GREEN, "path": BLUE, "entry": BLACK, "exit": BLACK},
]

KEY = {WALL: "wall", PATH: "path", ENTRY: "entry", EXIT: "exit"}


def gere_close(dummy: Any) -> None:
    """Activate the cross on the window to exit"""
    m.mlx_loop_exit(mlx_ptr)


def draw_maze_with_player(state: dict[str, Any]) -> None:
    """Draw the maze walls AND the player in
    a single buffer (no layering issues)."""
    screen = build_screen(state["grid"])
    if state["show_path"]:
        path(screen, state["entry"], state["solution"])
    markers(screen, state["entry"], state["exit"])
    paint = COLORS[state["palette_index"]]

    win_width = len(screen[0]) * CELL_SIZE
    win_height = len(screen) * CELL_SIZE

    img = m.mlx_new_image(mlx_ptr, win_width, win_height)
    data, bpp, size_line, iformat = m.mlx_get_data_addr(img)

    black_bytes = BLACK.to_bytes(4, "little")
    total_pixels = win_width * win_height
    i = 0
    while i < total_pixels * 4:
        data[i:i + 4] = black_bytes
        i += 4

    row = 0
    while row < len(screen):
        col = 0
        while col < len(screen[0]):
            c = screen[row][col]
            if c in KEY:
                color = paint[KEY[c]]
                color_bytes = color.to_bytes(4, "little")
                px = 0
                while px < CELL_SIZE:
                    py = 0
                    while py < CELL_SIZE:
                        x = col * CELL_SIZE + px
                        y = row * CELL_SIZE + py
                        offset = y * size_line + x * 4
                        data[offset:offset + 4] = color_bytes
                        py += 1
                    px += 1
            col += 1
        row += 1

    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img, 0, 0)
    m.mlx_destroy_image(mlx_ptr, img)

    sx = (state["exit"][0] * 2 + 1) * CELL_SIZE
    sy = (state["exit"][1] * 2 + 1) * CELL_SIZE
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, state["planet"], sx, sy)

    ex = (state["player"][0] * 2 + 1) * CELL_SIZE
    ey = (state["player"][1] * 2 + 1) * CELL_SIZE
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, state["alien"], ex, ey)

    if state["won"]:
        center = (len(screen[0]) * CELL_SIZE) // 2 - 160
        pattern_y = (state["height"] - 3) // 2
        msg_won = (pattern_y * 2 + 1) * CELL_SIZE
        m.mlx_string_put(mlx_ptr, win_ptr, center, msg_won, 0xFF00FF00,
                         "I found my home ! Thank you human <3 ! ")
        m.mlx_string_put(mlx_ptr, win_ptr, center, msg_won + 20, 0xFFFFFFFF,
                         "I found my home ! Thank you human <3 ! ")
        m.mlx_string_put(mlx_ptr, win_ptr, center, msg_won + 40, 0xFFFF0000,
                         "I found my home ! Thank you human <3 ! ")

    m.mlx_do_sync(mlx_ptr)


def draw_menu_text(state: dict[str, Any]) -> None:
    """Draw the static menu text once — never redrawn after."""
    screen = build_screen(state["grid"])
    menu_x = len(screen[0]) * CELL_SIZE + 20
    menu_y = 40
    m.mlx_string_put(mlx_ptr, win_ptr, menu_x,
                     menu_y, 0xFFFFFFFF, "Choice? (1-4):")
    m.mlx_string_put(mlx_ptr, win_ptr, menu_x,
                     menu_y + 30, 0xFFFFFFFF, "1. Re-generate a new maze")
    m.mlx_string_put(mlx_ptr, win_ptr, menu_x,
                     menu_y + 60, 0xFFFFFFFF,
                     "2. Show/Hide path from entry to exit")
    m.mlx_string_put(mlx_ptr, win_ptr, menu_x,
                     menu_y + 90, 0xFFFFFFFF, "3. Change maze wall colors")
    m.mlx_string_put(mlx_ptr, win_ptr, menu_x,
                     menu_y + 120, 0xFFFFFFFF, "4. Quit")


def redraw(state: dict[str, Any]) -> None:
    """Full redraw: background + player.
    Use only when the maze itself changes."""
    draw_maze_with_player(state)
    draw_menu_text(state)
    m.mlx_do_sync(mlx_ptr)


def key_handler(keynum: int, param: dict[str, Any]) -> None:
    """Call to action on menu"""
    if keynum == 65436:
        param["grid"] = generate_maze(param["width"], param["height"])
        bfs = breadth_first_search(param["grid"],
                                   param["entry"], param["exit"])
        param["solution"] = shortest_path(bfs, param["entry"], param["exit"])
        param["player"] = param["entry"]
        param["won"] = False
        redraw(param)
    if keynum == 65433:
        param["show_path"] = not param["show_path"]
        redraw(param)
    if keynum == 65435:
        param["palette_index"] = (param["palette_index"] + 1) % len(COLORS)
        redraw(param)
    if keynum == 65430:
        m.mlx_loop_exit(mlx_ptr)
    if keynum == 65362:
        x, y = param["player"]
        if not param["grid"][y][x]["N"]:
            param["player"] = (x, y - 1)
            if param["player"] == param["exit"]:
                param["won"] = True
        draw_maze_with_player(param)
    if keynum == 65363:
        x, y = param["player"]
        if not param["grid"][y][x]["E"]:
            param["player"] = (x + 1, y)
            if param["player"] == param["exit"]:
                param["won"] = True
        draw_maze_with_player(param)
    if keynum == 65364:
        x, y = param["player"]
        if not param["grid"][y][x]["S"]:
            param["player"] = (x, y + 1)
            if param["player"] == param["exit"]:
                param["won"] = True
        draw_maze_with_player(param)
    if keynum == 65361:
        x, y = param["player"]
        if not param["grid"][y][x]["W"]:
            param["player"] = (x - 1, y)
            if param["player"] == param["exit"]:
                param["won"] = True
        draw_maze_with_player(param)


if __name__ == "__main__":
    config_path = "config.txt"
    config = load_config(config_path)
    if config is None:
        sys.exit(1)

    width = config["WIDTH"]
    height = config["HEIGHT"]
    maze = generate_maze(width, height)
    entry = config["ENTRY"]
    exit = config["EXIT"]
    bfs = breadth_first_search(maze, entry, exit)
    solution = shortest_path(bfs, entry, exit)

    state: dict[str, Any] = {
        "grid": maze,
        "width": width,
        "height": height,
        "palette_index": 0,
        "show_path": False,
        "entry": entry,
        "exit": exit,
        "solution": solution,
        "player": entry,
        "won": False,
    }
    screen = build_screen(state["grid"])
    window_width = len(screen[0]) * CELL_SIZE + MENU_WIDTH
    window_height = len(screen) * CELL_SIZE
    m = Mlx()
    mlx_ptr = m.mlx_init()
    print("win_width:", window_width, "win_height:", window_height)
    win_ptr = m.mlx_new_window(mlx_ptr, window_width,
                               window_height, "HAVE FUN !")
    alien, aw, ah = m.mlx_png_file_to_image(mlx_ptr, "output/assets/alien.png")
    planet, pw, ph = m.mlx_png_file_to_image(
        mlx_ptr, "output/assets/planet.png")
    state["alien"] = alien
    state["planet"] = planet
    redraw(state)
    m.mlx_hook(win_ptr, 33, 0, gere_close, None)
    m.mlx_key_hook(win_ptr, key_handler, state)
    m.mlx_loop(mlx_ptr)
