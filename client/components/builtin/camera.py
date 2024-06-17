from pygame.draw import rect as draw_rect
from pygame.surface import Surface
from utils import Entity, Vector3, Component

from .transition import Transition
from .box_collider import BoxCollider
from .sprite_render import SpriteRender


class Camera(Component):
    screen: Surface
    screen_w: int
    screen_h: int
    transition: Transition
    background: tuple[int, int, int]

    def __init__(self, screen: Surface, background: Vector3 = None) -> None:
        super().__init__()

        self.screen = screen
        self.screen_w, self.screen_h = screen.get_size()
        self.background = background or Vector3(255, 255, 255)

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.transition = entity.get_component(Transition)

    def update(self) -> None:
        x, y = self.transition.pos.t

        for entity in self.entity.manager.get_entities():
            transition = entity.get_component(Transition)
            sprite_render = entity.get_component(SpriteRender)

            if transition and sprite_render:
                if sprite_render.invisible:
                    continue

                if sprite_render.changed():
                    sprite_render.render()

                pos = transition.pos.copy()
                w, h = sprite_render.size.t

                pos.x += self.screen_w / 2 - w / 2 - x
                pos.y = self.screen_h / 2 - h / 2 + y - pos.y

                self.screen.blit(sprite_render.rendered, pos.t)
                
                # box_collider = entity.get_component(BoxCollider)
                # draw_rect(self.screen, (0, 255, 0), (*pos.t, w, h), 1)

                # if box_collider:
                #     for rect in box_collider.get_rects():
                #         rx, ry, rw, rh = rect

                #         rx += self.screen_w / 2 - x
                #         ry = self.screen_h / 2 - rh + y - ry

                #         draw_rect(self.screen, (0, 0, 255), (rx, ry, rw, rh), 1)

    def normalize(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        cx, cy = self.transition.pos.t
        
        return x - self.screen_w / 2 + cx, y - self.screen_h / 2 - cy
