import pyglet

from objects.Bullet import Bullet
from objects.animations.ExplosionStandartBulletAnimation import explosionStandartBulletAnimation
from objects.animations.ExplosionStandartBulletAnimation2 import explosionStandartBulletAnimation2
from objects.animations.StandartBulletFireAnimation import StandartBulletFireAnimation


class LightBullet(Bullet):
    type = 'LightBullet'
    spriteName = 'assets/bullets/bullet.png'
    startPosition = (0, 0)

    scale = 0.4
    damage = 1
    damageRadius = 5
    velocity = (0, 0)
    fireLength = 600

    speed = 800

    def __init__(self):
        super(LightBullet, self).__init__(self.spriteName)

    def removeAnimation(self):
        Global.Layers.removeAnimation(self)
        # if self in Global.layers['bullets']: Global.layers['bullets'].remove(self)
        # if self in Global.objects['bullets']: Global.objects['bullets'].remove(self)

    def destroy(self, position=None):
        if not position: position = self.position

        animation = explosionStandartBulletAnimation()
        animation.appendAnimationToLayer(position)

        super(LightBullet, self).destroy()
