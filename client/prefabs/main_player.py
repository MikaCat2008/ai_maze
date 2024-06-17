from pygame.rect import Rect
from utils import Prefab, Vector2, Vector4, Component
from components.builtin.transition import Transition
from components.builtin.box_collider import BoxCollider
from components.builtin.sprite_render import SpriteRender
from components.movement import Movement


class MainPlayer(Prefab):
    movement: Movement
    transition: Transition
    box_collider: BoxCollider
    sprite_render: SpriteRender

    def init(self, pos: Vector2) -> tuple[list[Component], str]:
        return (
            [
                Movement(),
                Transition(pos),
                BoxCollider([
                    Rect(0, 0, 1, 1)
                ]),
                SpriteRender(Vector2(20, 20), Vector4(255, 0, 0))
            ],
            "MainPlayer"
        )
