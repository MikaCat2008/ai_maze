from utils import GameComponent

from .ui.button import MouseClick


class PlayButton(GameComponent):
    def __init__(self) -> None:
        super().__init__()

        self.handlers["click"] = self.on_click

    def on_click(self, event: MouseClick) -> None:
        scene_manager = self.entity.manager.scene.manager
        scene_manager.set_current("Game")
