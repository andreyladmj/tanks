from itertools import chain
from random import randint
from threading import Timer
from time import time

import cocos
import pyglet
from cocos.actions import MoveBy, FadeOut
from cocos.batch import BatchNode
from pyglet.window import key
import cocos.collision_model as cm

from Global import CurrentKeyboard, CollisionManager
from handlers.BotTankMovingHandlers import BotTankMovingHandlers
from handlers.BulletMovingHandlers import BulletMovingHandlers
from handlers.UserTankMovingHandlers import UserTankMovingHandlers
# from helper.CalcCoreHelper import CalcCoreHelper
from layers.TankNodeLayer import TankNodeLayer, ObjectsNodeLayer
from objects.Explosion import Explosion
from objects.Tank import Tank
import numpy as np


class MainSceneLayer(cocos.layer.ScrollableLayer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self):
        super(MainSceneLayer, self).__init__()
        self.schedule(self.update)
        self.backgroundLayer = ObjectsNodeLayer()
        self.tanksLayer = TankNodeLayer()
        self.objectsLayer = ObjectsNodeLayer()
        self.bulletsLayer = ObjectsNodeLayer()
        self.additionalLayer = ObjectsNodeLayer()
        self.globalPanel = cocos.layer.Layer()
        self.add(self.backgroundLayer, z=1)
        self.add(self.objectsLayer, z=2)
        self.add(self.tanksLayer, z=3)
        self.add(self.bulletsLayer, z=4)
        self.add(self.additionalLayer, z=5)
        self.add(self.globalPanel, z=5)

        back = cocos.sprite.Sprite('assets/background.png')
        back.image_anchor = (0,0)
        back.position = (0,0)
        self.backgroundLayer.add(back)
        # self.calc_core = CalcCoreHelper(self.tanksLayer, self.objectsLayer, self.bulletsLayer)

    s = 0
    def update(self, dt):
        self.checkCollisions()
        self.removeLabelsWithDamage()

        # print(dt)

        # self.s += dt
        # print('dt', dt, 'self.s', self.s)

        # if self.s > 4:
        #     self.calc_core.update_plt()
        #     self.s = 0
        # if Global.IsGeneralServer:
        #     Game.checkCollisions()
        #
        #     if Global.connections_listener: Global.connections_listener.Pump()
        #     self.playAnimationsQueue()
        #     self.callPeriodicalEvent(dt)
        # else:
        #     PodSixNet.Connection.connection.Pump()
        #     Global.TankNetworkListenerConnection.Pump()
        #     self.sendDataToServer()
        #
        #
        # self.removeLabelsWithDamage()
        # self.printDebugInfo()

    # def click(self, clicks):
    #     self.dispatch_event('on_clicked', clicks)

    def tank_destroy(self, tank):
        self.tanksLayer.remove(tank)
        self.additionalLayer.remove(tank.GunSprite)
        self.additionalLayer.remove(tank.healthSprite)
        CollisionManager.remove_tricky(tank)

        self.add_random_bot()
        # if hasattr(tank, 'moving_handler'):
        #     tank.moving_handler.finish()

    def add_tank(self, tank, player=False):
        self.tanksLayer.add(tank)
        self.additionalLayer.add(tank.GunSprite)
        self.additionalLayer.add(tank.healthSprite)
        CollisionManager.add(tank)

        if player:
            tank.do(UserTankMovingHandlers())

        if not player:
            moving_handler = BotTankMovingHandlers()
            tank.moving_handler = moving_handler
            tank.do(moving_handler)

    def add_bullet(self, bullet):
        self.bulletsLayer.add_object(bullet)
        CollisionManager.add(bullet)
        bullet.do(BulletMovingHandlers())

    def add_animation(self, animation, duration=0):
        try:
            self.additionalLayer.add(animation.getSprite(), z=5)
        except:
            pass
        # if duration:
        #     t = Timer(duration, lambda: self.additionalLayer.remove(animation.getSprite()))
        #     t.start()

    def remove_animation(self, animation):
        try:
            self.additionalLayer.remove(animation)
        except:
            pass

    def checkCollisions(self):
        for bullet in self.bulletsLayer.get_children():
            bullet.cshape = cm.AARectShape(bullet.position, 2, 2)
            collisions = CollisionManager.objs_colliding(bullet)
            shouldExplose = False

            if collisions:
                for item in self.tanksLayer.get_children():
                    if item in collisions and item != bullet.fired_tank:
                        shouldExplose = True
                        break

                if not shouldExplose:
                    for item in self.objectsLayer.get_children():
                        if item in collisions:
                            shouldExplose = True
                            break

            if bullet.exceededTheLengthLimit() or shouldExplose:
                explosion = Explosion(bullet)
                explosion.checkDamageCollisions()
                bullet.destroy()

    def get_observation(self, tank):
        obs = []

        tanks_list = self.tanksLayer.get_children()
        current_index = tanks_list.index(tank)

        # first tank it is the current tank
        tanks = self.get_K_means_tanks(current_index)
        # should be 9 features
        current_rotation = tank.getGunRotation()
        obs.append(current_rotation)

        for item in tanks:
            # tank_info = [item.position[0], item.position[1]]
            obs.append(item.position[0])
            obs.append(item.position[1])

        return obs

    def get_K_means_tanks(self, current_index, K=3):
        tanks_list = self.tanksLayer.get_children()
        tanks = np.array(list(map(lambda obj: obj.position, tanks_list)))
        dist_sq = np.sum((tanks[:, np.newaxis] - tanks[np.newaxis, :]) ** 2, axis=-1)
        nearest_sorted = np.argsort(dist_sq, axis=1)[:, :K+1]
        nearest_indexes = nearest_sorted[nearest_sorted[:, 0] == current_index][0]
        return [tanks_list[i] for i in nearest_indexes]

    def on_clicked(self, clicks):
        print('on_clicked', clicks)

    def sendDataToServer(self):
        player = getGamePlayer()

        if player:
            Global.TankNetworkListenerConnection.Send({
                'action': NetworkActions.TANK_MOVE,
                NetworkDataCodes.POSITION: player.position,
                NetworkDataCodes.GUN_ROTATION: player.gun_rotation,
                NetworkDataCodes.ROTATION: player.rotation,
                NetworkDataCodes.TANK_ID: player.id
            })

    def resize(self, width, height):
        self.viewPoint = (width // 2, height // 2)
        self.currentWidth = width
        self.currentHeight = height

    def buttonsHandler(self, dt):
        x_direction = CurrentKeyboard[key.NUM_4] - CurrentKeyboard[key.NUM_6]
        y_direction = CurrentKeyboard[key.NUM_5] - CurrentKeyboard[key.NUM_8]
        x, y = self.position

        if x_direction:
            x += x_direction * 20

        if y_direction:
            y += y_direction * 20

        if CurrentKeyboard[key.NUM_0]:
            x = y = 0

        if x_direction or y_direction:
            self.set_view(0, 0, self.currentWidth, self.currentHeight, x, y)

        # if self.help:
        #     type = self.selectTank()
        #     if type: self.connectToServer(type)

        # self.changleStatsPosition(-x, -y, self.currentWidth, self.currentHeight)

    def connectToServer(self, type):
        self.remove(self.help)
        self.help = None
        Global.TankNetworkListenerConnection = NetworkListener('localhost', 1332, type)
        self.TankNetworkListenerConnection = Global.TankNetworkListenerConnection

    def changleStatsPosition(self, x, y, width, height):
        return
        if self.label:
            self.label.position = (x, y + height)

    def init_panel_with_stats(self):
        self.label = cocos.text.Label(
            str(getGamePlayer().health),
            font_name='Helvetica',
            font_size=16,
            anchor_x='left', anchor_y='top'
        )

        Global.Layers.globalPanel.add(self.label)

    def setHealth(self, health):
        self.label.element.text = str(int(round(health)))

    damageLabels = []

    def add_damage_label(self, damage, position):
        label = cocos.text.Label(
            '-' + str(int(round(damage))),
            font_name='Helvetica',
            font_size=10, bold=True,
            color=(255, 0, 0, 255),
            anchor_x='center', anchor_y='center'
        )
        label.deleteWhenHided = True
        label.position = position
        label.do(MoveBy((0, 100), 2) | FadeOut(2))
        self.globalPanel.add(label)

    def removeLabelsWithDamage(self):
        for label in self.globalPanel.get_children():
            if isinstance(label, cocos.text.Label) and not int(label.opacity):
                self.globalPanel.remove(label)

    def add_random_bot(self):
        x, y = randint(0, 2000), randint(0, 2000)
        rotate = randint(0, 360)
        self.add_tank(Tank(x, y, rotate))

    def printDebugInfo(self):
        bullets = Global.getGameBullets()
        tanks = Global.getGameTanks()
        walls = Global.getGameWalls()
        CM = Global.CollisionManager
        LayersTanks = Global.Layers.tanks
        LayersWalls = Global.Layers.walls
        LayersBullets = Global.Layers.bullets
        LayersAnimations = Global.Layers.globalPanel

        print('bullets', len(bullets),
              'LayersBullets', len(LayersBullets.children),
              'LayersAnimations', len(LayersAnimations.children),
              'CollisionManager', len(CM.objs),
              'tanks', len(tanks))

    def playAnimationsQueue(self):
        for animation in Global.AnimationsQueue:
            a = animation['anim']()
            a.appendAnimationToLayer(animation['position'], animation['rotation'])

        Global.AnimationsQueue = []

    sumDt = 30.0

    def callPeriodicalEvent(self, dt):
        self.sumDt += dt

        if self.sumDt > 30:
            self.sumDt = 0.0

            w, h = Global.MapWidth, Global.MapHeight

            addGamePlayer(type=1, clan=1, position=(w / 2 - 150, 300), bot=True, rotation=180)
            # addGamePlayer(type=1, clan=1, position=(1120, 200), bot=True, rotation=180)
            addGamePlayer(type=1, clan=1, position=(w / 2 + 150, 300), bot=True, rotation=180)
            #
            addGamePlayer(type=2, clan=2, position=(w / 2 - 150, h - 300), bot=True)
            # addGamePlayer(type=2, clan=2, position=(1120, 3640), bot=True)
            addGamePlayer(type=2, clan=2, position=(w / 2 + 150, h - 300), bot=True)
