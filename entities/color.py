from config import PIECE_BG_COLORS
from entities.piece import PIECE_NAMES


class Color:
    @staticmethod
    def color_by_name(name: PIECE_NAMES):
        return PIECE_BG_COLORS[name]

    @staticmethod
    def color_by_number(num: int):
        color_map = {
            1: PIECE_BG_COLORS["I"],
            2: PIECE_BG_COLORS["O"],
            3: PIECE_BG_COLORS["T"],
            4: PIECE_BG_COLORS["J"],
            5: PIECE_BG_COLORS["L"],
            6: PIECE_BG_COLORS["S"],
            7: PIECE_BG_COLORS["Z"],
        }

        color = color_map[max(1, min(7, num))]
        # print(color)
        return color
