from typing import Callable
from threading import Thread, current_thread

callbacks = {}


class Callback:
    data: dict

    def __init__(self, f: Callable, *args) -> None:
        self.f = f
        self.data = args[1]["data"]
        self.thread = Thread(target=f, args=args)
        self.thread.start()
        callbacks[self.thread.ident] = self


def current_callback() -> Callback:
    thread = current_thread()
    
    return callbacks[thread.ident]
