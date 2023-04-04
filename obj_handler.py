from sprite_obj import *
from npc import *

class ObjHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.static_sprite_path = "resources/sprites/static_sprites/"
        self.anim_sprite_path = "resources/sprites/animated_sprites/"
        add_sprite = self.add_sprite
        add_ncp = self.add_npc

        self.npc_positions = {}

        add_sprite(AnimatedSprite(game, pos=(11.5, 3.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 5.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(14.5, 7.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(12.5, 7.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(9.5, 7.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(14.5, 12.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(9.5, 20.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(10.5, 20.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(3.5, 14.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(3.5, 18.5), path=self.anim_sprite_path + 'red_light/0.png'))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

        add_ncp(Soldier(game, pos=(10.5, 4.5)))
        add_ncp(CacoDemon(game, pos=(10.5, 5.5)))
        add_ncp(CyberDemon(game, pos=(10.5, 6.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)