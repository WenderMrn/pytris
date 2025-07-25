from config import TERM
from core.drawer import Drawer
from core.screen_game import ScreenGame
from core.types import GameEvent


class NewGame(ScreenGame):
    def __init__(self):
        self.player = ""
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

        Drawer.draw_square(
            width=50,
            height=5,
            fill_char=" ",
            start_x=offset_x,
            start_y=9,
            bg_color=TERM.on_lightyellow3,
        )

        Drawer.render_block_text(
            text="Name: ",
            x=offset_x + 4,
            y=5,
            fg_color=TERM.black,
            bg_color=TERM.on_darkseagreen,
        )

        Drawer.render_block_text(
            text=self.player,
            x=offset_x + 4,
            y=10,
            fg_color=TERM.black,
            bg_color=TERM.on_lightyellow3,
        )

        self.__update_draw = False

    def update(self):
        return super().update()

    def show_info(self):
        return super().show_info()

    def handle_event(self, key):
        if key.code in (TERM.KEY_ENTER, TERM.KEY_RETURN) and self.player:
            return GameEvent("Start Game", "SCREEN_START_GAME", self.player)
        elif key.code == TERM.KEY_BACKSPACE:
            self.player = self.player[:-1]
            self.__update_draw = True
        elif (key.isalnum() or key == " ") and len(self.player) <= 10:
            self.player += key.upper()
            self.__update_draw = True
        elif key.code == TERM.KEY_ESCAPE or key == "\x1b":
            return GameEvent("Esc", "SCREEN_MENU", 0)
