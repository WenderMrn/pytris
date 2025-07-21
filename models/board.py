from typing import List
import numpy as np
from config import BOARD_HEIGHT, BOARD_WIDTH
from models.piece import Piece

from blessed import Terminal

term = Terminal()


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

        for i, row in enumerate(piece_map):
            for j, val in enumerate(row):
                if val:
                    py = i + offset_y
                    px = j + offset_x
                    if py < self.height and px < self.width and board[py]:
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

    def check_next_colision(self, piece: Piece):
        board = self.shape

        if piece.y < 0 or piece.width < 0:
            return False

        piece_box_colision = np.zeros(
            (
                piece.height + 1,
                BOARD_WIDTH,
            ),
            dtype=int,
        )
        board_box_colision = np.zeros(
            (
                piece.height + 1,
                BOARD_WIDTH,
            ),
            dtype=int,
        )

        if piece.y + piece.height > BOARD_HEIGHT - 1:
            return True

        line_colision_height = len(piece_box_colision)
        line_colision_width = len(piece_box_colision[0])

        for y, row in enumerate(piece.shape):
            for x, col in enumerate(row):
                if col:
                    piece_box_colision[y][(x + piece.x) - line_colision_width] = col

        offset_py = piece.y + 1

        for y in range(line_colision_height):
            py = offset_py + y
            if py < BOARD_HEIGHT:
                board_box_colision[y] = board[py]

        for i, row in enumerate(board_box_colision):
            for j, col in enumerate(row):
                if col and i < line_colision_height and piece_box_colision[i][j]:
                    return True

        return False

    def check_complete_line(self):
        board = self.shape

        for i, row in enumerate(board):
            if not 0 in row:
                board.pop(i)
                board.insert(0, [0 for x in range(BOARD_WIDTH)])

    def print_map(self, map1, map2, x, y):
        height = len(map1) + 3

        for i in range(2 * len(map1) + 3):
            print(term.move_xy(x, i + y) + f" " + " " * 50)

        for i, row in enumerate(map1):
            print(term.move_xy(x, i + y) + f"{row}" + " " * 50)

        if map2.any():
            for i, row in enumerate(map2):
                print(term.move_xy(x, i + y + height) + f"{row}" + " " * 50)
