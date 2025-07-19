import copy
import random
import time
from blessed import Terminal, keyboard
from datetime import datetime

from config import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_WIDTH,
    DEBUG,
    PLAYER_SEED,
    SPEED_GAME,
)
from models.board import Board
from models.color import Color
from models.piece import Piece

BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 0


class GameScene:
    def __init__(self, term: Terminal):
        self.term = term
        self.running = True
        self.pause = False

        self.falling_block = None
        self.prev_falling_block = None
        self.total_fallen_blocks = 0

        self.board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self._last_update = time.perf_counter() * 1000

        # teste
        # self.board.insert_block(Piece("Z", x=17, y=18))
        # self.board.insert_block(Piece("I", x=0, y=19))

    def key_listener(self):
        with self.term.cbreak():
            while True:
                key = self.term.inkey(timeout=0.01)
                if key:
                    self.__handle_event(key)

    def __handle_event(self, key: keyboard.Keystroke):
        now = time.perf_counter() * 1000
        if self.falling_block:
            self.prev_falling_block = copy.deepcopy(self.falling_block)
            if key.code == self.term.KEY_RIGHT:
                self.falling_block.move("RIGHT")
            elif key.code == self.term.KEY_LEFT:
                self.falling_block.move("LEFT")
            elif key.code == self.term.KEY_DOWN:
                self.falling_block.move("DOWN")
            elif key.code == self.term.KEY_UP:
                self.falling_block.rotate()
        else:
            self.prev_falling_block = None

        if key.lower() == "p":
            self.pause = not self.pause
        elif key.lower() == "r":
            self.__reset()
        elif key.lower() == "q":
            self.running = False
            exit(0)

        print(self.term.move_xy(0, 28) + f"key event: code: [{key.code}], now: {now}]")

    def update(self):
        now = time.perf_counter() * 1000
        interval = 1000 / SPEED_GAME

        if self.pause or now - self._last_update < interval:
            return

        self.__get_new_random_block()
        self.board.check_complete_line()
        self._last_update = now

    def draw(self):
        self.__draw_board()
        self.__draw_piece(self.falling_block)

        if DEBUG:
            self.__draw_map(0, 45)

    def __draw_board(self):
        fg = self.term.black
        for i, row in enumerate(self.board.shape):
            for j, val in enumerate(row):
                bg = (
                    Color.color_by_number(val)
                    if val
                    else self.term.on_color_rgb(192, 192, 192)
                )
                print(
                    self.term.move(i, j * CELL_WIDTH)
                    + bg
                    + fg("[]" if val else "::")
                    + self.term.normal
                )

        print(self.term.normal)

    def __draw_piece(self, piece: Piece):
        if not piece:
            return

        print(self.term.move(24, 1) + f"VIRTUAL BLOCK[y,x]: [{piece.y}, {piece.x}] ")

        fg = self.term.black
        for i, row in enumerate(piece.shape):
            for j, val in enumerate(row):
                bg = (
                    Color.color_by_number(val)
                    if val
                    else self.term.on_color_rgb(192, 192, 192)
                )
                py = min(piece.y + i, BOARD_HEIGHT - 1)
                px = min(piece.x + j, BOARD_WIDTH - 1)

                print(
                    self.term.move(py, px * CELL_WIDTH)
                    + bg
                    + fg("[]" if val else "::")
                    + self.term.normal
                )

        print(self.term.normal)

    def __draw_map(self, px=0, py=0):
        fg = self.term.black
        for i, row in enumerate(self.board.shape):
            for j, val in enumerate(row):
                print(
                    self.term.move(px + i, py + j)
                    + fg(f"{val if val else "█"}")
                    + self.term.normal
                )

        print(self.term.normal)

    def __get_new_random_block(self):
        if self.falling_block:
            self.prev_falling_block = copy.deepcopy(self.falling_block)
            self.falling_block.move("DOWN")

            print(
                self.term.move(25, 1)
                + f"NEXT_PIECE[name, y, x]: {self.falling_block.name, self.falling_block.y, self.falling_block.x}   "
            )

            if self.board.check_colision(self.falling_block):
                self.board.insert_block(self.falling_block)
                self.falling_block = None
        else:
            self.total_fallen_blocks += 1
            self.falling_block = Piece.random_new(
                y=0, x=random.randrange(0, BOARD_WIDTH)
            )
            self.falling_block.y -= self.falling_block.height - 1
            # teste
            # self.falling_block = Piece("I", rotation=0, y=0, x=16)

    def __reset(self):
        self.falling_block = None
        self.running = True
        self.tick = 0

        self.total_fallen_blocks = 0
        self.board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT)
