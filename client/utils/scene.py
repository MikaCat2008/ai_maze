from __future__ import annotations

from typing import TYPE_CHECKING
from .entity import Entity
from .component import Component
from .game_object import GameObject
from .entity_manager import EntityManager

if TYPE_CHECKING:
    from .scene_manager import SceneManager


class Scene:
    name: str
    inited: bool
    manager: SceneManager
    entity_manager: EntityManager

    def __init__(self, name: str, manager: SceneManager) -> None:
        self.name = name
        self.inited = False
        self.manager = manager
        self.entity_manager = EntityManager(self)

    def create(self, components: list[Component], tag: str = None) -> Entity:
        return self.entity_manager.create(components, tag, cls=GameObject)

    def init(self) -> None:
        self.inited = True

        for entity in self.entity_manager.get_entities():
            entity.init_components()
