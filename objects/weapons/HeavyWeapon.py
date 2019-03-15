import random

import math
from time import time

from Global import MainLayer, get_main_layer
from objects.animations.HeavyBulletFireAnimation import HeavyBulletFireAnimation
from objects.bullets.HeavyBullet import HeavyBullet


class HeavyWeapon:
    heavy_fire_offset_x = -20
    heavy_fire_offset_y = 0
    heavy_fire_animation_offset_x = -35
    heavy_fire_animation_offset_y = 0

    tank = None

    def __init__(self, tank):
        self.tank = tank

    def getAngleDeflection(self):
        return 0
        return random.randrange(-200, 200) / 100

    def firePosition(self):
        cos_x = math.cos(math.radians(self.tank.getGunRotation() - 180))
        sin_x = math.sin(math.radians(self.tank.getGunRotation()))
        x = self.tank.x + self.heavy_fire_offset_x * sin_x + self.heavy_fire_offset_y * cos_x
        y = self.tank.y - self.heavy_fire_offset_x * cos_x + self.heavy_fire_offset_y * sin_x
        return (x, y)

    def fireRotation(self):
        return self.tank.getGunRotation() - 90 + self.getAngleDeflection()

    def fireAnimationPosition(self):
        cos_x = math.cos(math.radians(self.tank.getGunRotation() - 180))
        sin_x = math.sin(math.radians(self.tank.getGunRotation()))
        x = self.tank.x + self.heavy_fire_offset_x * sin_x + self.heavy_fire_offset_y * cos_x
        y = self.tank.y - self.heavy_fire_offset_x * cos_x + self.heavy_fire_offset_y * sin_x
        anim_x = x + self.heavy_fire_animation_offset_x * sin_x + self.heavy_fire_animation_offset_y * cos_x
        anim_y = y - self.heavy_fire_animation_offset_x * cos_x + self.heavy_fire_animation_offset_y * sin_x
        return (anim_x, anim_y)

    # def fire(self, id=None, position=None, rotation=None, last_update_time=None):
    #     bullet = HeavyBullet()
    #
    #     if not position: position = self.firePosition()
    #     if not rotation: rotation = self.fireRotation()
    #     if not last_update_time: last_update_time = time()
    #
    #     bullet.id = id
    #     bullet.parent_id = self.tank.tank.id
    #     bullet.position = position
    #     bullet.start_position = position
    #     bullet.rotation = rotation
    #     bullet.last_update_time = last_update_time
    #
    #     addBulletToGame(bullet)
    #     bullet.do(BulletMovingHandlers())
    #
    #     animation = HeavyBulletFireAnimation()
    #     animatiom_position = self.fireAnimationPosition()
    #     animation.appendAnimationToLayer(animatiom_position, self.tank.rotation)

    def fire(self, bullet=None):
        position = self.firePosition()
        rotation = self.fireRotation()
        animatiom_position = self.fireAnimationPosition()
        animatiom_rotation = self.tank.getGunRotation()

        bullet = HeavyBullet(position, rotation, fired_tank=self.tank)
        get_main_layer().dispatch_event('add_bullet', bullet)

        animation = HeavyBulletFireAnimation(animatiom_position, animatiom_rotation)
        get_main_layer().dispatch_event('add_animation', animation)

        # bullet = BulletFactory.create(
        #     instance=HeavyBullet,
        #     parent_id = self.gun.tank.id,
        #     position=position,
        #     rotation=rotation,
        #     last_update_time=time(),
        #     animation_instance=HeavyBulletFireAnimation,
        #     animation_position=animatiom_position,
        #     animation_rotation=animatiom_rotation,
        #     add_moving_handler=True
        # )
        #
        # sendBulletToOtherPlayers(bullet)
