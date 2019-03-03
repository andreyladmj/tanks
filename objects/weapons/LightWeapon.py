import random

import math
from time import time

from Global import get_main_layer
from objects.animations.StandartBulletFireAnimation import StandartBulletFireAnimation
from objects.bullets.StandartBullet import StandartBullet


class LightWeapon:
    standart_fire_offset_x = -20
    standart_fire_offset_y = 5
    standart_fire_animation_offset_x = -5
    standart_fire_animation_offset_y = 0

    tank = None

    def __init__(self, tank):
        self.tank = tank

    def getAngleDeflection(self):
        return random.randrange(-500, 500) / 100

    def firePosition(self):
        cos_x = math.cos(math.radians(self.tank.getGunRotation() - 180))
        sin_x = math.sin(math.radians(self.tank.getGunRotation()))
        x = self.tank.x + self.standart_fire_offset_x * sin_x + self.standart_fire_offset_y * cos_x
        y = self.tank.y - self.standart_fire_offset_x * cos_x + self.standart_fire_offset_y * sin_x
        return (x, y)

    def fireRotation(self):
        return self.tank.getGunRotation() - 90 + self.getAngleDeflection()

    def fireAnimationPosition(self):
        cos_x = math.cos(math.radians(self.tank.getGunRotation() - 180))
        sin_x = math.sin(math.radians(self.tank.getGunRotation()))
        x = self.tank.x + self.standart_fire_offset_x * sin_x + self.standart_fire_offset_y * cos_x
        y = self.tank.y - self.standart_fire_offset_x * cos_x + self.standart_fire_offset_y * sin_x
        anim_x = x + self.standart_fire_animation_offset_x * sin_x + self.standart_fire_animation_offset_y * cos_x
        anim_y = y - self.standart_fire_animation_offset_x * cos_x + self.standart_fire_animation_offset_y * sin_x
        return (anim_x, anim_y)

    # def fire(self, id=None, position=None, rotation=None, last_update_time=None):
    #     bullet = StandartBullet()
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
    #     animation = StandartBulletFireAnimation()
    #     animatiom_position = self.fireAnimationPosition()
    #     animation.appendAnimationToLayer(animatiom_position, self.tank.getGunRotation())

    def fire(self, bullet=None):
        position = self.firePosition()
        rotation = self.fireRotation()
        animatiom_position = self.fireAnimationPosition()
        animatiom_rotation = self.tank.getGunRotation()

        bullet = StandartBullet(position, rotation, fired_tank=self.tank)
        get_main_layer().dispatch_event('add_bullet', bullet)

        animation = StandartBulletFireAnimation(animatiom_position, animatiom_rotation)
        get_main_layer().dispatch_event('add_animation', animation)
    #
    #     bullet = BulletFactory.create(
    #         instance=StandartBullet,
    #         parent_id=self.gun.tank.id,
    #         position=position,
    #         rotation=rotation,
    #         last_update_time=time(),
    #         animation_instance=StandartBulletFireAnimation,
    #         animation_position=animatiom_position,
    #         animation_rotation=animatiom_rotation,
    #         add_moving_handler=True
    #     )
    #
    #     sendBulletToOtherPlayers(bullet)
