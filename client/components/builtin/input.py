import pygame as pg
from pygame.event import Event
from utils import Entity, Component


class Actions:
    def __init__(self) -> None:
        self.up = False
        self.left = False
        self.down = False
        self.right = False

    def get_str(self, direction: str) -> bool:
        return getattr(self, direction)

    def set_str(self, direction: str, value: bool) -> None:
        setattr(self, direction, value)


class Input(Component):
    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.action_keys = { 119: "up", 97: "left", 115: "down", 100: "right" }
        self.clicked = Actions()
        self.pressed = Actions()
        self.keys = {}

        self.handlers[pg.KEYUP] = self.on_keyup
        self.handlers[pg.KEYDOWN] = self.on_keydown

    def on_keyup(self, event: Event) -> None:
        self.keys[event.key] = False

    def on_keydown(self, event: Event) -> None:
        self.keys[event.key] = True

    def update(self) -> None:
        for key, value in self.keys.items():
            action = self.action_keys.get(key)

            if action is None:
                continue
            
            if not value:
                self.clicked.set_str(action, False)
                self.pressed.set_str(action, False)

                continue

            clicked = self.clicked.get_str(action)
            pressed = self.pressed.get_str(action)

            if clicked:
                self.clicked.set_str(action, False)
            elif not pressed:
                self.clicked.set_str(action, True)

            self.pressed.set_str(action, True)
