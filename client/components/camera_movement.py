from utils import Entity, Component, GameObject

from .builtin.transition import Transition


class CameraMovement(Component):
    camera: GameObject
    main_player: GameObject

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.camera = entity.manager.get_entity_by_tag("Camera")
        self.main_player = None

    def update(self) -> None:
        if self.main_player is None:
            self.main_player = self.entity.manager.get_entity_by_tag("MainPlayer")

            if self.main_player:
                self.main_player.transition = self.main_player.transition
        else:
            self.camera.transition.pos = self.main_player.transition.pos
