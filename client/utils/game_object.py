from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from .entity import Entity

if TYPE_CHECKING:
    from components.builtin.transition import Transition
    from components.builtin.box_collider import BoxCollider
    from components.builtin.sprite_render import SpriteRender


class GameObject(Entity):
    @property
    def transition(self) -> Optional[Transition]:
        return self.get_component("Transition")

    @property
    def box_collider(self) -> Optional[BoxCollider]:
        return self.get_component("BoxCollider")

    @property
    def sprite_render(self) -> Optional[SpriteRender]:
        return self.get_component("SpriteRender")
