from typing import Type, Optional
from pygame.draw import rect as draw_rect
from utils import Prefab, Entity, Vector2, Vector3, Component, instantiate

from .transition import Transition
from .box_collider import BoxCollider
from .sprite_render import SpriteRender


class Tile(Component):
    type: str
    color: str

    def __init__(self, type: str, color: Vector3 = None) -> None:
        super().__init__()

        self.type = type
        self.color = color or Vector3()


class TileType:
    tag: str
    type: Optional[str]
    size: Optional[int]
    color: Vector3
    rects: list[list[tuple[int, int, int, int]]]
    collision: bool

    def __init__(
        self,
        type: str = None,
        size: int = None,
        tag: str = "Tile",
        color: Vector3 = None,
        rects: list[list[tuple[int, int, int, int]]] = None,
        collision: bool = False
    ) -> None:
        self.tag = tag
        self.type = type
        self.size = size
        self.color = color or Vector3()
        self.rects = rects or [[ 0, 0, 1, 1 ]]
        self.collision = collision


class TilePrefab(Prefab):
    def init(self, pos: Vector2, cls: Type[Tile], type: TileType) -> tuple[list[Component], str]:
        return (
            [
                cls(type.type, type.color),
                TileRender(Vector2(type.size, type.size)),
                Transition(pos),
                BoxCollider(type.rects, type.collision)
            ], 
            type.tag
        )


class TileMap(Component):
    type = "TileMap"

    tiles: list[Entity]
    tile_size: int
    tile_types: dict[str, TileType]

    def __init__(self, tile_size: int, tile_types: dict[str, TileType]) -> None:
        super().__init__()

        self.tiles = []
        self.tile_size = tile_size
        self.tile_types = tile_types
        
        for type, tile_type in tile_types.items():
            if tile_type.type is None:
                tile_type.type = type
            if tile_type.size is None:
                tile_type.size = tile_size

    def add_tile(self, pos: Vector2, type: str, cls: Type[Tile] = Tile) -> None:
        x, y = pos.t
        tile_type = self.tile_types[type]
        
        tile = instantiate(
            TilePrefab, Vector2(x * self.tile_size, y * self.tile_size), cls=cls, type=tile_type
        )
        
        self.tiles.append(tile)

        return tile
    
    def clear(self) -> None:
        for tile in self.tiles:
            tile.remove()
        
        self.tiles = []


class TileRender(SpriteRender):
    tile: Tile
    box_collider: BoxCollider

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.tile = entity.get_component(Tile)
        self.box_collider = entity.get_component(BoxCollider)

    def render(self) -> None:
        super().render()

        w, h = self.size.t

        for x, y, rw, rh in self.box_collider.rects:
            rw *= w
            rh *= h
            x = w / 2 - rw / 2 + x * w
            y = h / 2 - rh / 2 - y * h

            draw_rect(self.rendered, self.tile.color.t, (x, y, rw, rh))
