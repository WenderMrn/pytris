import os
import platform
import time

from blessed import Terminal

from config import GAME_SPEED
from core.key_event_observable import KeyEventObservable
from core.screen_manager import ScreenManager


term = Terminal()
key_observable = KeyEventObservable(term)


def resize_terminal(cols=100, rows=30):
    if platform.system() == "Windows":
        os.system(f"mode con: cols={cols} lines={rows}")
    else:
        print(rf"\033[8;{rows};{cols}t")


def run():
    resize_terminal()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        screen_manager = ScreenManager()
        running = True
        time_per_frame = max(1 / GAME_SPEED, 0.01)

        key_observable.subscribe(screen_manager.handle_event)
        key_observable.start()

        print(term.home + term.clear)

        while True:
            screen_manager.update()
            screen_manager.render()
            screen_manager.show_info()

            running = screen_manager.running
            if not running:
                break

            time.sleep(time_per_frame)

        key_observable.stop()
        exit(0)
