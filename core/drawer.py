from typing import List, Literal
from config import (
    BLOCK_LETTERS,
    SMALL_BLOCK_LETTERS,
    TERM,
    BoardValues,
)
from entities.board import Board
from entities.color import Color
from entities.piece import Piece


from art import text2art


class Drawer:
    @staticmethod
    def clear_screen():
        print(TERM.home + TERM.clear)

    @staticmethod
    def draw_square(
        *,
        start_x: int = 0,
        start_y: int = 0,
        height: int = 0,
        width: int = 0,
        fill_char: str = " ",
        clear_screen: bool = False,
        fg_color=None,
        bg_color=TERM.normal,
    ):
        if clear_screen:
            print(TERM.home + TERM.clear)

        if height == 0 or width == 0:
            height = max(height, width)
            width = height

        for y in range(height):
            for x in range(width):
                print(
                    TERM.move_xy(start_x + x, start_y + y)
                    + bg_color
                    + (fg_color(fill_char) if fg_color else fill_char)
                    + TERM.normal
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

    @staticmethod
    def draw_text(
        text: str,
        center: bool = False,
        fg=TERM.white,
        bg=TERM.normal,
        x: int = 0,
        y: int = 0,
        offset_x: int = 0,
        offset_y: int = 0,
    ):
        if center:
            x = BoardValues.WIDTH - len(text) // 2
            y = BoardValues.HEIGHT // 2

        print(
            TERM.move_xy(
                x + offset_x,
                y + offset_y,
            )
            + bg
            + (fg(text) if fg else text + TERM.normal)
        )

    @staticmethod
    def draw_board(*, board: Board):
        for py, row in enumerate(board.shape):
            for px, val in enumerate(row):
                bg = Color.bg_color(val) if val else TERM.on_color_rgb(192, 192, 192)
                fg = Color.fg_color(val) if val else TERM.white

                print(
                    TERM.move_xy(
                        px * BoardValues.CELL_WIDTH + BoardValues.OFFSET_X,
                        py + BoardValues.OFFSET_Y,
                    )
                    + bg
                    + fg("[]" if val else "⬜")
                    + TERM.normal
                )

        print(TERM.normal)

    @staticmethod
    def draw_piece(
        *,
        board: Board,
        piece: Piece,
        x=BoardValues.OFFSET_X,
        y=BoardValues.OFFSET_Y,
    ):
        if not piece:
            return

        for shape_y, row in enumerate(piece.shape):
            for shape_x, val in enumerate(row):
                bg = Color.bg_color(val) if val else TERM.on_white
                fg = Color.fg_color(val) if val else TERM.white
                py = piece.y + shape_y
                px = piece.x + shape_x

                if (
                    val
                    and (py >= 0 and py < board.height)
                    and (px >= 0 and px < board.width)
                ):
                    print(
                        TERM.move_xy(px * BoardValues.CELL_WIDTH + x, py + y)
                        + bg
                        + fg("[]" if val else "")
                        + TERM.normal
                    )

        print(TERM.normal)

    @staticmethod
    def render_text(
        *,
        text: str,
        fg_color=None,
        bg_color=TERM.normal,
        x=BoardValues.OFFSET_X,
        y=BoardValues.OFFSET_Y,
    ):

        big_text = text2art(text=text.upper(), font="big")

        for i, line in enumerate(big_text.splitlines()):
            print(
                TERM.move_xy(x, y + i)
                + bg_color
                + (fg_color(line) if fg_color else line)
                + TERM.normal
            )

        # with TERM.fullscreen(), TERM.cbreak(), TERM.hidden_cursor():
        #     print(TERM.clear)
        #     print(TERM.center(TERM.bold_yellow(big_text)))
        #     TERM.sleep(3)

    @staticmethod
    def render_block_text(
        *,
        text: str,
        size: str = "small",
        fg_color=None,
        bg_color=TERM.normal,
        x: int = 0,
        y: int = 0,
    ):
        text = text.upper()
        letters = BLOCK_LETTERS if size == "big" else SMALL_BLOCK_LETTERS

        # define altura
        height = len(next(iter(letters.values()), []))
        lines = ["" for _ in range(height)]

        for char in text:
            if char == " ":
                part = [" " * len(next(iter(letters.values()))[0])] * height
            else:
                part = letters.get(
                    char, ["?" * len(next(iter(letters.values()))[0])] * height
                )
            for i in range(height):
                lines[i] += part[i] + " "

        for i, line in enumerate(lines):
            print(
                TERM.move_xy(x, y + i)
                + bg_color
                + (fg_color(line) if fg_color else line)
                + TERM.normal
            )

    @staticmethod
    def render_game_instructions(
        instruction: Literal["MENU", "GAME", "NEW_GAME", "BACK"] = "MENU",
        x: int = 20,
        y: int = 25,
    ):
        messages: List[str] = []
        if instruction == "GAME":
            messages.append("Controls: → / ← to move / ↑ to rotate / ↓ to drop faster")
            messages.append('ESC to go back menu / "P" to pause / "R" to reset')
        elif instruction == "MENU":
            messages.append("Controls: ↑ to up / ↓ to down / ENTER to confirm")
        elif instruction == "NEW_GAME":
            messages.append("Controls: type your name and press ENTER to confirm")
        elif instruction == "BACK":
            messages.append("Controls: ESC to go back menu")

        if len(messages) > 0:
            for ly, line in enumerate(messages):
                print(TERM.move_xy(x, y + ly) + line + TERM.normal, end="")

    @staticmethod
    def render_screen():
        pass
