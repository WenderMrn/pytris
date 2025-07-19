import copy
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
        return len(self.shape)

    @property
    def height(self):
        return len(self.shape[0])

    def reset(self):
        self.__shape = self.__generate_empty_map(self.width, self.height)

    def __generate_empty_map(self, width: int, height: int):
        return [[0 for _ in range(width)] for _ in range(height)]

    def insert_block(self, piece: Piece):
        board = self.shape
        piece_map = piece.shape

        offset_x = min(piece.x, self.width)
        offset_y = min(piece.y, self.height)

        for i, row in enumerate(piece_map):
            for j, val in enumerate(row):
                if val:
                    py = min(i + offset_y, self.height - 1)
                    px = min(j + offset_x, self.width - 1)
                    if not board[py][px]:
                        board[py][px] = val

    # def clear_block(self, piece: Piece):
    #     board = self.shape
    #     piece_map = piece.shape

    #     board_size = len(board)
    #     row_size = len(piece_map)
    #     col_size = len(piece_map[0])

    #     x = min(piece.x, board_size)
    #     y = min(piece.y, board_size)

    #     for i, row in enumerate(piece_map):
    #         for j, val in enumerate(row):
    #             py = min(min(i + y, i + y - row_size), board_size - 1)
    #             px = min(max(j, j + x - col_size), board_size - 1)
    #             board[py][px] = 0

    def check_colision(self, piece: Piece):
        board = self.shape
        piece_max_size = max(piece.height, piece.width)

        piece_box_colision = np.zeros((piece_max_size, BOARD_WIDTH))
        board_box_colision = np.zeros((piece_max_size, BOARD_WIDTH))

        if piece.y + piece.height > BOARD_HEIGHT - 1:
            return True

        line_colision_height = len(piece_box_colision)
        line_colision_width = len(piece_box_colision[0])

        for i, row in enumerate(piece.shape):
            for j, col in enumerate(row):
                piece_box_colision[i][(j + piece.x) - line_colision_width] = col

        for i in range(line_colision_height):
            if (i + piece.y + 1) < BOARD_HEIGHT - 1:
                print(term.move_xy(80, i) + f"{board[i + piece.y + 1]}" + " " * 50)
                board_box_colision[i] = board[i + piece.y + 1]

        for i, row in enumerate(board_box_colision):
            for j, col in enumerate(row):
                if col and piece_box_colision[i][j]:
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

        for i, row in enumerate(map1):
            print(term.move_xy(x, i + y) + f" " + " " * 50)

        for i, row in enumerate(map1):
            print(term.move_xy(x, i + y) + f"{row}" + " " * 50)

        if map2.any():
            for i, row in enumerate(map2):
                print(term.move_xy(x, i + y + height) + f"{row}" + " " * 50)
