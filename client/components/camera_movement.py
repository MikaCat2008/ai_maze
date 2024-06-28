from utils import Entity, GameComponent, GameObject


class CameraMovement(GameComponent):
    camera: GameObject
    main_player: GameObject

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.camera = entity.manager.get_entity_by_tag("Camera")
        self.main_player = None

    def update(self) -> None:
        if self.main_player is None:
            self.main_player = self.entity.manager.get_entity_by_tag("MainPlayer")
        else:
            self.camera.transition.pos = self.main_player.transition.pos
