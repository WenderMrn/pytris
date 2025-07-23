from typing import Literal
from blessed import Terminal

TERM = Terminal()

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_WIDTH = 2
DEBUG = False
GAME_SPEED = 1.75
PLAYER_SEED = 1

PIECE_BG_COLORS = {
    "I": TERM.on_cyan,
    "O": TERM.on_yellow,
    "T": TERM.on_magenta,
    "S": TERM.on_green,
    "Z": TERM.on_red,
    "J": TERM.on_blue,
    "L": TERM.on_bright_yellow,
}

PIECE_NAMES = Literal["I", "O", "T", "J", "L", "S", "Z"]

# fmt: off
PIECES = {
    "I": [
        [
            [1, 1, 1, 1]
        ], 
        [
            [1], 
            [1], 
            [1], 
            [1]
        ]
    ],
    "O": [
        [
            [1, 1], 
            [1, 1]
        ]
    ],
    "T": [
        [
            [0, 2, 0], 
            [2, 2, 2]],
        [
            [2, 0], 
            [2, 2], 
            [2, 0]
        ],
        [
            [2, 2, 2], 
            [0, 2, 0]
        ],
        [
            [0, 2], 
            [2, 2], 
            [0, 2]
        ],
    ],
    "J": [
        [
            [3, 0, 0], 
            [3, 3, 3]
        ],
        [
            [3, 3], 
            [3, 0], 
            [3, 0]
        ],
        [
            [3, 3, 3], 
            [0, 0, 3]
        ],
        [
            [0, 3], 
            [0, 3], 
            [3, 3]
        ],
    ],
    "L": [
        [
            [0, 0, 4], 
            [4, 4, 4]
        ],
        [
            [4, 0], 
            [4, 0], 
            [4, 4]],
        [
            [4, 4, 4], 
            [4, 0, 0]
        ],
        [
            [4, 4], 
            [0, 4], 
            [0, 4]
        ],
    ],
    "S": [
        [
            [0, 5, 5], 
            [5, 5, 0]
        ], 
        [
            [5, 0], 
            [5, 5], 
            [0, 5]
        ]
    ],
    "Z": [
        [
            [6, 6, 0], 
            [0, 6, 6]
        ], 
        [
            [0, 6], 
            [6, 6], 
            [6, 0]
        ]
    ],
}
# fmt: on
