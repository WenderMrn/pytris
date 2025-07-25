from abc import ABC, abstractmethod
from blessed import keyboard

from core.types import GameEvent


class ScreenGame(ABC):
    running = True

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def show_info(self):
        pass

    @abstractmethod
    def handle_event(self, key: keyboard.Keystroke) -> GameEvent:
        pass
