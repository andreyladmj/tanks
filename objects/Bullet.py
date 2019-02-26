import math
import random
from time import time

from cocos import actions
from cocos import sprite
from cocos.actions import Action, MoveBy
import cocos.collision_model as cm


class Bullet(sprite.Sprite):
    # startPosition = (0, 0)
    # scale = 1
    # damage = 10
    # damageRadius = 20
    # velocity = (0, 0)
    # fireLength = 1000

    id = 0
    animation_position = (0, 0)
    animation_rotation = 0
    start_position = (0, 0)
    last_update_time = 0

    def __init__(self, spriteName, position=(0, 0), rotation=0):
        super(Bullet, self).__init__(spriteName)
        self.start_position = position
        self.last_update_time = time()
        self.rotation = rotation

        self.cshape = cm.AARectShape(
            self.position,
            self.width // 2,
            self.height // 2
        )

    def update(self):
        angle = self.rotation
        curr_x, curr_y = self.start_position
        time_delta = (time() - self.last_update_time)
        new_x = self.speed * time_delta * math.cos(math.radians(angle - 180)) + curr_x
        new_y = self.speed * time_delta * math.sin(math.radians(angle)) + curr_y
        self.position = (new_x, new_y)

    def exceededTheLengthLimit(self):
        if self.getLength(self.start_position, self.position) > self.fireLength:
            return True

        return False

    def getLength(self, point1, point2):
        deltax = math.pow(point1[0] - point2[0], 2)
        deltay = math.pow(point1[1] - point2[1], 2)
        return math.sqrt(deltax + deltay)

    def update_position(self, x, y):
        cos_x = math.cos(math.radians(self.rotation - 180))
        sin_x = math.sin(math.radians(self.rotation))

        x = x + self.bullets_fired_offset_x * sin_x + self.bullets_fired_offset_y * cos_x
        y = y - self.bullets_fired_offset_x * cos_x + self.bullets_fired_offset_y * sin_x
        self.position = (x, y)

        # self.startPosition = (x, y)
        # self.do(BulletMovingHandlers())

        # animation = pyglet.image.load_animation('sprites/weapons/Explosion2.gif')
        # anim = sprite.Sprite(animation)getExplosionAnimation
        # print(animation.get_duration())
        # anim.sprite_move_action = None
        # animation.(lambda x: Global.layers['game'])

        # animation.get_duration(lambda x: Global.layers['game'].remove(anim))

        # anim.position = (x, y)
        # Global.layers['game'].add(anim)

        anim_x = x + self.bullets_fired_animation_offset_x * sin_x + self.bullets_fired_animation_offset_y * cos_x
        anim_y = y - self.bullets_fired_animation_offset_x * cos_x + self.bullets_fired_animation_offset_y * sin_x

        # animation = self.getFireAnimation()
        # animq = self.getFireAnimationSprite(animation, anim_x, anim_y)
        # Global.layers['game'].add(anim)
        # t = Timer(animation.get_duration(), lambda: Global.layers['game'].remove(anim))
        # t.start()

        # montage Explosion2.gif -tile x1 -geometry +0+0 -alpha On -background "rgba(0,0,0,0.0)" -quality 100 test.png

        # animation = pyglet.image.load_animation('animation.gif')
        # frames = [frame.image for frame in animation.frames]

    def destroy(self, position=None):
        removeBullet(self)

    def getObjectFromSelf(self):
        return {
            'action': Global.NetworkActions.TANK_FIRE,
            NetworkDataCodes.LAST_UPDATE_TIME: str(self.last_update_time),
            NetworkDataCodes.BULLET_ID: self.id,
            NetworkDataCodes.TANK_ID: self.parent_id,
            NetworkDataCodes.POSITION: self.position,
            NetworkDataCodes.ROTATION: self.rotation,
            NetworkDataCodes.TYPE: self.type,
            NetworkDataCodes.ANIMATION_POSITION: self.animation_position,
            NetworkDataCodes.ANIMATION_ROTATION: self.animation_rotation,
        }


class removeAfterComplete(Action):
    def step(self, dt):
        super(removeAfterComplete, self).step(dt)


class SetBulletMovingHandlers(actions.Move):
    speed = 800

    def __init__(self):
        super(SetBulletMovingHandlers, self).__init__()
        self.r = random.randrange(-50, 50) / 10

    def step(self, dt):
        super(SetBulletMovingHandlers, self).step(dt)  # Run step function on the parent class.
        angle = self.target.rotation
        x = self.speed * math.cos(math.radians(angle - 180 + self.r))
        y = self.speed * math.sin(math.radians(angle + self.r))
        self.target.velocity = (x, y)
        x, y = self.target.position
        startX, startY = self.target.startPosition

        if self.getLength(x, y, startX, startY) > self.target.fireLength:
            self.target.explosion()

    def getLength(self, x1, y1, x2, y2):
        deltax = math.pow(x1 - x2, 2)
        deltay = math.pow(y1 - y2, 2)
        return math.sqrt(deltax + deltay)
