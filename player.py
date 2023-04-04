from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recover_delay = 700
        self.time_prev = pg.time.get_ticks()

    def recover_health(self):
        if self.check_health_recover_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recover_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recover_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health <= 0:
            self.game.obj_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def check_win(self):
        all_dead = True
        for npc in self.game.obj_handler.npc_list:
            if npc.alive:
                all_dead = False
                break
        if all_dead:
            self.game.obj_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        self.health -= damage
        self.game.obj_renderer.player_in_pain = True
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.shot = True
                self.game.weapon.reloading = True
                self.game.sound.shotgun.play()
        
    def movement(self):
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        dx, dy = 0, 0

        speed = PLAYER_SPEED * self.game.delta_time
        speed_cos = speed * cos_a
        speed_sin = speed * sin_a

        keys = pg.key.get_pressed()
        if keys[FORWARD]:
            dx += speed_cos
            dy += speed_sin
        if keys[BACK]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[LEFT]:
            dx += speed_sin
            dy -= speed_cos
        if keys[RIGHT]:
            dx -= speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)
        self.angle %= math.tau

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        pg.mouse.set_pos(mx, HALF_HEIGHT)
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENS * self.game.delta_time

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()
        self.check_win()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)