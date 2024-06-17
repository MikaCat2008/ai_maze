from utils import Vector2, Component


class Transition(Component):
    pos: Vector2

    def __init__(self, pos: Vector2) -> None:
        super().__init__()

        self.pos = pos
