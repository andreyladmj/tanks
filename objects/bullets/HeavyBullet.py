from Global import get_main_layer
from objects.Bullet import Bullet
from objects.animations.ExplosionHeavyBulletAnimation import explosionHeavyBulletAnimation


class HeavyBullet(Bullet):
    type = 'HeavyBullet'
    spriteName = 'assets/bullets/bullet-origin.png'
    startPosition = (0, 0)

    scale = 1
    damage = 25
    damageRadius = 20
    velocity = (0, 0)
    fireLength = 800

    speed = 600

    def removeAnimation(self):
        Global.Layers.removeAnimation(self)

    def destroy(self, position=None):
        if not position: position = self.position

        animation = explosionHeavyBulletAnimation(self.position, self.rotation)
        get_main_layer().dispatch_event('add_animation', animation)

        super(HeavyBullet, self).destroy()
