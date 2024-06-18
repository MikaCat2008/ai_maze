from random import choice, shuffle
from typing import Optional
from utils import Vector2, Entity, Component

from components.builtin.tile_map import TileMap
from components.spawn_point import SpawnPoint
from components.finish_point import FinishPoint


class MazeHelper:
    @staticmethod
    def directions() -> list[tuple[int, int]]:
        return [ (1, 0), (0, 1), (-1, 0), (0, -1) ]

    @staticmethod
    def is_point_in_maze(maze: list[list[bool]], x: int, y: int) -> bool:
        return x >= 0 and y >= 0 and x < len(maze[0]) and y < len(maze)

    @classmethod
    def is_road(cls, maze: list[list[bool]], x: int, y: int) -> bool:
        return cls.is_point_in_maze(maze, x, y) and not maze[y][x]

    @classmethod
    def is_wall(cls, maze: list[list[bool]], x: int, y: int) -> bool:
        return cls.is_point_in_maze(maze, x, y) and maze[y][x]


class MazeGenerator(Component):
    maze: list[list[bool]]
    width: int
    height: int
    wall_size: int

    tile_map: TileMap

    def init(self, entity: Entity) -> None:
        super().init(entity)

        self.maze = None        
        self.width = 15
        self.height = 15
        self.wall_size = 48

        self.tile_map = entity.manager.get_entity_by_tag("TileMap").get_component(TileMap)

        self.generate()

    def generate(self) -> None:
        self.tile_map.clear()

        self.generate_maze()
        self.normalize_maze()
        self.create_walls()
        self.create_spawn_point()
        self.create_finish_point()

    def generate_maze(self) -> None:
        self.maze = [[1] * (self.width - 2) for _ in range(self.height - 2)]

        need_connect_points = set()
        need_connect_points.add((0, 0))

        while need_connect_points:
            x, y = point = choice(tuple(need_connect_points))
                    
            need_connect_points.remove(point)

            self.maze[y][x] = False

            self.connect(x, y)
            self.add_visible_points(need_connect_points, x, y)

    def connect(self, x: int, y: int) -> None:
        directions = MazeHelper.directions()
        
        shuffle(directions)

        for dx, dy in directions:
            nx = x + dx * 2
            ny = y + dy * 2

            if MazeHelper.is_road(self.maze, nx, ny):
                self.maze[y + dy][x + dx] = False

                return

    def add_visible_points(
        self, points: set[tuple[int, int]], x: int, y: int
    ) -> None:
        for ox, oy in MazeHelper.directions():
            dx, dy = x + ox * 2, y + oy * 2
            
            if MazeHelper.is_wall(self.maze, dx, dy):
                points.add((dx, dy))

    def normalize_maze(self) -> None:
        maze = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                if x == self.width - 1:
                    if self.width % 2:
                        maze[y][x] = 1
                elif y == self.height - 1:
                    if self.height % 2:
                        maze[y][x] = 1
                elif x == 0 or y == 0:
                    maze[y][x] = 1
                else:
                    maze[y][x] = self.maze[y - 1][x - 1]

        self.maze = maze

    def get_by_xy(self, x: int, y: int) -> bool:
        if MazeHelper.is_point_in_maze(self.maze, x, y):
            return self.maze[y][x]

        return False   

    def neighbours(self, x: int, y: int) -> tuple[bool, bool, bool, bool]:        
        return ( 
            self.get_by_xy(x, y + 1), 
            self.get_by_xy(x - 1, y), 
            self.get_by_xy(x, y - 1), 
            self.get_by_xy(x + 1, y) 
        )

    def create_walls(self) -> None:
        for y, row in enumerate(self.maze):
            for x, wall in enumerate(row):
                if not wall:
                    continue

                self.create_wall(x, y)

    def create_wall(self, x: int, y: int) -> None:
        top, left, down, right = self.neighbours(x, y)

        wall_type = top + down * 2 + left * 4 + right * 8

        self.tile_map.add_tile(
            Vector2(x, y), f"Wall-{wall_type}"
        )

    def create_spawn_point(self) -> None:
        x, y = 1, 1 + (not self.height % 2)

        self.tile_map.add_tile(
            Vector2(x, y), "SpawnPoint", SpawnPoint
        )

    def create_finish_point(self) -> None:
        x, y = self.width - 2 - (not self.width % 2), self.height - 2

        self.tile_map.add_tile(
            Vector2(x, y), "FinishPoint", FinishPoint
        )
