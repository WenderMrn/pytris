import copy
import random
import time
from typing import List
from blessed import Terminal, keyboard

from config import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CELL_WIDTH,
    DEBUG,
    GAME_SPEED,
)
from core.shapes import Shapes
from entities.board import Board
from entities.color import Color
from entities.piece import Piece

BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 0


class GameScene:
    def __init__(self, term: Terminal):
        self.term = term
        self.__new_game()

    def __new_game(self):
        self.running = True
        self.pause = False
        self.game_over = False
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.game_speed = GAME_SPEED

        self.falling_block = None
        self.prev_falling_block = None
        self.total_fallen_blocks = 0
        self.falling_blocks_queue: List[Piece] = Piece.random_list(2)

        self.board = Board(width=BOARD_WIDTH, height=BOARD_HEIGHT)
        self._last_update = time.perf_counter() * 1000

        # self.__mock()

    def __mock(self):
        # teste
        self.board.insert_block(Piece("I", x=0, y=5))
        self.board.insert_block(Piece("I", x=5, y=5))

    def key_listener(self):
        with self.term.cbreak():
            while True:
                key = self.term.inkey(timeout=0.01)
                if key:
                    self.__handle_event(key)

    def __handle_event(self, key: keyboard.Keystroke):
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
            # elif key.lower() == "c":
            #     piece = copy.deepcopy(self.falling_block)

            #     self.falling_block = Piece.random_new()
            #     self.falling_block.x = piece.x
            #     self.falling_block.y = piece.y
        else:
            self.prev_falling_block = None

        if key.lower() == "p" and not self.game_over:
            self.pause = not self.pause
        elif key.lower() == "r":
            self.__reset()
        elif key.lower() == "q":
            self.running = False
            exit(0)

        # print(self.term.move_xy(0, 28) + f"key event: code: [{key.code}], now: {now}]")

    def update(self):
        now = time.perf_counter() * 1000
        interval = 1000 / self.game_speed

        if (
            self.pause
            or self.game_over
            or not self.running
            or now - self._last_update < interval
        ):
            return

        self.__move_current_block_down()
        self.__calculate_score()
        self._last_update = now

    def draw(self):
        if self.pause or not self.running or not self.running:
            return

        self.__draw_board()
        self.__draw_piece(self.falling_block)
        self.__draw_game_info()

        if DEBUG:
            self.__draw_map(40, 0)

    def show_messages(self):
        if self.pause:
            Shapes.draw_text(text="PAUSED", center=True, bg=self.term.on_red)
        elif self.game_over:
            Shapes.draw_text(text="GAME OVER!", center=True, bg=self.term.on_red)

    def __calculate_score(self):
        yes, count = self.board.check_complete_line()
        # print(
        #     self.term.move_xy(80, 1)
        #     + f"Score: {self.score}, level: {self.level}, yes: {yes}, count: {count}, speed: {self.game_speed}, lines: {self.lines_cleared}"
        #     + " " * 5
        # )

        if not yes:
            return

        score_per_lines = {1: 40, 2: 200, 3: 300, 4: 1200}

        self.score += score_per_lines.get(count, 0) * max(1, self.level)
        self.lines_cleared += count
        self.level = max(0, self.lines_cleared // 10)
        self.game_speed = min(GAME_SPEED + (self.level * 0.25), 80)

    def __draw_board(self):
        fg = self.term.black
        for py, row in enumerate(self.board.shape):
            for px, val in enumerate(row):
                bg = (
                    Color.color_by_number(val)
                    if val
                    else self.term.on_color_rgb(192, 192, 192)
                )

                print(
                    self.term.move_xy(px * CELL_WIDTH, py)
                    + bg
                    + fg("[]" if val else "::")
                    + self.term.normal
                )

        print(self.term.normal)

    def __draw_piece(self, piece: Piece, offset_x=0, offset_y=0):
        if not piece:
            return

        fg = self.term.black
        for y, row in enumerate(piece.shape):
            for x, val in enumerate(row):
                bg = (
                    Color.color_by_number(val)
                    if val
                    else self.term.on_color_rgb(192, 192, 192)
                )
                py = piece.y + y + offset_y
                px = piece.x + x + offset_x

                if (
                    val
                    and (py >= 0 and py < self.board.height + offset_y)
                    and (px >= 0 and px < self.board.width + offset_x)
                ):
                    print(
                        self.term.move_xy(px * CELL_WIDTH, py)
                        + bg
                        + fg("[]" if val else "::")
                        + self.term.normal
                    )

        print(self.term.normal)

    def __draw_map(self, offset_px=0, offset_py=0):
        fg = self.term.black
        for i, row in enumerate(self.board.shape):
            for j, val in enumerate(row):
                print(
                    self.term.move_xy(j + offset_px, i + offset_py)
                    + fg(f"{val if val else "█"}")
                    + self.term.normal
                )

        print(self.term.normal)

    def __move_current_block_down(self):
        if self.falling_block:
            self.prev_falling_block = copy.deepcopy(self.falling_block)
            self.falling_block.move("DOWN")

            has_collision, overflow = self.board.check_next_collision(
                self.falling_block
            )
            if overflow:
                self.board.insert_block(self.falling_block)
                self.falling_block = None
                self.game_over = True
            elif has_collision:
                self.board.insert_block(self.falling_block)
                self.falling_block = None

        else:
            self.total_fallen_blocks += 1
            total_next_blocks = len(self.falling_blocks_queue)

            if total_next_blocks < 2:
                self.falling_blocks_queue.append(Piece.random_new())

            self.falling_block = self.falling_blocks_queue.pop(0)

            time.sleep(0.1)

    def __draw_game_info(self):
        next_piece = self.falling_blocks_queue[0]
        next_box_width = BOARD_WIDTH * 2 + 2
        score_y = 1
        next_y = 5
        level_y = next_y + score_y + 8
        lines_y = level_y + 3

        Shapes.draw_square(
            width=next_box_width,
            height=20,
            fill_char=" ",
            start_x=next_box_width,
            start_y=0,
        )

        Shapes.draw_text(
            text="         SCORE        ",
            bg=self.term.on_black,
            x=next_box_width,
            y=score_y,
        )
        Shapes.draw_text(
            text=f" {self.score}",
            x=next_box_width,
            y=score_y + 1,
        )

        Shapes.draw_text(
            text="         NEXT         ",
            bg=self.term.on_black,
            x=next_box_width,
            y=next_y,
        )
        if len(self.falling_blocks_queue) > 0:
            offset_x = next_box_width + 3
            offset_y = 2

            next = copy.deepcopy(next_piece)
            next.x = 0
            next.y = 0

            self.__draw_piece(next, offset_x - 10, offset_y + next_y)

        Shapes.draw_text(
            text="         LEVEL        ",
            bg=self.term.on_black,
            x=next_box_width,
            y=level_y,
        )
        Shapes.draw_text(
            text=f" {self.level}",
            x=next_box_width,
            y=level_y + 1,
        )

        Shapes.draw_text(
            text="         LINES        ",
            bg=self.term.on_black,
            x=next_box_width,
            y=lines_y,
        )
        Shapes.draw_text(
            text=f" {self.lines_cleared}",
            x=next_box_width,
            y=lines_y + 1,
        )

    def __reset(self):
        self.__new_game()
