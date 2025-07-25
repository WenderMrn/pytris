from collections import namedtuple
import sys
from config import TERM
from core.db import Db
from core.drawer import Drawer
from core.screen_game import ScreenGame
from core.types import Score
from scenes.game_menu import GameMenu
from scenes.game_scene import GameScene
from scenes.new_game import NewGame
from scenes.top_scores import TopScores


class ScreenManager:
    def __init__(self):
        self.current_screen = GameMenu()
        # self.current_screen = GameScene(term=TERM, player="Wender", db=db)

    def change_screen(self, new_screen: ScreenGame):
        self.current_screen = new_screen

    def update(self):
        self.current_screen.update()

    def render(self):
        self.current_screen.draw()

    def show_info(self):
        self.current_screen.show_info()

    @property
    def running(self):
        return self.current_screen.running

    def handle_event(self, key):
        event = self.current_screen.handle_event(key)

        if event:
            if event.name == "SCREEN_NEW_GAME":
                Drawer.clear_screen()
                self.current_screen = NewGame()
            elif event.name == "SCREEN_MENU":
                Drawer.clear_screen()
                self.current_screen = GameMenu()
            elif event.name == "SCREEN_SCORES":
                Drawer.clear_screen()
                pass
            elif event.name == "SCREEN_START_GAME":
                Drawer.clear_screen()
                self.current_screen = GameScene(term=TERM, player=event.value)
            elif event.name == "SCREEN_TOP_SCORES":
                Drawer.clear_screen()
                self.current_screen = TopScores()
            elif event.name == "QUIT":
                self.current_screen.running = False
