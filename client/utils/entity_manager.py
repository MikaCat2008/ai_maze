from __future__ import annotations

from typing import Type, Optional, TYPE_CHECKING
from collections import defaultdict
from pygame.event import Event

from .entity import Entity
from .component import Component

if TYPE_CHECKING:
    from .scene import Scene


class EntityManager:
    entities: defaultdict[str, list[Entity]]

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.entities = defaultdict(list)

    def notify(self, event: Event) -> None:
        for entity in self.get_entities():
            entity.notify(event)

    def update(self, delta: float) -> None:
        for entity in self.get_entities():
            entity.update(delta)

    def create(self, components: list[Component], tag: str = None, cls: Type[Entity] = Entity) -> Entity:
        entity = cls()
        entity.init(tag, self)

        self.entities[tag].append(entity)

        for component in components:
            entity.add_component(component)

        return entity

    def get_entities(self) -> list[Entity]:
        entities = []

        for _entities in self.entities.values():
            entities.extend(_entities)

        return entities

    def get_entities_by_tag(self, tag: str) -> list[Entity]:
        return self.entities[tag]

    def get_entity_by_tag(self, tag: str) -> Optional[Entity]:
        entity_list = self.get_entities_by_tag(tag)

        if entity_list:
            return entity_list[0]
        return None

    def remove_entity(self, entity: Entity) -> None:
        self.entities[entity.tag].remove(entity)
