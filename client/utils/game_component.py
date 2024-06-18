from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from utils import Component
from .game_object import GameObject

if TYPE_CHECKING:
    from components.builtin.transition import Transition
    from components.builtin.box_collider import BoxCollider
    from components.builtin.sprite_render import SpriteRender


class GameComponent(Component):
    _transition: Optional[Transition]
    _box_collider: Optional[BoxCollider]
    _sprite_render: Optional[SpriteRender]

    def init(self, game_object: GameObject) -> None:
        super().init(game_object)

        self._transition = None
        self._box_collider = None
        self._sprite_render = None

    @property
    def game_object(self) -> GameObject:
        return self.entity

    @property
    def transition(self) -> Optional[Transition]:
        if self._transition is None:
            self._transition = self.game_object.get_component("Transition")
        
        return self._transition

    @property
    def box_collider(self) -> Optional[BoxCollider]:
        if self._box_collider is None:
            self._box_collider = self.game_object.get_component("BoxCollider")

        return self._box_collider

    @property
    def sprite_render(self) -> Optional[SpriteRender]:
        if self._sprite_render is None:
            self._sprite_render = self.game_object.get_component("SpriteRender")

        return self._sprite_render
