from sprite_obj import *
from random import randint, random, choice

class NPC(AnimatedSprite):
    def __init__(self, game, pos, path="resources/sprites/npc/soldier/0.png", scale=0.6, shift=0.38, anim_time=200):
        super().__init__(game, pos, path, scale, shift, anim_time)
        self.attack_images = self.get_images(self.path + "/attack")
        self.death_images = self.get_images(self.path + "/death")
        self.idle_images = self.get_images(self.path + "/idle")
        self.pain_images = self.get_images(self.path + "/pain")
        self.walk_images = self.get_images(self.path + "/walk")
        
        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.in_pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        self.check_anim_time()
        self.get_sprite()
        self.run_logic()

    def anim_pain(self):
        self.animate(self.pain_images)
        if self.anim_trigger:
            self.in_pain = False

    def check_hit_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.in_pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1: 
            self.alive = False
            self.game.sound.npc_death.play
            
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.obj_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)   

    def attack(self):
        if self.anim_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy and self.game.obj_renderer.blood_current_frames == 0:
                self.game.player.get_damage(self.damage)

    def anim_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_npc()
            if self.in_pain:
                self.anim_pain()
            elif self.ray_cast_player_npc():
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
        else:
            self.anim_death()
    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.pos == self.map_pos:
            return True
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        map_x, map_y = self.game.player.map_pos
        texture_hor, texture_vert = 1, 1

        ray_angle = self.theta
        cos_a = math.cos(ray_angle)
        sin_a = math.sin(ray_angle)

        y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - TINY_VALUE, -1)
        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx= delta_depth * cos_a 
        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth
        
        x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - TINY_VALUE, -1)
        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a 
        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        if depth_hor > depth_vert:
            depth, texture = depth_vert, texture_vert
            y_vert %= 1
            offset = y_vert if cos_a > 0 else (1 - y_vert)
        else:
            depth, texture = depth_hor, texture_hor
            x_hor %= 1
            offset = (1 - x_hor) if sin_a > 0 else x_hor
        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

class Soldier(NPC):
    def __init__(self, game, pos, path="resources/sprites/npc/soldier/0.png", scale=0.6, shift=0.38, anim_time=180):
        super().__init__(game, pos, path, scale, shift, anim_time)

class CacoDemon(NPC):
    def __init__(self, game, pos, path="resources/sprites/npc/caco_demon/0.png", scale=0.7, shift=0, anim_time=250):
        super().__init__(game, pos, path, scale, shift, anim_time)
        self.attack_dist = 1.0
        self.health = 150
        self.damage = 25
        self.speed = 0.05
        self.accuracy = 0.5

class CyberDemon(NPC):
    def __init__(self, game, pos, path="resources/sprites/npc/cyber_demon/0.png", scale=0.6, shift=0.38, anim_time=200):
        super().__init__(game, pos, path, scale, shift, anim_time)