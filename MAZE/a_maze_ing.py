import sys
from config_loader import load_config
from mazegen.mazegen import generate_maze, breadth_first_search, shortest_path
from output.encoder import write_maze_file
from output.menu import menu

Grid = list[list[dict[str, bool]]]


def main(config_path: str) -> None:
    """Run pipeline: check config, generate maze, write file, launch menu"""
    config = load_config(config_path)
    if config is None:
        return
    try:
        width = config["WIDTH"]
        height = config["HEIGHT"]
        maze = generate_maze(width, height)
        entry = config["ENTRY"]
        exit = config["EXIT"]
        bfs = breadth_first_search(maze, entry, exit)
        solution = shortest_path(bfs, entry, exit)

        write_maze_file(maze, config["ENTRY"], config["EXIT"],
                        solution, config["OUTPUT_FILE"])

        def regenerate() -> Grid:
            return generate_maze(width, height)
        menu(regenerate, config["ENTRY"], config["EXIT"], solution)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("You need to add the config file to run the maze")
        sys.exit(1)
    main(sys.argv[1])
