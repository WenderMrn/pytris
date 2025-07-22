from typing import List
from config import CELL_WIDTH, TERM


class Rgb:
    def __init__(self, R: int, G: int, B: int):
        self.R = R
        self.G = G
        self.B = B


class Shapes:
    @staticmethod
    def draw_square(
        *,
        start_x: int = 0,
        start_y: int = 0,
        height: int = 0,
        width: int = 0,
        fill_char: str = " ",
        clear_screen: bool = False,
        bg_color: Rgb = Rgb(0, 0, 0),
    ):
        if clear_screen:
            print(TERM.home + TERM.clear)

        for y in range(height):
            for x in range(width):
                print(
                    TERM.move_xy((start_x + x) * CELL_WIDTH, start_y + y)
                    + (fill_char * CELL_WIDTH)
                )

    @staticmethod
    def draw_map(*, shape: list[list[int]], offset_x=0, offset_y=0):
        fg = TERM.black
        for y, row in enumerate(shape):
            for x, val in enumerate(row):
                print(
                    TERM.move_xy(x + offset_x, y + offset_y)
                    + fg(f"{val if val else "*"}")
                    + TERM.normal
                )

        print(TERM.normal)
