from utils import Vector2, GameObject, GameComponent

from .builtin.input import Input


class Movement(GameComponent):
    speed: int
    input: Input
    
    def init(self, game_object: GameObject) -> None:
        super().init(game_object)

        self.speed = 200
        self.input = game_object.manager.get_entity_by_tag("Input").get_component(Input)

    def update(self, delta: float) -> None:
        move = Vector2()
        speed = self.speed * delta

        if self.input.pressed.up:
            move.y += speed
        if self.input.pressed.down:
            move.y -= speed
        if self.input.pressed.left:
            move.x -= speed
        if self.input.pressed.right:
            move.x += speed

        if move.x or move.y:
            self.box_collider.update_collision(move)
