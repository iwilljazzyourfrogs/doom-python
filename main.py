import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
import pygame as pg

from settings import *
from map import *
from player import *
from raycasting import *
from obj_renderer import *
from sprite_obj import *
from obj_handler import *
from weapon import *
from sound import *
from pathfinding import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES, pg.SCALED, vsync=1)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.obj_renderer = ObjRenderer(self)
        self.raycasting = Raycasting(self)
        self.obj_handler = ObjHandler(self)
        self.weapon = RangedWeapon(self)
        self.sound = Sound(self)
        self.pathfinding = Pathfinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.obj_handler.update()
        self.weapon.update()
        self.delta_time =  self.clock.tick(FPS)
        pg.display.set_caption(f"{self.clock.get_fps():.1f}")

    def draw(self):
        self.obj_renderer.draw()
        self.weapon.draw()
        pg.display.update()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit() 
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()