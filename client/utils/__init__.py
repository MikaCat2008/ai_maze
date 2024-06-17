from json import load
from typing import Type

from .scene import Scene as Scene
from .entity import Entity as Entity
from .prefab import Prefab as Prefab
from .vectors import Vector2 as Vector2, Vector3 as Vector3, Vector4 as Vector4
from .component import Component as Component
from .scene_manager import SceneManager as SceneManager
from .entity_manager import EntityManager as EntityManager


def instantiate(prefab: Type[Prefab], pos: Vector2, **kwds) -> Entity:
    manager = SceneManager.get_instance().current.entity_manager

    entity = manager.create(*prefab().init(pos, **kwds))
    entity.init_components()

    return entity


def load_json(path: str) -> dict:
    with open(path) as f:
        return load(f)
