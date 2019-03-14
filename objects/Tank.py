import cocos.collision_model as cm
from cocos import sprite
from threading import Timer

from Global import get_main_layer
from helper.DamageHelper import DamageHelper
from objects.HealthSprite import HealthSprite
from objects.animations.ExplosionTankAnimation import ExplosionTankAnimation
from objects.weapons.HeavyWeapon import HeavyWeapon
from objects.weapons.LightWeapon import LightWeapon


class Tank(sprite.Sprite):
    Gun = None
    gun_rotation = 0
    id = 0
    type = 1

    speed = 30
    health = 100

    old_position = (0, 0)
    velocity = (0, 0)

    maxBulletsHolder = 10
    bulletsHolder = 10
    timeForBulletsHolderReload = 3

    healthHelper = None

    spriteName = 'assets/tank/parts/E-100_1.png'
    spriteGunName = 'assets/tank/parts/E-100_2.png'
    spriteHealthName = 'assets/50x5.png'

    canHeavyFire = True
    canFire = True
    bulletFreezTime = 0.3
    heavyBulletFreezTime = 2

    bot = False
    clan = 0
    rotation_speed = 1
    gun_rotation_speed = 1
    speed_acceleration = 1.2
    max_speed = 35

    def __init__(self, x=0, y=0, rotation=0):
        self.GunSprite = sprite.Sprite(self.spriteGunName)
        self.GunSprite.image_anchor = (self.GunSprite.image.width / 2, self.GunSprite.image.height / 2 + 20)

        self.healthSprite = sprite.Sprite(self.spriteHealthName)
        super().__init__(self.spriteName)

        self.scale = self.GunSprite.scale = 0.5
        self.rotation = self.GunSprite.rotation = rotation
        self.healthHelper = HealthSprite()
        self.updateHealthPosition()

        self.position = (x, y)
        self._update_position()

        self.weapon1 = HeavyWeapon(self)
        self.weapon2 = LightWeapon(self)

        self.reward = 0

        self.cshape = cm.AARectShape(
            self.position,
            self.width // 2,
            self.height // 2
        )

    def _update_position(self):
        super(Tank, self)._update_position()
        self.GunSprite.position = self.position
        self.GunSprite.rotation = self.rotation + self.gun_rotation

        x, y = self.position
        self.healthSprite.position = (x - 5, y + 40)
        # self.updateHealthPosition()

        # self.rotation = 180
        # self.Gun.position = self.position
        # self.Gun.rotation = self.rotation + self.Gun.gun_rotation

    # def update(self, data):
    #     self.position = data.get(NetworkDataCodes.POSITION)
    #     self.gun_rotation = data.get(NetworkDataCodes.GUN_ROTATION)
    #     self.rotation = data.get(NetworkDataCodes.ROTATION)

    def updateHealthPosition(self):
        if self.healthHelper: self.healthHelper.updateHealthPosition(self.position)

    def setHealth(self, health):
        # self.healthHelper.setHealth(health)
        percent = max(health, 0) / 100.
        self.healthSprite.scale_x = percent

    def heavy_fire(self, bullet=None):
        self.weapon1.fire()

        # self.Gun.fireFirstWeapon(bullet)

    def fire(self, bullet=None):
        self.weapon2.fire()
        # self.Gun.fireSecondWeapon(bullet)

    def fireFirstWeapon(self, bullet=None):
        if self.canHeavyFire:
            self.weapon1.fire(bullet)
            self.canHeavyFire = False
            Timer(self.heavyBulletFreezTime, self.acceptHeabyFire).start()

    def fireSecondWeapon(self, bullet=None):
        if self.canFire:
            self.weapon2.fire(bullet)
            self.canFire = False
            Timer(self.bulletFreezTime, self.acceptFire).start()

    def acceptHeabyFire(self):
        self.canHeavyFire = True

    def acceptFire(self):
        self.canFire = True

    def destroy(self):
        animation = ExplosionTankAnimation()
        animation.appendAnimationToLayer(self.position)

        Global.EventDispatcher.dispatch_event('tank_destroy', self)
        Global.removeTankFromGame(self)

    def damage(self, bullet):
        dx = (self.width + self.height) * self.scale / 2
        dmg = DamageHelper.get_damage(self.position, bullet, dx)

        self.health -= dmg
        x, y = self.position
        get_main_layer().add_damage_label(dmg, (x, y + 20))
        self.setHealth(self.health)

        # Global.damageSomeTank(id=self.id, dmg=dmg, health=self.health)
        #
        # Global.Queue.append({
        #     "action": NetworkActions.DAMAGE,
        #     NetworkDataCodes.TYPE: NetworkDataCodes.TANK,
        #     NetworkDataCodes.TANK_ID: self.id,
        #     NetworkDataCodes.HEALTH: self.health,
        #     NetworkDataCodes.DAMAGE: dmg
        # })
        return dmg

    def get_reward(self):
        reward = self.reward
        self.reward = 0
        return reward

    def set_reward(self, reward):
        self.reward = max(self.reward, reward)

    def getGunRotation(self):
        return self.gun_rotation + self.rotation

    def getObjectFromSelf(self):
        x, y = self.position
        r = self.rotation
        gr = self.gun_rotation

        return {
            'action': NetworkCodes.NetworkActions.UPDATE,
            NetworkCodes.NetworkDataCodes.TANK_ID: self.id,
            NetworkCodes.NetworkDataCodes.POSITION: (int(x), int(y)),
            NetworkCodes.NetworkDataCodes.ROTATION: int(r),
            NetworkCodes.NetworkDataCodes.GUN_ROTATION: int(gr),
            NetworkCodes.NetworkDataCodes.CLAN: self.clan,
            NetworkCodes.NetworkDataCodes.HEALTH: self.health,
            NetworkCodes.NetworkDataCodes.TYPE: self.type,
        }
