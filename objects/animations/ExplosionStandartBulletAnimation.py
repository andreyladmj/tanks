from threading import Timer

from cocos import sprite
from pyglet.image import load_animation

from objects.animations.AnimationTypes import OnceAnimation


class explosionStandartBulletAnimation(sprite.Sprite):
    src = 'assets/weapons/bullet-explode.gif'

    def __init__(self, position=(0, 0), rotation=0):
        self.animation = load_animation(self.src)
        self.animation.frames[-1].duration = None  # stop loop

        super(explosionStandartBulletAnimation, self).__init__(self.animation)

        # self.anim = sprite.Sprite(self.animation)
        self.anim = OnceAnimation(self.animation)
        self.anim.image_anchor = (self.animation.get_max_width() / 2, self.animation.get_max_height() / 4)
        self.anim.scale = 0.2
        self.anim.position = position

    def getAnimation(self):
        return self.animation

    def getSprite(self):
        return self.anim

    def appendAnimationToLayer(self, position):
        self.anim.position = position

        addanimationToGame(self.anim)
        # Global.Layers.addAnimation(self.anim)
        # t = Timer(self.animation.get_duration(), lambda: Global.Layers.removeAnimation(self.anim))
        # t.start()
