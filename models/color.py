from models.context import TERM
from models.piece import PIECE_NAMES

__PIECE_COLORS__ = {
    "I": TERM.on_cyan,
    "O": TERM.on_yellow,
    "T": TERM.on_magenta,
    "S": TERM.on_green,
    "Z": TERM.on_red,
    "J": TERM.on_blue,
    "L": TERM.on_bright_yellow,
}


class Color:
    @staticmethod
    def color_by_name(name: PIECE_NAMES):
        return __PIECE_COLORS__[name]

    @staticmethod
    def color_by_number(num: int):
        color_map = {
            1: __PIECE_COLORS__["I"],
            2: __PIECE_COLORS__["O"],
            3: __PIECE_COLORS__["T"],
            4: __PIECE_COLORS__["J"],
            5: __PIECE_COLORS__["L"],
            6: __PIECE_COLORS__["S"],
            7: __PIECE_COLORS__["Z"],
        }

        color = color_map[max(1, min(7, num))]
        # print(color)
        return color
