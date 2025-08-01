from config import TERM, GameEventName
from core.drawer import Drawer
from core.screen_game import ScreenGame
from scenes.game_menu import GameMenu
from scenes.game_scene import GameScene
from scenes.new_game import NewGame
from scenes.top_scores import TopScores


class ScreenManager:
    def __init__(self):
        self.current_screen = GameMenu()

    def change_screen(self, new_screen: ScreenGame):
        Drawer.clear_screen()
        self.current_screen = new_screen
        self.current_screen.running = True

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
            if event.name == GameEventName.SCREEN_NEW_GAME:
                self.change_screen(NewGame())
            elif event.name == GameEventName.SCREEN_MENU:
                self.change_screen(GameMenu())
            elif event.name == GameEventName.SCREEN_START_GAME:
                self.change_screen(GameScene(term=TERM, player=event.value))
            elif event.name == GameEventName.SCREEN_TOP_SCORES:
                self.change_screen(TopScores())
            elif event.name == GameEventName.QUIT_GAME:
                self.current_screen.running = False
