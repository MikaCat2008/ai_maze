import pygame as pg
from pygame.surface import Surface
from utils import Vector2, Vector4, Component


class SpriteRender(Component):
    _size: Vector2
    _color: Vector4
    _changed: bool
    rendered: Surface
    invisible: bool

    def __init__(self, size: Vector2, color: Vector4 = None) -> None:
        super().__init__()

        self._size = size
        self._color = color or Vector4(0, 0, 0, 0)
        self._changed = True
        self.invisible = False

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, size: Vector2) -> None:
        self._size = size
        self._changed = True

    @property
    def color(self) -> Vector4:
        return self._color

    @color.setter
    def color(self, color: Vector4) -> None:
        self._color = color
        self._changed = True

    def render(self) -> None:
        self._changed = False
        self.rendered = Surface(self.size.t, pg.SRCALPHA)
        self.rendered.fill(self.color.t)

    def changed(self) -> bool:
        changed = self._changed

        self._changed = False

        return changed
