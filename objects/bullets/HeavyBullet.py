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

    def __init__(self, position=(0, 0), rotation=0):
        super(HeavyBullet, self).__init__(self.spriteName, position, rotation)

    def removeAnimation(self):
        Global.Layers.removeAnimation(self)

    def destroy(self, position=None):
        if not position: position = self.position

        animation = explosionHeavyBulletAnimation()
        animation.appendAnimationToLayer(position, self.rotation)

        super(HeavyBullet, self).destroy()
