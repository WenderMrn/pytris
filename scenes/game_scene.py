import copy
import time
from typing import List
from blessed import Terminal, keyboard

from config import (
    CONN,
    DEBUG,
    GAME_SPEED,
    BoardValues,
)
from core.drawer import Drawer
from core.screen_game import ScreenGame
from core.types import GameEvent
from entities.board import Board
from entities.piece import Piece

BOARD_OFFSET_X = 0
BOARD_OFFSET_Y = 0


class GameScene(ScreenGame):
    def __init__(self, term: Terminal, player: str):
        self.term = term
        self.player = player
        self.__new_game()

    def __new_game(self):
        self.running = True
        self.pause = False
        self.game_over = False
        self.level = 0
        self.score = 0
        self.lines_cleared = 0
        self.distance_hard_drop = 0
        self.game_speed = GAME_SPEED

        self.falling_block = None
        self.total_fallen_blocks = 0
        self.falling_blocks_queue: List[Piece] = Piece.random_list(2)

        self.board = Board(width=BoardValues.WIDTH, height=BoardValues.HEIGHT)
        self._last_update = time.perf_counter() * 1000

    def __mock(self):
        # teste
        self.board.insert_block(Piece("I", x=0, y=5))
        self.board.insert_block(Piece("I", x=5, y=5))

    def handle_event(self, key: keyboard.Keystroke):
        if self.falling_block:
            try_move = copy.deepcopy(self.falling_block)
            if key.code == self.term.KEY_RIGHT:
                try_move.move("RIGHT")
                collision, _ = self.board.check_next_collision(try_move)
                if not collision:
                    self.falling_block.move("RIGHT")
            elif key.code == self.term.KEY_LEFT:
                try_move.move("LEFT")
                collision, _ = self.board.check_next_collision(try_move)
                if not collision:
                    self.falling_block.move("LEFT")
            elif key.code == self.term.KEY_DOWN:
                self.distance_hard_drop = 0
                while self.falling_block:
                    self.__move_current_block_down()
                    self.distance_hard_drop += 1

            elif key.code == self.term.KEY_UP:
                try_move.rotate()
                collision, _ = self.board.check_next_collision(try_move)

                if not collision:
                    self.falling_block.rotate()

        if key.lower() == "p" and not self.game_over:
            self.pause = not self.pause
        elif key.lower() == "r":
            self.__reset()
        elif key.code == self.term.KEY_ESCAPE or key == r"\x1b":
            self.running = False
            return GameEvent("Esc", "SCREEN_MENU", 0)

    def update(self):
        if self.pause or self.game_over or not self.running:
            return

        now = time.perf_counter() * 1000
        interval = 1000 / self.game_speed

        if now - self._last_update < interval:
            return

        self.__move_current_block_down()
        self.__calculate_score()
        self._last_update = now

    def draw(self):
        self.__draw_game_info()
        self.__draw_total_lines()
        self.__draw_player()

        if self.pause or not self.running:
            return

        Drawer.draw_board(board=self.board)
        Drawer.draw_piece(board=self.board, piece=self.falling_block)

        if DEBUG:
            self.__draw_map(40, 0)

    def show_info(self):
        Drawer.render_game_instructions("GAME", 13, 26)

        if self.pause:
            Drawer.draw_text(
                text="PAUSED",
                center=True,
                bg_color=self.term.on_red,
                offset_y=BoardValues.OFFSET_Y,
                offset_x=BoardValues.OFFSET_X,
            )
        elif self.game_over:
            Drawer.draw_text(
                text="GAME OVER!",
                center=True,
                bg_color=self.term.on_red,
                offset_y=BoardValues.OFFSET_Y,
                offset_x=BoardValues.OFFSET_X,
            )

    def __calculate_score(self):
        yes, count = self.board.check_complete_line()

        if not yes:
            return

        score_per_lines = {1: 40, 2: 200, 3: 300, 4: 1200}

        self.score += score_per_lines.get(count, 0) * max(1, self.level)
        self.score += self.distance_hard_drop * 2
        self.lines_cleared += count
        self.level = max(0, self.lines_cleared // 10)
        self.game_speed = min(GAME_SPEED + (self.level * 0.5), 80)

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
            self.falling_block.move("DOWN")

            has_collision, overflow = self.board.check_next_collision(
                self.falling_block
            )

            if has_collision:
                self.board.insert_block(self.falling_block)
                self.falling_block = None

            if overflow:
                self.game_over = True

                if self.score:
                    CONN.try_save_score(name=str(self.player).upper(), score=self.score)

        else:
            self.total_fallen_blocks += 1
            total_next_blocks = len(self.falling_blocks_queue)

            if total_next_blocks < 2:
                self.falling_blocks_queue.append(Piece.random_new())

            self.falling_block = self.falling_blocks_queue.pop(0)

            time.sleep(0.1)

    def __draw_total_lines(self):
        offset_x = BoardValues.WIDTH * 2 + 10
        offset_y = 1
        Drawer.draw_text(
            text="        LINES       ",
            fg_color=self.term.black,
            bg_color=self.term.on_darkseagreen,
            x=offset_x,
            y=offset_y,
        )
        Drawer.draw_text(
            text=f" {self.lines_cleared}               ",
            x=offset_x,
            y=offset_y + 2,
        )

    def __draw_player(self):
        offset_x = 10
        offset_y = 4
        Drawer.draw_text(
            text="      PLAYER      ",
            fg_color=self.term.black,
            bg_color=self.term.on_darkseagreen,
            x=offset_x,
            y=offset_y,
        )
        Drawer.draw_text(
            text=f" {self.player}    ",
            x=offset_x,
            y=offset_y + 2,
        )

    def __draw_game_info(self):
        next_piece = self.falling_blocks_queue[0]
        next_box_width = BoardValues.WIDTH * 2 + BoardValues.OFFSET_X + 2
        score_y = 4
        next_y = 10
        level_y = next_y + score_y + 4

        Drawer.draw_square(
            width=BoardValues.WIDTH * 2 + 2,
            height=8,
            fill_char=" ",
            start_x=next_box_width,
            start_y=next_y + 1,
        )

        Drawer.draw_text(
            text="         SCORE        ",
            fg_color=self.term.black,
            bg_color=self.term.on_darkseagreen,
            x=next_box_width,
            y=score_y,
        )
        Drawer.draw_text(
            text=f" {self.score}        ",
            x=next_box_width,
            y=score_y + 2,
        )

        Drawer.draw_text(
            text="         NEXT         ",
            fg_color=self.term.black,
            bg_color=self.term.on_darkseagreen,
            x=next_box_width,
            y=next_y,
        )

        if len(self.falling_blocks_queue) > 0:
            offset_x = next_box_width + 8
            offset_y = 2

            next = copy.deepcopy(next_piece)
            next.x = 0
            next.y = 0

            Drawer.draw_piece(
                board=self.board,
                piece=next,
                x=offset_x,
                y=offset_y + next_y,
            )

        Drawer.draw_text(
            text="         LEVEL        ",
            fg_color=self.term.black,
            bg_color=self.term.on_darkseagreen,
            x=next_box_width,
            y=level_y,
        )
        Drawer.draw_text(
            text=f" {self.level}        ",
            x=next_box_width,
            y=level_y + 2,
        )

    def __reset(self):
        self.__new_game()
