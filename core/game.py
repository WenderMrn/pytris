import copy
import threading
import time

from blessed import Terminal

from config import GAME_SPEED
from scenes.game_scene import GameScene

term = Terminal()


def run():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        scene = GameScene(term)
        running = True
        time_per_frame = 1 / GAME_SPEED

        print(term.home + term.clear)

        threading.Thread(target=scene.key_listener, daemon=True).start()

        while running:
            start_time = time.time()
            # Limpa a tela

            if not scene.pause:
                scene.update()
                scene.draw()

            running = scene.running

            elapsed = time.time() - start_time
            # time.sleep(max(0, 1 / 60 - elapsed))
            # time.sleep(max(0, time_per_frame - elapsed))
            time.sleep(time_per_frame)

            # print(term.move(20, 0) + f"Tick: {elapsed}")

        print("exiting....")
        exit(0)
