import pyglet
from cocos import sprite

# anim = None
# animation = None
#
# def init_animation():
#     global animation, anim
#     explosion = pyglet.image.load('assets/weapons/fire-small-gun.png')
#     explosion_seq = pyglet.image.ImageGrid(explosion, 1, 3)
#     explosion_tex_seq = pyglet.image.TextureGrid(explosion_seq)
#     animation = pyglet.image.Animation.from_image_sequence(explosion_tex_seq, .02, loop=False)
#     anim = sprite.Sprite(animation)
#     anim.scale = 0.2
from objects.animations.AnimationTypes import OnceAnimation


class StandartBulletFireAnimation:

    def __init__(self, position=(0, 0), rotation=0):
        explosion = pyglet.image.load('assets/weapons/fire-small-gun.png')
        explosion_seq = pyglet.image.ImageGrid(explosion, 1, 3)
        explosion_tex_seq = pyglet.image.TextureGrid(explosion_seq)
        self.animation = pyglet.image.Animation.from_image_sequence(explosion_tex_seq, .02, loop=False)
        # self.anim = sprite.Sprite(self.animation)
        self.anim = OnceAnimation(self.animation)
        self.anim.scale = 0.2
        self.anim.position = position
        self.anim.rotation = rotation - 180

    def getAnimation(self):
        return self.animation

    def getSprite(self):
        return self.anim

    def appendAnimationToLayer(self, position, rotation):
        anim = self.getSprite(position, rotation)
        duration = self.animation.get_duration()

        addanimationToGame(anim)
