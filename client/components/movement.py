from __future__ import annotations

from typing import TYPE_CHECKING
from utils import Vector2, Entity, Component

from .builtin.input import Input
from .builtin.box_collider import BoxCollider


class Movement(Component):
    speed: int
    input: Input
    box_collider: BoxCollider
    
    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.speed = 200
        self.input = entity.manager.get_entity_by_tag("Input").get_component(Input)
        self.box_collider = entity.get_component(BoxCollider)

    def update(self, delta: float) -> None:
        move = Vector2()
        speed = self.speed * delta

        if self.input.pressed.up:
            move.y += speed
        if self.input.pressed.down:
            move.y -= speed
        if self.input.pressed.left:
            move.x -= speed
        if self.input.pressed.right:
            move.x += speed

        if move.x or move.y:
            self.box_collider.update_collision(move)
