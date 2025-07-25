import threading
from typing import Callable, List
from blessed import Terminal, keyboard


class KeyEventObservable:
    def __init__(self, term: Terminal):
        self._term = term
        self._observers: List[Callable[[keyboard.Keystroke], None]] = []
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def subscribe(self, callback: Callable[[keyboard.Keystroke], None]):
        with self._lock:
            self._observers.append(callback)

    def unsubscribe(self, callback: Callable[[keyboard.Keystroke], None]):
        with self._lock:
            if callback in self._observers:
                self._observers.remove(callback)

    def _notify_all(self, key: keyboard.Keystroke):
        with self._lock:
            for observer in self._observers:
                try:
                    observer(key)
                except Exception as e:
                    print(f"[ERROR] Observer failed: {e}")

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)

    def _listen_loop(self):
        with self._term.cbreak():
            while self._running:
                key = self._term.inkey(timeout=0.1)  # non-blocking
                if key:
                    self._notify_all(key)
