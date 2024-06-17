from utils import Entity, Component

from .builtin.transition import Transition


class CameraMovement(Component):
    camera: Entity
    main_player: Entity
    camera_transition: Transition
    main_player_transition: Transition

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.camera = entity.manager.get_entity_by_tag("Camera")
        self.main_player = None
        self.camera_transition = self.camera.get_component(Transition)
        self.main_player_transition = None

    def update(self) -> None:
        if self.main_player is None:
            self.main_player = self.entity.manager.get_entity_by_tag("MainPlayer")

            if self.main_player:
                self.main_player_transition = self.main_player.get_component(Transition)
        else:
            self.camera_transition.pos = self.main_player_transition.pos
