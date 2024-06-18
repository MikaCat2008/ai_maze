from pygame.surface import Surface
from utils import load_json, Scene, Vector2, Vector3, Vector4, SceneManager

from components.builtin.input import Input
from components.builtin.camera import Camera
from components.builtin.tile_map import TileMap, TileType
from components.builtin.transition import Transition
from components.maze_generator import MazeGenerator
# from components.camera_movement import CameraMovement

walls = {
    f"Wall-{i}": TileType(
        tag="Wall",
        rects=[ list(map(eval, rect)) for rect in rects ],
        collision=True
    ) for i, rects in load_json("client/resources/walls.json").items()
}


def game_scene_setup(screen: Surface, manager: SceneManager) -> Scene:
    return manager.create([
        ( 
            [
                Input()
            ], 
            "Input"
        ),
        (
            [
                Camera(screen, Vector3(255, 255, 255)),
                Transition(Vector2(336, 336))
            ],
            "Camera"
        ),
        # ( 
        #     [ 
        #         Multiplayer(username, password) 
        #     ], "Multiplayer"
        # ),
        (
            [
                TileMap(48, {
                    "SpawnPoint": TileType(
                        size=80,
                        color=Vector4(0, 255, 0, 100)
                    ),
                    "FinishPoint": TileType(
                        size=80,
                        color=Vector4(255, 0, 0, 100)
                    ),
                    **walls
                }),
                Transition(Vector2(0, 0))
            ],
            "TileMap"
        ),
        ( 
            [
                MazeGenerator()
            ], 
            "MazeGenerator" 
        ),
        # ( 
        #     [ 
        #         CameraMovement() 
        #     ], 
        #     "CameraMovement" 
        # ),
    ], "Game")
