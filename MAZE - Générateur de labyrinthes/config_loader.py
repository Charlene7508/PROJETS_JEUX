from typing import Any


def load_config(file_config: str) -> dict[str, Any] | None:
    '''Read informations from config.txt'''
    lines = []
    config = {}
    with open(file_config, "r") as file:
        content = file.read()
        lines = content.split("\n")

    for line in lines:
        if not line or line[0] == "#":
            continue
        key, value = line.split("=")
        config[key] = value

    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])
        x, y = config["ENTRY"].split(",")
        config["ENTRY"] = (int(x), int(y))
        x, y = config["EXIT"].split(",")
        config["EXIT"] = (int(x), int(y))

    except Exception as e:
        print(f"{e}")
        return None

    return config


if __name__ == "__main__":
    result = load_config("config.txt")
    print(result)
