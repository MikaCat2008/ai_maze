from typing import Optional
from utils import Entity, instantiate
from prefabs.main_player import MainPlayer

from components.builtin.tile_map import Tile
from components.builtin.transition import Transition


class SpawnPoint(Tile):
    main_player: Optional[Entity]
    
    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.main_player = None

        self.spawn(True)

    def spawn(self, main: bool) -> None:
        if main:
            pos = self.transition.pos.copy()

            self.main_player = instantiate(MainPlayer, pos)

    def remove(self) -> None:
        self.main_player.remove()
