import random
import time
from typing import Literal

from config import BOARD_HEIGHT, BOARD_WIDTH

random.seed(time.time())

PIECE_NAMES = Literal["I", "O", "T", "J", "L", "S", "Z"]

# fmt: off
__PIECES__ = {
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
            [0, 2]],
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
            [0, 0, 3]],
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


class Piece:
    def __init__(self, type: PIECE_NAMES, rotation: int = 0, y=0, x=0):
        self.__name = type
        self.__rotation_idx = self.__normalize_idx(rotation)
        self.x = x
        self.y = y

    @staticmethod
    def names():
        return list(__PIECES__.keys())

    @staticmethod
    def random_new():
        random_x = random.randrange(0, BOARD_WIDTH - 1)
        random_rotation = random.randrange(0, 4)
        random_name = random.choice(Piece.names())

        piece = Piece(type=random_name, rotation=random_rotation)

        piece.x = max(0, min(random_x, BOARD_WIDTH - piece.width))
        piece.y -= piece.height - 1

        return piece

    @staticmethod
    def random_list(total: int = 1):
        pieces: list[Piece] = []
        for i in range(total):
            pieces.append(Piece.random_new())

        return pieces

    @property
    def shape(self):
        return self.__shape_by_index(self.__rotation_idx)

    @property
    def ratation_idx(self):
        return self.__rotation_idx

    @property
    def name(self):
        return self.__name

    @property
    def width(self):
        return len(self.shape[0])

    @property
    def height(self):
        return len(self.shape)

    def move(
        self,
        direction: Literal["UP", "DOWN", "LEFT", "RIGHT"],
        value=1,
    ):
        if direction == "UP":
            self.y = max(0, self.y - value)

        if direction == "DOWN":
            self.y = min(self.y + value, BOARD_HEIGHT - self.height)

        if direction == "RIGHT":
            self.x = min(self.x + value, BOARD_WIDTH - self.width)

        if direction == "LEFT":
            self.x = max(0, self.x - value)

    def rotate(self, idx: int = None):
        self.__rotation_idx = self.__normalize_idx(
            idx if idx else self.__rotation_idx + 1
        )

    def calc_next_rotate(self):
        return Piece(self.__name, self.__normalize_idx(self.__rotation_idx + 1))

    def __normalize_idx(self, index: int):
        return index % len(__PIECES__[self.__name])

    def __shape_by_index(self, idx: int):
        return __PIECES__[self.__name][self.__normalize_idx(idx)]
