import pyglet

from Global import get_main_layer
from objects.Bullet import Bullet
from objects.animations.ExplosionStandartBulletAnimation import explosionStandartBulletAnimation


class StandartBullet(Bullet):
    type = 'StandartBullet'
    spriteName = 'assets/bullets/bullet.png'
    startPosition = (0, 0)

    scale = 0.8
    damage = 3
    damageRadius = 5
    velocity = (0, 0)
    fireLength = 1000

    speed = 400

    def removeAnimation(self):
        Global.Layers.removeAnimation(self)
        # if self in Global.layers['bullets']: Global.layers['bullets'].remove(self)
        # if self in Global.objects['bullets']: Global.objects['bullets'].remove(self)

    def destroy(self, position=None):
        if not position: position = self.position

        animation = explosionStandartBulletAnimation(self.position, self.rotation)
        get_main_layer().dispatch_event('add_animation', animation)

        super(StandartBullet, self).destroy()
