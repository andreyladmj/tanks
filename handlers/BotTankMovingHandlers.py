import math
from threading import Thread

import time

import operator

from Landing.Center import Center
from components import Global
from movingHandlers.DefaultTankMovingHandlers import DefaultTankMovingHandlers
from objects.Tank import Tank


class BotTankMovingHandlers(DefaultTankMovingHandlers):
    speed = 120
    target = None  # type: Tank
    '''
    actions: fire, rotate gun
    observations: K-nearest tanks, current position, gun rotation, tank rotation
    '''

    def step(self, dt):
        super(BotTankMovingHandlers, self).step(dt)  # Run step function on the parent class.

        if self.findNearPlayerAndAttack() or self.findNearBuildingAndAttack():
            self.reduceSpeed()
        else:
            self.setDefaultMoving()

        self.checkPosition()

        # turns_direction = Global.CurrentKeyboard[self.RIGHT] - Global.CurrentKeyboard[self.LEFT]
        # moving_directions = Global.CurrentKeyboard[self.UP] - Global.CurrentKeyboard[self.DOWN]
        # gun_turns_direction = Global.CurrentKeyboard[self.GUN_RIGHT] - Global.CurrentKeyboard[self.GUN_LEFT]
        #
        # if Global.CurrentKeyboard[self.FIRE_LIGHT_GUN]:
        #     self.target.fire()
        #
        # if Global.CurrentKeyboard[self.FIRE_HEAVY_GUN]:
        #     self.target.heavy_fire()
        #
        # self.addSpeed(moving_directions)
        #
        # # Set the object's velocity.
        # self.setTankRotation(turns_direction, moving_directions)
        # new_velocity = self.getVelocity()
        #
        # new_position = tuple(map(operator.add, self.target.position, new_velocity))
        #
        # if self.checkCollisionsWithObjects():
        #     self.target.velocity = (0, 0)
        #     self.target.position = self.target.old_position
        # else:
        #     self.target.old_position = self.target.position
        #     new_velocity = self.getVelocityByNewPosition(self.target.position, new_position)
        #     self.setNewVelocity(new_velocity)
        #
        #
        # # SHOULD REDUCE SPEED IF NEXT POSITION IS WALL
        # #self.setNewVelocity(new_velocity)
        # self.setGunPosition()
        #
        # # Set the object's rotation
        # self.setGunRotation(gun_turns_direction)

    def check_position(self):
        if not self.findNearPlayerAndAttack():
            if not self.findNearBuildingAndAttack():
                self.setDefaultMoving()

    def findNearPlayerAndAttack(self):
        player, distanse = self.getPlayerByShortestDistanse()

        if player and distanse < 600:
            angleToPlayer = getAngleWithObject(self.target, player)
            self.rotateGunToObject(player)
            diffAngle = getDiffAngleInSector(self.target.getGunRotation(), angleToPlayer)

            if diffAngle < 4:
                self.target.heavy_fire()
            return True
        return False

    def findNearBuildingAndAttack(self):
        building, distanse = self.getBuildingByShortestDistanse()

        if building and distanse < 600:
            angleToPlayer = getAngleWithObject(self.target, building)
            self.rotateGunToObject(building)
            diffAngle = getDiffAngleInSector(self.target.getGunRotation(), angleToPlayer)

            if diffAngle < 4:
                self.target.heavy_fire()
            return True

        return False

    def goto(self, x, y):
        currx, curry = self.target.position

        if getLength(currx, curry, x, y) > 10:
            angle = getAngle(currx, curry, x, y)
            self.rotateToAngle(angle)
            # self.addSpeed(1)

    def checkPosition(self):
        new_velocity = self.getVelocity()
        new_position = tuple(map(operator.add, self.target.position, new_velocity))

        if self.checkCollisionsWithObjects():
            self.target.velocity = (0, 0)
            self.target.position = self.target.old_position
        else:
            self.target.old_position = self.target.position
            new_velocity = self.getVelocityByNewPosition(self.target.position, new_position)
            self.setNewVelocity(new_velocity)

    def rotateGunToAngle(self, angle):
        gunAngle = abs(self.target.gun_rotation() % 360)
        angleDiff = self.getDiffAngle(gunAngle, angle)
        self.target.gun_rotation += angleDiff * self.target.rotation_speed

    def rotateToAngle(self, angle):
        tankAngle = abs(self.target.rotation % 360)
        angleDiff = self.getDiffAngle(tankAngle, angle)
        self.target.rotation += angleDiff * self.target.rotation_speed

    def getDiffAngle(self, tankAngle, angle):
        angleDiff = math.floor(tankAngle - angle)

        if angleDiff == -180: angleDiff -= 1

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            return -1
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            return 1

        return 0

    def rotateGunToObject(self, player):
        angleToPlayer = getAngleWithObject(self.target, player)
        gunAngle = abs(self.target.getGunRotation() % 360)
        angleDiff = gunAngle - angleToPlayer

        if abs(angleDiff) < 2: return

        if (angleDiff > 0 and angleDiff < 180) or angleDiff < -180:
            self.target.gun_rotation -= 1
        elif (angleDiff < 0 and angleDiff > -180) or angleDiff > 180:
            self.target.gun_rotation += 1

    def getPlayerByShortestDistanse(self):
        shortest_distanse = 0
        shortest_player = None

        for player in Global.getGameTanks():
            if player.clan == self.target.clan: continue

            distanse = self.getDistanceByPlayer(player)

            if not shortest_distanse or distanse < shortest_distanse:
                shortest_distanse = distanse
                shortest_player = player

        return shortest_player, shortest_distanse

    def getBuildingByShortestDistanse(self):
        shortest_distanse = 0
        shortest_building = None

        for building in Global.getGameObjects():
            # if building.type != 5: continue
            if building.clan == self.target.clan: continue

            x1, y1 = self.target.position
            x2, y2 = building.position
            distanse = getLength(x1, y1, x2, y2)

            if not shortest_distanse or distanse < shortest_distanse:
                shortest_distanse = distanse
                shortest_building = building

        return shortest_building, shortest_distanse

    def getDistanceByPlayer(self, player):
        x1, y1 = self.target.position
        x2, y2 = player.position
        return getLength(x1, y1, x2, y2)

    def setDefaultMoving(self):
        clan = 2 - self.target.clan + 1
        # center = Global.GameObjects.getCenter(clan)
        # x, y = center.position

        enemyCenter = self.getEnemyCenter(self.target.clan)

        self.goto(*enemyCenter.position)

    def getEnemyCenter(self, clan):
        for obj in Global.getGameObjects():
            if isinstance(obj, Center) and obj.clan != clan:
                return obj

        # if self.target.clan == 1:
        # self.goto(1120, 3740)
        # else:
        # self.goto(1120, 100)

        # #self.setGunPosition()
        # new_velocity = self.getVelocity()
        #
        # new_position = tuple(map(operator.add, self.target.position, new_velocity))
        # if self.checkCollisionsWithObjects():
        #     self.target.velocity = (0, 0)
        #     self.target.position = self.target.old_position
        # else:
        #     self.target.old_position = self.target.position
        #     new_velocity = self.getVelocityByNewPosition(self.target.position, new_position)
        #     self.setNewVelocity(new_velocity)

        # Set the object's rotation
        # self.setGunRotation(gun_turns_direction)

    def addSpeed(self, moving_directions=None):
        if moving_directions:
            speed = self.speed + self.target.speed_acceleration * moving_directions

            if abs(speed) < self.target.max_speed:
                self.speed = speed

        else:
            self.reduceSpeed()

    def reduceSpeed(self):
        if self.speed > 0:
            self.speed -= self.target.speed_acceleration
        elif self.speed < 0:
            self.speed += self.target.speed_acceleration

        if abs(self.speed) < self.target.speed_acceleration:
            self.speed = 0


def getLength(x1, y1, x2, y2):
    deltax = math.pow(x1 - x2, 2)
    deltay = math.pow(y1 - y2, 2)
    return math.sqrt(deltax + deltay)


def getAngle(x1, y1, x2, y2):
    deltaX = x2 - x1
    deltaY = y2 - y1
    rad = math.atan2(deltaX, deltaY)
    return rad * (180 / math.pi) + 180


def getMinDiffAngle(angle):
    return min(180 - angle % 180, angle % 180)


def getDiffAngleInSector(angle1, angle2):
    angle1 = getMinDiffAngle(angle1)
    angle2 = getMinDiffAngle(angle2)
    return abs(angle1 - angle2)


def getAngleWithObject(obj1, obj2):
    x1, y1 = obj1.position
    x2, y2 = obj2.position
    return getAngle(x1, y1, x2, y2)
