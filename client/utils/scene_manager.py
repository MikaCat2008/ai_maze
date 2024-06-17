from typing import Optional

from .scene import Scene
from .entity import Entity
from .component import Component


class SceneManager:
    scenes: dict[str, Scene]
    current: Optional[Scene]
    _instance: "SceneManager" = None

    def __init__(self) -> None:
        self.scenes = {}
        self.current = None
        self.set_instance(self)

    def create(self, entities_setup: list[tuple[list[Component], Optional[str]]], name: str) -> Scene:
        scene = Scene(name, self)

        for entity_setup in entities_setup:
            components, tag = entity_setup
            
            scene.create(components, tag)

        self.scenes[name] = scene

        return scene

    def set_current(self, scene: Scene | str) -> None:        
        if isinstance(scene, str):
            scene = self.get_scene_by_name(scene)
        
        self.current = scene

        if not scene.inited:
            scene.init()
        
    def get_scene_by_name(self, name: str) -> Optional[Scene]:
        return self.scenes.get(name)

    @classmethod
    def get_instance(cls) -> "SceneManager":
        return cls._instance

    @classmethod
    def set_instance(cls, instance: "SceneManager") -> None:
        cls._instance = instance
