from typing import List
from config import CONN, TERM
from core.db import Db
from core.drawer import Drawer
from core.screen_game import ScreenGame
from core.types import GameEvent, Score


class TopScores(ScreenGame):
    def __init__(self):
        self.scores = CONN.get_all_scores()
        self.__update_draw = True

    def draw(self):
        if not self.__update_draw:
            return

        offset_x = 20
        Drawer.draw_square(
            width=50,
            height=20,
            fill_char=" ",
            start_x=offset_x,
            start_y=4,
            bg_color=TERM.on_darkseagreen,
        )

        Drawer.render_block_text(
            text="Best Scores",
            x=offset_x + 4,
            y=5,
            fg_color=TERM.black,
            bg_color=TERM.on_darkseagreen,
        )

        scores = sorted(self.scores, key=lambda s: s.value, reverse=True)
        for i, score in enumerate(scores[:5]):
            dots_size = 35 - min(len(score.name) + len(str(score.value)), 35)
            Drawer.draw_text(
                text=f"{i+1}. {str(score.name).upper()} "
                + "." * dots_size
                + f" {score.value}",
                x=offset_x + 4,
                y=10 + i,
                fg=TERM.black,
                bg=TERM.on_darkseagreen,
            )

        if len(scores) == 0:
            Drawer.draw_text(
                text=f"No scores",
                x=offset_x + 4,
                y=10,
                fg=TERM.black,
                bg=TERM.on_darkseagreen,
            )

        self.__update_draw = False

    def update(self):
        return super().update()

    def show_info(self):
        return super().show_info()

    def handle_event(self, key):
        if key.code == TERM.KEY_ESCAPE or key == "\x1b":
            return GameEvent("Esc", "SCREEN_MENU", 0)
