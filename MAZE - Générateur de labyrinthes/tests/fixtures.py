
Grid = list[list[dict[str, bool]]]


def mock_2x2() -> Grid:
    """Fake maze 2x2. False = no wall. Entry(0,0) and exit(1,1)"""
    return [
        [
            {"N": True, "E": False, "S": True, "W": True},
            {"N": True, "E": True, "S": False, "W": False},
        ],
        [
            {"N": True, "E": False, "S": True, "W": True},
            {"N": False, "E": True, "S": True, "W": False},
        ],
    ]


def mock_6x6() -> Grid:
    """Fake maze 6x6. Entry(0,0) and exit(5,1)"""
    return [
        [
            {"N": True, "E": False, "S": True, "W": True},
            {"N": True, "E": True, "S": False, "W": False},
            {"N": True, "E": False, "S": False, "W": True},
            {"N": True, "E": True, "S": False, "W": False},
            {"N": True, "E": True, "S": False, "W": True},
            {"N": True, "E": True, "S": True, "W": True},
        ],
        [
            {"N": True, "E": True, "S": False, "W": True},
            {"N": False, "E": False, "S": True, "W": True},
            {"N": False, "E": True, "S": False, "W": False},
            {"N": False, "E": False, "S": True, "W": True},
            {"N": False, "E": False, "S": True, "W": False},
            {"N": True, "E": True, "S": True, "W": False},
        ],
        [
            {"N": False, "E": True, "S": False, "W": True},
            {"N": True, "E": True, "S": False, "W": True},
            {"N": False, "E": False, "S": True, "W": True},
            {"N": True, "E": False, "S": True, "W": False},
            {"N": True, "E": True, "S": False, "W": False},
            {"N": True, "E": True, "S": False, "W": True},
        ],
        [
            {"N": False, "E": False, "S": False, "W": True},
            {"N": False, "E": False, "S": True, "W": False},
            {"N": True, "E": False, "S": False, "W": False},
            {"N": True, "E": True, "S": True, "W": False},
            {"N": False, "E": False, "S": False, "W": True},
            {"N": False, "E": True, "S": True, "W": False},
        ],
        [
            {"N": False, "E": False, "S": True, "W": True},
            {"N": True, "E": True, "S": True, "W": False},
            {"N": False, "E": False, "S": False, "W": True},
            {"N": True, "E": False, "S": True, "W": False},
            {"N": False, "E": False, "S": False, "W": False},
            {"N": True, "E": True, "S": True, "W": False},
        ],
        [
            {"N": True, "E": False, "S": True, "W": True},
            {"N": True, "E": False, "S": True, "W": False},
            {"N": False, "E": True, "S": True, "W": False},
            {"N": True, "E": False, "S": True, "W": True},
            {"N": False, "E": False, "S": True, "W": False},
            {"N": True, "E": True, "S": True, "W": False},
        ],
     ]
