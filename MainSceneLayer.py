from itertools import chain
from threading import Timer

import cocos
import pyglet
from cocos.batch import BatchNode
from pyglet.window import key
import cocos.collision_model as cm

from Global import CurrentKeyboard, CollisionManager
from handlers.BulletMovingHandlers import BulletMovingHandlers
from handlers.UserTankMovingHandlers import UserTankMovingHandlers
from layers.TankNodeLayer import TankNodeLayer, ObjectsNodeLayer
from objects.Explosion import Explosion


class MainSceneLayer(cocos.layer.ScrollableLayer, pyglet.event.EventDispatcher):
    is_event_handler = True

    def __init__(self):
        super(MainSceneLayer, self).__init__()
        self.schedule(self.update)
        self.tanksLayer = TankNodeLayer()
        self.objectsLayer = ObjectsNodeLayer()
        self.bulletsLayer = ObjectsNodeLayer()
        self.add(self.tanksLayer)
        self.add(self.objectsLayer)
        self.add(self.bulletsLayer)

    def update(self, dt):
        self.checkCollisions()
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

    def add_tank(self, tank):
        self.tanksLayer.add_tank(tank)
        CollisionManager.add(tank)
        tank.do(UserTankMovingHandlers())

    def add_bullet(self, bullet):
        self.bulletsLayer.add_object(bullet)
        CollisionManager.add(bullet)
        bullet.do(BulletMovingHandlers())

    def add_animation(self, animation, duration=0):
        self.objectsLayer.add(animation.getSprite(), z=5)
        if duration:
            t = Timer(duration, lambda: self.objectsLayer.remove(animation.getSprite()))
            t.start()

    def remove_animation(self, animation):
        self.objectsLayer.remove(animation)

    def checkCollisions(self):
        for bullet in self.bulletsLayer.get_children():
            bullet.cshape = cm.AARectShape(bullet.position, 2, 2)
            collisions = CollisionManager.objs_colliding(bullet)

            if collisions:
                items = chain(self.objectsLayer.get_children(), self.tanksLayer.get_children())

                for item in items:
                    if item in collisions:
                        explosion = Explosion(bullet)
                        explosion.checkDamageCollisions()
                        self.bulletsLayer.remove(bullet)
                        CollisionManager.remove_tricky(bullet)

            if bullet.exceededTheLengthLimit():
                explosion = Explosion(bullet)
                explosion.checkDamageCollisions()
                self.bulletsLayer.remove(bullet)
                CollisionManager.remove_tricky(bullet)

            # if Collisions.checkWithWalls(bullet) \
            #         or Collisions.checkWithObjects(bullet, bullet.parent_id) \
            #         or bullet.exceededTheLengthLimit():
            #     bullet.destroy()

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

    def damage(self, damage, position):
        label = cocos.text.Label(
            '-' + str(int(round(damage))),
            font_name='Helvetica',
            font_size=10,
            color=(255, 0, 0, 255),
            anchor_x='center', anchor_y='center'
        )
        label.deleteWhenHided = True
        label.position = position
        # Global.Layers.globalPanel.add(label)
        Global.Layers.globalPanel.add(label)
        label.do(MoveBy((0, 100), 2) | FadeOut(2))
        self.damageLabels.append(label)

    def removeLabelsWithDamage(self):
        for label in self.damageLabels:
            if not int(label.opacity):
                if label in Global.Layers.globalPanel: Global.Layers.globalPanel.remove(label)

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
