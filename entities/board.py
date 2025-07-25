import numpy as np
from config import BOARD_HEIGHT, BOARD_WIDTH, TERM
from entities.piece import Piece


class Board:
    def __init__(self, width: int, height: int):
        self.__shape = self.__generate_empty_map(width, height)

    @property
    def shape(self):
        return self.__shape

    @property
    def width(self):
        return len(self.shape[0])

    @property
    def height(self):
        return len(self.shape)

    def reset(self):
        self.__shape = self.__generate_empty_map(self.width, self.height)

    def __generate_empty_map(self, width: int, height: int):
        return [[0 for _ in range(width)] for _ in range(height)]

    def insert_block(self, piece: Piece):
        board = self.shape
        piece_map = piece.shape

        offset_x = min(piece.x, self.width - 1)
        offset_y = min(piece.y, self.height - 1)

        for y, row in enumerate(piece_map):
            for x, val in enumerate(row):
                if val:
                    py = y + offset_y
                    px = x + offset_x
                    if (
                        py >= 0
                        and py < self.height
                        and px >= 0
                        and px < self.width
                        and board[py]
                    ):
                        if not board[py][px]:
                            board[py][px] = val

    def clear_block(self, piece: Piece):
        board = self.shape

        x = min(piece.x, self.width)
        y = min(piece.y, self.height)

        for i, row in enumerate(piece.shape):
            for j, val in enumerate(row):
                py = min(min(i + y, i + y - piece.height), self.height - 1)
                px = min(max(j, j + x - piece.width), self.width - 1)

                board[py][px] = 0

    def has_top_conflict(self, piece: Piece, num_lines=2):
        num_lines = min(num_lines, BOARD_HEIGHT - 1)
        for y in range(num_lines):
            for x, cell in enumerate(self.shape[y]):
                py = y - piece.y
                px = x - piece.x

                if (
                    cell
                    and py >= 0
                    and py < piece.height - 1
                    and px >= 0
                    and px < piece.width - 1
                    and piece.shape[py][px]
                ):
                    return True
        return False

    def check_next_collision(self, piece: Piece):
        # print(
        #     TERM.move_xy(80, 2)
        #     + f"Piece[x, y]: {piece.x, piece.y} / Piece[height, width]: {piece.height, piece.width} "
        #     + " " * 5
        # )

        for y, row in enumerate(piece.shape):
            for x, col in enumerate(row):
                py = piece.y + y + 2 if piece.y + piece.height < 1 else piece.y + y + 1
                px = piece.x + x

                if col and py >= 0 and py < self.height and px >= 0 and px < self.width:
                    overflow = piece.y <= 0
                    if self.shape[py][px]:
                        return True, overflow

        if piece.y + piece.height > self.height - 1:
            return True, False

        return False, False

    def check_complete_line(self):
        board = self.shape
        new_board: list[list[int]] = []
        count = 0

        for i, row in enumerate(board):
            if 0 in row:
                new_board.append(row)
            else:
                count += 1

        while len(new_board) < len(board):
            new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])

        self.__shape = new_board

        return count > 0, count

    def find_first_occupied_row(self):
        for y, row in enumerate(self.shape):
            if any(cell > 0 for cell in row):
                return y

        return -1

    def __draw_map(self, offset_px=0, offset_py=0):
        fg = TERM.black
        for y, row in enumerate(self.shape):
            for x, val in enumerate(row):
                print(
                    TERM.move_xy(x + offset_px, y + offset_py)
                    + fg(f"{val if val else "█"}")
                    + TERM.normal
                )

        print(TERM.normal)
