from __future__ import annotations

from typing import Type, Optional, TypeVar, TYPE_CHECKING
from pygame.event import Event

from .component import Component

if TYPE_CHECKING:
    from .entity_manager import EntityManager

T = TypeVar("T", bound=Component)


class Entity:
    tag: Optional[str]
    inited: bool
    manager: Optional[EntityManager]    
    components: dict[Type[Component], Component]

    def __init__(self) -> None:
        self.tag = None
        self.inited = False
        self.manager = None
        self.components = {}

    def init(self, tag: str, manager: EntityManager) -> Entity:
        self.tag = tag
        self.inited = True
        self.manager = manager

        return self
    
    def init_components(self) -> None:
        for component in self.components.values():
            component.init(self)

    def notify(self, event: Event) -> None:
        for component in self.components.values():
            component.notify(event)

    def update(self, delta: float) -> None:
        for component in self.components.values():
            if component.update_delta:
                component.update(delta)
            else:
                component.update()

    def add_component(self, component: T) -> T:
        self.components[type(component)] = component

        return component

    def get_component(self, component: Type[T] | str) -> Optional[T]:
        if isinstance(component, str):
            component_list = [
                _component for _component in self.components.values() 
                if _component.__class__.__name__ == component
            ]
        else:
            component_list = [
                _component for _component in self.components.values() 
                if isinstance(_component, component)
            ]

        if component_list:
            return component_list[0]
        return None

    def remove(self) -> None:
        for component in self.components.values():
            component.remove()

        self.manager.remove_entity(self)

    def extend(self, components: list[Component]) -> Entity:
        for component in components:
            self.add_component(component)

        return self
