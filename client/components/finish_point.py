from utils import Vector4, Entity, Component

from .builtin.tile_map import Tile
from .builtin.box_collider import BoxCollider
from .builtin.sprite_render import SpriteRender


class FinishPoint(Tile):
    main_player: Entity
    maze_generator: Entity

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.main_player = None
        self.box_collider = entity.get_component(BoxCollider)
        self.maze_generator = None
        self.main_player_box_collider = None

    def update(self) -> None:
        if self.main_player is None:
            self.main_player = self.entity.manager.get_entity_by_tag("MainPlayer")
            self.main_player_box_collider = self.main_player.get_component(BoxCollider)
        elif self.maze_generator is None:
            self.maze_generator = self.entity.manager.get_entity_by_tag("MazeGenerator")
        else:
            if self.box_collider.collidewith(self.main_player_box_collider):
                self.maze_generator.get_component("MazeGenerator").generate()
