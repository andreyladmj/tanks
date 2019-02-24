from threading import Timer

import pyglet
from cocos import sprite

from components import Global


class explosionStandartBulletAnimation2:

    def __init__(self):
        explosion = pyglet.image.load('assets/weapons/standart-bullet-explode.png')
        explosion_seq = pyglet.image.ImageGrid(explosion, 1, 12)
        explosion_tex_seq = pyglet.image.TextureGrid(explosion_seq)
        self.animation = pyglet.image.Animation.from_image_sequence(explosion_tex_seq, .05, loop=False)

        self.anim = sprite.Sprite(self.animation)
        self.anim.image_anchor = (self.animation.get_max_width() / 2, self.animation.get_max_height() / 4)
        self.anim.scale = 0.2

    def getAnimation(self):
        return self.animation

    def getSprite(self, position, rotation):
        self.anim.position = position
        self.anim.rotation = rotation - 90
        return self.anim

    def appendAnimationToLayer(self, position, rotation):
        anim = self.getSprite(position, rotation)
        Global.Layers.addAnimation(anim)
        t = Timer(self.animation.get_duration(), lambda: Global.Layers.removeAnimation(anim))
        t.start()
