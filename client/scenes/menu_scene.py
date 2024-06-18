from pygame.surface import Surface
from utils import Scene, Vector2, Vector3, SceneManager

from components.ui.button import Button, ButtonRender
from components.builtin.camera import Camera
from components.builtin.transition import Transition
from components.builtin.box_collider import BoxCollider
from components.play_button import PlayButton


def menu_scene_setup(screen: Surface, manager: SceneManager) -> Scene:
    return manager.create([
        (
            [
                Camera(screen, Vector3(80, 81, 133)),
                Transition(Vector2(0, 0))
            ],
            "Camera" 
        ),
        (
            [
                Button("Play"),
                PlayButton(),
                Transition(Vector2()),
                BoxCollider([ [0, 0, 1, 1] ]),
                ButtonRender(Vector2(150, 50))
            ],
            None
        )
    ], "Menu")
