from collections import namedtuple
from config import TERM
from core.drawer import Drawer
from core.screen_game import ScreenGame
from core.types import GameEvent


class GameMenu(ScreenGame):
    def __init__(self):
        self.__update_draw = True
        self.__selected_item: int = None
        self.__current_item: int = 1
        self.__options = self.__menu_options()

    def draw(self):
        pass
        if self.__update_draw:
            self.__draw_backgorund()

    def show_info(self):
        pass

    def update(self):
        pass

    def handle_event(self, key):
        if key.code == TERM.KEY_DOWN:
            self.__current_item = min(len(self.__options), self.__current_item + 1)
            self.__update_draw = True
        elif key.code == TERM.KEY_UP:
            self.__current_item = max(1, self.__current_item - 1)
            self.__update_draw = True
        elif key.code == TERM.KEY_ENTER:
            self.__selected_item = self.__current_item
            self.__update_draw = True
            return self.__options[self.__current_item - 1]

    @property
    def selected_menu_item(self):
        return self.__selected_item

    def __menu_options(self):
        return [
            GameEvent("New Game", "SCREEN_NEW_GAME", 1),
            GameEvent("Top Scores", "SCREEN_TOP_SCORES", 2),
            GameEvent("QUIT", "QUIT", 3),
        ]

    def __draw_backgorund(self):
        if not self.__current_item:
            return

        Drawer.clear_screen()
        Drawer.render_game_instructions()

        offset_x = 20
        offset_screen_y = 2
        offset_arrow_y = (offset_screen_y + 1) * self.__current_item
        offset_menu_y = 8

        Drawer.draw_square(
            width=52,
            height=22,
            fill_char=" ",
            start_x=offset_x,
            start_y=offset_screen_y,
            bg_color=TERM.on_darkseagreen,
        )

        Drawer.render_text(
            text="Pytris ",
            fg_color=TERM.black,
            bg_color=TERM.on_darkseagreen,
            x=offset_x + 1,
            y=offset_screen_y,
        )
        Drawer.draw_text(
            text="+" * 50,
            x=offset_x + 1,
            y=offset_screen_y + 6,
            fg=TERM.black,
            bg=TERM.on_darkseagreen,
        )

        for y, item in enumerate(self.__options):
            Drawer.render_block_text(
                text=item.label,
                x=offset_x + 12,
                y=offset_screen_y + (y * 5) + offset_menu_y,
                fg_color=(
                    TERM.black if self.__current_item != y + 1 else TERM.palegreen1
                ),
                bg_color=TERM.on_darkseagreen,
            )

        Drawer.render_block_text(
            text=">",
            x=offset_x + 5,
            y=offset_arrow_y + offset_menu_y - 1,
            fg_color=TERM.palegreen1,
            bg_color=TERM.on_darkseagreen,
        )

        self.__update_draw = False
