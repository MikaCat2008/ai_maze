from typing import cast
import pygame as pg
from pygame.time import Clock
from pygame.event import get as get_events
from pygame.display import flip as flip_screen, set_mode, set_caption
from utils import SceneManager

pg.font.init()

from scenes.menu_scene import menu_scene_setup
from scenes.game_scene import game_scene_setup

clock = Clock()
screen = set_mode((744, 744))
scene_manager = SceneManager()

menu_scene = menu_scene_setup(screen, scene_manager)
game_scene = game_scene_setup(screen, scene_manager)

scene_manager.set_current(menu_scene)

while True:
    scene = scene_manager.current
    camera = scene.entity_manager.get_entity_by_tag("Camera").get_component("Camera")
    screen.fill(camera.background.t)

    for event in get_events():
        if event.type in (pg.MOUSEMOTION, pg.MOUSEBUTTONUP, pg.MOUSEBUTTONDOWN):
            event.pos = camera.normalize(event.pos)

        scene.entity_manager.notify(event)
        
        if event.type == pg.QUIT:
            exit()

    scene.entity_manager.update(clock.get_time() / 1000)

    flip_screen()

    clock.tick(120)
    set_caption(f"{clock.get_fps():.1f} fps")
