import pygame as pg
from settings import *

class ObjRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_texture = self.get_texture("resources/textures/sky.png", (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture("resources/textures/blood_screen.png", RES)
        self.blood_max_frames = 10
        self.blood_current_frames = 0
        self.player_in_pain = False
        self.digit_size = 90
        self.digit_images = [self.get_texture(f"resources/textures/digits/{i}.png", [self.digit_size] * 2)for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture("resources/textures/game_over.png", RES)
        self.win_image = self.get_texture("resources/textures/win.png", RES)

    def draw(self):
        self.draw_background()
        self.render_game_objs()
        self.player_damage()
        self.draw_player_health()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits["10"], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        if self.player_in_pain:
            self.blood_current_frames += 1
            self.screen.blit(self.blood_screen, (0, 0))
            self.blood_screen.set_alpha(int((self.blood_max_frames - self.blood_current_frames) / self.blood_max_frames * 255))
            if self.blood_current_frames >= self.blood_max_frames:
                self.blood_screen.set_alpha(255)
                self.player_in_pain = False
                self.blood_current_frames = 0

    def draw_background(self):
        pg.draw.rect(self.screen, FLOOR_COL, (0, 0, WIDTH, HEIGHT))
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_texture, (-self.sky_offset, 0))
        self.screen.blit(self.sky_texture, (-self.sky_offset + WIDTH, 0))
        
    def render_game_objs(self):
        list_objs = sorted(self.game.raycasting.objs_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objs:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture("resources/textures/1.png"), 
            2: self.get_texture("resources/textures/2.png"), 
            3: self.get_texture("resources/textures/3.png"), 
            4: self.get_texture("resources/textures/4.png"), 
            5: self.get_texture("resources/textures/5.png"), 
        }