from utils import GameObject, GameComponent

from .builtin.tile_map import Tile


class FinishPoint(Tile, GameComponent):
    main_player: GameObject
    maze_generator: GameObject

    def init(self, game_object: GameObject) -> None:
        super().init(game_object)

        self.main_player = None
        self.maze_generator = None
        self.main_player_box_collider = None

    def update(self) -> None:
        if self.main_player is None:
            self.main_player = self.game_object.manager.get_entity_by_tag("MainPlayer")
            self.main_player_box_collider = self.main_player.box_collider
        elif self.maze_generator is None:
            self.maze_generator = self.game_object.manager.get_entity_by_tag("MazeGenerator")
        else:
            if self.box_collider.collidewith(self.main_player_box_collider):
                self.maze_generator.get_component("MazeGenerator").generate()
