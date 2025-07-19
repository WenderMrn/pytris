import copy

from models.board import Board
from models.color import Color
from models.context import TERM
from models.piece import Piece

BOARD_WIDTH = 20
BOARD_HEIGHT = 20
OFFSET_Y = 1
CELL_WIDTH = 2  # caracteres por célula


def print_matrix(mtz, name=""):
    print(f"\n{name}{"-" * 50}\n")
    for row in mtz:
        print(row)
    print(f"\n{"-" * (50 + len(name))}\n")


def draw_board(board: Board, start_x=0, start_y=0):
    print(TERM.home + TERM.clear)

    # print(TERM.move(0, 0) + "+" + "=" * (BOARD_WIDTH * 2) + "+")
    fg = TERM.black
    for i, row in enumerate(board.shape):
        for j, val in enumerate(row):
            bg = Color.color_by_number(val) if val else TERM.on_color_rgb(192, 192, 192)
            print(
                TERM.move(start_y + i, start_x + j * CELL_WIDTH)
                + bg
                + fg("[]" if val else "::")
                + TERM.normal
            )

    print(TERM.normal)

    print_matrix(board.shape, "GAME BOARD")


def can_place(board_obj: Board, piece_obj: Piece, x, y):
    board = board_obj.shape
    piece = piece_obj.shape

    board_height = len(board)
    board_width = len(board[0])
    piece_height = len(piece)
    piece_width = len(piece[0])

    x = min(x, board_width)
    y = min(y, board_height)

    for i, row in enumerate(piece):
        for j, val in enumerate(row):
            if val:
                new_y = min(min(i + y, i + y - piece_height), board_width - 1)
                new_x = min(max(j, j + x - piece_width), board_height - 1)

                # Fora do tabuleiro?
                if (
                    new_y < 0
                    or new_y >= board_height
                    or new_x < 0
                    or new_x >= board_width
                ):
                    print(f"out board: {new_x}, {new_y}")
                    return False

                # Posição já ocupada?
                if board[new_y][new_x]:
                    print(f"busy position: {new_x}, {new_y} / {board[new_y][new_x]}")
                    return False

    return True


def fix_piece_on_board(board_obj: Board, piece_obj: Piece, x, y):
    board = board_obj.shape
    piece = piece_obj.shape

    board_size = len(board)
    row_size = len(piece)
    col_size = len(piece[0])

    x = min(x, board_size)
    y = min(y, board_size)

    for i, row in enumerate(piece):
        for j, val in enumerate(row):
            if val:
                # p_row = min(min(i + y, i + y), board_size - 1)
                # p_col = min(max(j, j + x), board_size - 1)
                # OFFSET
                p_row = min(min(i + y, i + y - row_size), board_size - 1)
                p_col = min(max(j, j + x - col_size), board_size - 1)
                board[p_row][p_col] = val  # ou uma cor/código da peça


def main():
    BOARD = Board(BOARD_WIDTH, BOARD_HEIGHT)
    draw_board(BOARD)

    sequence = [
        # {"piece": Piece("T", 0), "coord": [0, 18]},
        # {"piece": Piece("T", 1), "coord": [0, 17]},
        # {"piece": Piece("L", 3), "coord": [2, 17]},
        # {"piece": Piece("I", 0), "coord": [3, 19]},
        # {"piece": Piece("T", 4), "coord": [17, 18]},
        # {"piece": Piece("L", 3), "coord": [18, 16]},
        # {"piece": Piece("Z", 1), "coord": [16, 17]},
        # OFFSET
        {"piece": Piece("T", 0), "coord": [0, 20]},
        {"piece": Piece("T", 1), "coord": [0, 19]},
        {"piece": Piece("L", 3), "coord": [3, 19]},
        {"piece": Piece("I", 0), "coord": [7, 20]},
        {"piece": Piece("T", 4), "coord": [20, 20]},
        {"piece": Piece("L", 3), "coord": [20, 19]},
        {"piece": Piece("Z", 1), "coord": [18, 20]},
    ]

    boardfilled = copy.deepcopy(BOARD)

    for seq in sequence:
        piece = seq["piece"]
        x = seq["coord"][0]
        y = seq["coord"][1]

        can = can_place(boardfilled, piece, x, y)
        # print(f"\nCan place? {can}")
        if can:
            fix_piece_on_board(boardfilled, piece, x, y)

        draw_board(boardfilled)

    pass


if __name__ == "__main__":
    main()
