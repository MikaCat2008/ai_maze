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
        pos = Vector2(x + mx, y + my)

        self._update_collision(w, None, mx, None, pos, self.get_rects(mx, 0))
        self._update_collision(None, h, None, my, pos, self.get_rects(0, my))

        self.transition.pos = pos

    def _update_collision(
        self, w: int, h: int, mx: int, my: int, pos: Vector2, rects: list[Rect]
    ) -> None:
        for entity in self.entity.manager.get_entities():
            box_collider = entity.get_component(BoxCollider)

            if box_collider is None or box_collider is self or not box_collider.collision:
                continue

            for rect in rects:
                for _rect in box_collider.get_rects():
                    if rect.colliderect(_rect):
                        if mx is not None:
                            if mx > 0:
                                pos.x = _rect.left - w / 2
                            elif mx < 0:
                                pos.x = _rect.right + w / 2
                        if my is not None:
                            if my > 0:
                                pos.y = _rect.top - h / 2
                            elif my < 0:
                                pos.y = _rect.bottom + h / 2

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
