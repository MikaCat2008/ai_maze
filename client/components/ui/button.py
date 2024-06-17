import pygame as pg
from pygame.draw import rect
from pygame.font import SysFont
from pygame.event import Event
from utils import Entity, Vector2, Vector4

from ..builtin.box_collider import BoxCollider
from ..builtin.sprite_render import SpriteRender

font = SysFont(None, 24)


class MouseClick:
    pos: Vector2
    type: str

    def __init__(self, pos: Vector2) -> None:
        self.pos = pos
        self.type = "click"


class Button(SpriteRender):
    text: str
    box_collider: BoxCollider

    def __init__(self, size: Vector2, text: str) -> None:
        super().__init__(size, Vector4(0, 0, 0, 0))

        self.text = text
        self.entered = False

        self.handlers[pg.MOUSEMOTION] = self.on_mouse_motion
        self.handlers[pg.MOUSEBUTTONUP] = self.on_mouse_up

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.box_collider = entity.get_component(BoxCollider)

    def on_mouse_motion(self, event: Event) -> None:
        x, y = event.pos

        if self.box_collider.collidepoint((x, y)):
            if not self.entered:
                self.color = Vector4(72, 61, 139)
            
            self.entered = True
        else:
            if self.entered:
                self.color = Vector4(80, 81, 133)

            self.entered = False

    def on_mouse_up(self, event: Event) -> None:
        x, y = event.pos
        
        if self.box_collider.collidepoint((x, y)):
            self.entity.notify(MouseClick(Vector2(x, y)))

    def render(self) -> None:
        super().render()

        w, h = self.size.t

        rect(self.rendered, (255, 255, 255), (0, 0, w, h), 2)

        text = font.render(self.text, None, (255, 255, 255))
        tw, th = text.get_size()

        self.rendered.blit(text, (w / 2 - tw / 2, h / 2 - th / 2))
