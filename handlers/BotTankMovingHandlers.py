import math
import random

from cocos import actions

import operator

from Global import get_main_layer
from objects.Tank import Tank


class BotTankMovingHandlers(actions.Move):
      # type: Tank
    '''
    actions: fire, rotate gun
    observations: K-nearest tanks, current position, gun rotation, tank rotation
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.speed = 5
        self.target = None
        self.observations = []
        self.actions = []
        self.rewards = []

    def step(self, dt):
        super(BotTankMovingHandlers, self).step(dt)  # Run step function on the parent class.

        observation = self.get_observation()
        self.observations.append(observation)
        action = self.get_predicted_action(observation)

        if action == 0: pass
        if action == 1: self.gun_rotate(-1)
        if action == 2: self.gun_rotate(1)
        if action == 3: self.target.fireFirstWeapon()

        reward = self.get_reward()

        self.actions.append(action)
        self.rewards.append(reward)
        print(self.rewards)
        print(self.actions)
        print('')

    def policy_rollout(self, env):
        observation, reward, done = env.reset(), 0, False
        obs, acts, rews = [], [], []

        while not done:

            env.render()
            obs.append(observation)

            action = act(observation)
            observation, reward, done, _ = env.step(action)

            acts.append(action)
            rews.append(reward)

        return obs, acts, rews

    def get_reward(self):
        return self.target.get_reward()

    def get_observation(self):
        return get_main_layer().get_observation(self.target)

    def get_predicted_action(self, observation):
        return random.randint(0, 3)

    def gun_rotate(self, direction):
        self.target.gun_rotation += direction

    def rotate(self, direction):
        self.target.rotation += direction

    def move(self):
        new_velocity = self.getVelocity()
        new_position = tuple(map(operator.add, self.target.position, new_velocity))
        new_velocity = self.getVelocityByNewPosition(self.target.position, new_position)
        self.target.velocity = new_velocity

    def getVelocityByNewPosition(self, current_position, new_position):
        curr_x, curr_y = current_position
        new_x, new_y = new_position
        diff_x = new_x - curr_x
        diff_y = new_y - curr_y

        return (diff_x, diff_y)

    def getVelocity(self):
        tank_rotation = self.target.rotation
        cos_x = math.cos(math.radians(tank_rotation + 180))
        sin_x = math.sin(math.radians(tank_rotation + 180))
        return (self.speed * sin_x, self.speed * cos_x)

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
