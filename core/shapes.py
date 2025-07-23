from typing import List
from config import BOARD_HEIGHT, BOARD_WIDTH, CELL_WIDTH, TERM


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

        if height == 0 or width == 0:
            height = max(height, width)
            width = height

        for y in range(height):
            for x in range(width):
                print(TERM.move_xy(start_x + x, start_y + y) + (fill_char))

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

    @staticmethod
    def draw_text(
        text: str, center: bool = False, bg=TERM.normal, x: int = 0, y: int = 0
    ):
        if center:
            x = BOARD_WIDTH - len(text) // 2
            y = BOARD_HEIGHT // 2

        print(
            TERM.move_xy(
                x,
                y,
            )
            + bg
            + text
            + TERM.normal
        )
