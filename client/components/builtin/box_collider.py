from pygame.rect import Rect
from utils import Vector2, Entity, Component

from .transition import Transition
from .sprite_render import SpriteRender


class BoxCollider(Component):
    rects: list[Rect]
    collision: bool
    transition: Transition
    sprite_render: SpriteRender

    def __init__(self, rects: list[Rect], collision: bool = True) -> None:
        super().__init__()

        self.rects = rects
        self.collision = collision  

    def init(self, entity: Entity) -> None:
        super().init(entity)
        
        self.transition = entity.get_component(Transition)
        self.sprite_render = entity.get_component(SpriteRender)

    def update_collision(self, move: Vector2) -> None:
        mx, my = move.t
        x, y = self.transition.pos.t
        w, h = self.sprite_render.size.t
        x += mx
        y += my

        rects = self.get_rects(mx, 0)

        for entity in self.entity.manager.get_entities():
            box_collider = entity.get_component(BoxCollider)

            if box_collider is None or box_collider is self or not box_collider.collision:
                continue

            for rect in rects:
                for _rect in box_collider.get_rects():
                    if rect.colliderect(_rect):
                        if mx > 0:
                            x = _rect.left - w / 2
                        elif mx < 0:
                            x = _rect.right + w / 2

        rects = self.get_rects(0, my)

        for entity in self.entity.manager.get_entities():
            box_collider = entity.get_component(BoxCollider)

            if box_collider is None or box_collider is self or not box_collider.collision:
                continue

            for rect in rects:
                for _rect in box_collider.get_rects():
                    if rect.colliderect(_rect):
                        if my > 0:
                            y = _rect.top - h / 2
                        elif my < 0:
                            y = _rect.bottom + h / 2

        self.transition.pos = Vector2(x, y)

    def get_rects(self, mx: int = 0, my: int = 0) -> list[Rect]:
        x, y = self.transition.pos.t
        w, h = self.sprite_render.size.t

        return [ 
            Rect(
                x + w * ox + mx - w * ow / 2, 
                y + h * oy + my - h * oh / 2, 
                w * ow, h * oh
            )
            for ox, oy, ow, oh in self.rects 
        ]

    def collidepoint(self, point: tuple[int, int]) -> bool:
        return any(rect.collidepoint(point) for rect in self.get_rects())

    def colliderect(self, rect: tuple[int, int]) -> bool:
        return any(_rect.colliderect(rect) for _rect in self.get_rects())
    
    def collidewith(self, box_collider: "BoxCollider") -> bool:
        for rect in self.get_rects():
            for _rect in box_collider.get_rects():
                if rect.colliderect(_rect):
                    return True
        
        return False
