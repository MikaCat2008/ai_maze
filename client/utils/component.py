from __future__ import annotations

from typing import TypeVar, Callable, Optional, TYPE_CHECKING
from inspect import getfullargspec
from pygame.event import Event

T = TypeVar("T")

if TYPE_CHECKING:
    from .entity import Entity


class Component:
    type = None
    
    entity: Optional[Entity]
    handlers: dict[object, Callable]

    update_delta: bool

    def __init__(self) -> None:
        self.entity = None
        self.handlers = {}
        self.update_delta = True

    def notify(self, event: Event) -> None:
        handler = self.handlers.get(event.type)

        if handler:
            handler(event)

    def init(self, entity: Entity) -> None:
        self.entity = entity
        self.update_delta = len(getfullargspec(self.update).args) == 2

    def update(self, delta: float) -> None: ...
    def remove(self) -> None: ...
