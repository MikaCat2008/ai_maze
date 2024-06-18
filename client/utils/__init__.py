from json import load as _load_json
from typing import Type
from pygame.image import load as _load_image
from pygame.transform import scale

from .scene import Scene as Scene
from .entity import Entity as Entity
from .prefab import Prefab as Prefab
from .vectors import Vector2 as Vector2, Vector3 as Vector3, Vector4 as Vector4
from .component import Component as Component
from .game_object import GameObject as GameObject
from .scene_manager import SceneManager as SceneManager
from .entity_manager import EntityManager as EntityManager
from .game_component import GameComponent as GameComponent


def instantiate(prefab: Type[Prefab], pos: Vector2, **kwds) -> GameObject:
    manager = SceneManager.get_instance().current.entity_manager

    game_object = manager.create(*prefab().init(pos, **kwds), cls=GameObject)
    game_object.init_components()

    return game_object


def load_json(path: str) -> dict:
    with open(path) as f:
        return _load_json(f)


def load_image(path: str, size: tuple[int, int]) -> dict:
    return scale(_load_image(path).convert_alpha(), size)
