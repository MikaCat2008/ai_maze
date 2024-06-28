from utils import load_image, Prefab, Vector2, Component
from components.builtin.transition import Transition
from components.builtin.box_collider import BoxCollider
from components.builtin.sprite_render import SpriteRender
from components.movement import Movement

sprite = load_image("client/resources/player.png", (60, 66))


class MainPlayer(Prefab):
    def init(self, pos: Vector2) -> tuple[list[Component], str]:
        return (
            [
                Movement(),
                Transition(pos),
                BoxCollider([
                    [0, 0, 0.5, 0.55]
                ]),
                SpriteRender(sprite=sprite)
            ],
            "MainPlayer"
        )
