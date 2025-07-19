from blessed import Terminal
import threading
import time
import random
import copy

from models.color import Color
from models.piece import Piece
from models.board import Board

term = Terminal()
last_key = None

p_r = 0
p_c = 0

# Dimensões do board
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
CELL_WIDTH = 2  # caracteres por célula
SPEED = 1
OFFSET_Y = 1

# board state
board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT).shape


def draw_board(board, piece=None, x=0, y=0):
    py = max(OFFSET_Y + 1, y)
    print(term.home + term.clear)

    print(term.move(py, x) + "+" + "=" * (BOARD_WIDTH * 2) + "+")

    for row in range(BOARD_HEIGHT):
        line = "|"
        for col in range(BOARD_WIDTH):
            cell = board[row][col]

            # Desenha a peça se estiver nessa posição
            # if piece and is_piece_block(piece, row, col, py, x):
            #     line += term.on_green + "██" + term.normal
            if cell:
                line += term.on_yellow + "██" + term.normal
            else:
                line += "  "
        line += "|"
        print(line)

    # # Bottom border
    print("+" + "=" * (BOARD_WIDTH * 2) + "+")


def is_piece_block(piece, row, col, py, px):
    """Verifica se a célula (row, col) está dentro da peça"""
    for i, piece_row in enumerate(piece):
        for j, val in enumerate(piece_row):
            if val:
                if row == py + i and col == px + j:
                    return True
    return False


def draw_status(term, x, y):
    mensagem = f"Pressione 'q' para sair | x={x} y={y} | pr: {p_r}, pc: {p_c}"
    print(term.move(term.height + 2, 0) + term.clear_eol + mensagem, end="", flush=True)


def print_matrix(mtz):
    for row in mtz:
        print(" ".join(str(cell) for cell in row))
    print("**************************", end="\n")


def rotate_clockwise(matrix):
    return [list(row) for row in zip(*matrix[::-1])]


def draw_border():
    for y in range(BOARD_HEIGHT):
        print(term.move(y, 0) + term.white("+"), end=None, sep=None)
        print(term.move(y, BOARD_WIDTH * CELL_WIDTH + 1) + term.white("|"))
    bottom = "+" + "-" * (BOARD_WIDTH * CELL_WIDTH) + "+"
    print(term.move(BOARD_HEIGHT, 0) + term.white(bottom), end=None)


def draw_piece(x, y, matrix, bg, fg=term.black):
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                cx = x + col_idx * CELL_WIDTH
                cy = y + row_idx
                print(term.move(cy, cx) + bg + fg("  ") + term.normal)

    # print(term.save)
    # print(term.move(BOARD_HEIGHT + 3, 0) + f"p: x: {x}, y: {y}")
    # print(term.restore)


def clear_ghost():
    # Limpar a área da peça anterior
    for row_idx in range(4):
        print(term.move(2 + row_idx, 2) + " " * (CELL_WIDTH * 4))


def clear_piece(x, y, matrix):
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                cx = x + col_idx * CELL_WIDTH
                cy = y + row_idx
                print(term.move(cy, cx) + "  ")  # dois espaços para "apagar"


def key_listener():
    global last_key
    with term.cbreak():
        while True:
            key = term.inkey(timeout=0.1)
            if key:
                last_key = key


def clamp(val, minval, maxval):
    return max(minval, min(val, maxval))


def can_place(shape, x, y):
    for row_idx, row in enumerate(shape):
        for col_idx, cell in enumerate(row):
            if cell:
                bx = x + col_idx
                by = y + row_idx
                if bx < 0 or bx >= BOARD_WIDTH or by < 0 or by >= BOARD_HEIGHT:
                    return False
                if board[by][bx]:
                    return False
    return True


def trim_piece(piece):
    rows = len(piece)
    cols = len(piece[0])

    # Determina colunas e linhas não vazias
    non_empty_rows = [i for i in range(rows) if any(piece[i])]
    non_empty_cols = [j for j in range(cols) if any(piece[i][j] for i in range(rows))]

    min_row, max_row = min(non_empty_rows), max(non_empty_rows)
    min_col, max_col = min(non_empty_cols), max(non_empty_cols)

    trimmed = [row[min_col : max_col + 1] for row in piece[min_row : max_row + 1]]

    return trimmed, min_row, min_col


def play():
    global last_key
    global p_c
    global p_r

    threading.Thread(target=key_listener, daemon=True).start()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.home + term.clear)

        # draw_border()
        # print(
        #     term.move(BOARD_HEIGHT + 2, 0)
        #     + "Aparecendo uma peça aleatória a cada segundo. Pressione 'q' para sair."
        # )

        x = 1
        y = OFFSET_Y + CELL_WIDTH

        prev_x = x
        prev_y = y
        prev_piece = None

        piece_name = "L"  # random.choice(list(PIECES.keys()))
        piece = Piece(piece_name)
        color = Color.color_by_name(piece_name)

        draw_board(board, piece.shape)

        while True:

            prev_x = x
            prev_y = y

            p_r = len(piece.shape)
            p_c = len(piece.shape[0])

            prev_piece = copy.deepcopy(piece)

            if last_key:
                key = last_key
                if key.code == term.KEY_RIGHT:
                    x = clamp(
                        x + SPEED,
                        0,
                        BOARD_WIDTH * CELL_WIDTH - len(piece.shape[0]) * CELL_WIDTH + 1,
                    )
                elif key.code == term.KEY_LEFT:
                    x = clamp(
                        x - SPEED,
                        1,
                        BOARD_WIDTH * CELL_WIDTH - len(piece.shape[0]) * CELL_WIDTH,
                    )
                elif key.code == term.KEY_DOWN:
                    y = min(
                        y + SPEED,
                        max(
                            0,
                            BOARD_HEIGHT + OFFSET_Y,
                        ),
                    )

                elif key.code == term.KEY_UP:
                    rotated = piece.calc_next_rotate()
                    prev_piece = copy.deepcopy(piece)

                    piece = rotated
                    # if can_place(rotated, x, y):
                    #     x = clamp(x, 0, BOARD_WIDTH - len(rotated[0]))
                    #     y = clamp(y, 0, BOARD_HEIGHT - len(rotated))

                    #     prev_piece = copy.deepcopy(piece)
                    #     piece = rotated
                elif key.lower() == "c":
                    piece_name = random.choice(Piece.names())
                    piece = Piece(piece_name)
                    color = Color.color_by_name(piece_name)
                elif key.lower() == "r":
                    x = 1
                    y = OFFSET_Y + CELL_WIDTH
                elif key.lower() == "q":
                    exit(0)
                last_key = None

            if prev_x != x or prev_y != y or prev_piece.shape != piece.shape:
                clear_piece(prev_x, prev_y, prev_piece.shape)
                pass

            draw_piece(x, y, piece.shape, bg=color)  # posição inicial (x=2, y=2)
            draw_status(term, x, y)

            # print_matrix(piece.shape)
            time.sleep(0.1)


def print_board_value():
    for row in range(BOARD_HEIGHT):
        print(board[row])


def check_colision(piece: Piece, x: int, y: int):
    print(f"P: x: {x}, y: {y}")
    print_board_value()
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            cell = board[row][col]
            if y == row and x == col and not cell:
                for py_idx, p_row in enumerate(piece.shape):
                    for px_idx, p_col in enumerate(p_row):
                        if p_col:
                            board[y + py_idx][x + px_idx] = p_col

    print("**********************************", sep="\n")
    print(f"P: x: {x}, y: {y}")
    print_board_value()


def main():
    play()
    # check_colision(Piece("I"), 0, BOARD_HEIGHT - 1)
    # p = Piece("I")
    # print_matrix(p.shape)
    # p.rotate()
    # p.rotate()
    # print_matrix(p.shape)


if __name__ == "__main__":
    main()
