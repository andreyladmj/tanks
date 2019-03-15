import cocos.collision_model as cm
import cocos.euclid as eu

import Global
from Global import get_main_layer


class Explosion():
    def __init__(self, bullet):
        center_x, center_y = bullet.position
        self.radius = bullet.damageRadius
        self.cshape = cm.CircleShape(eu.Vector2(center_x, center_y), bullet.damageRadius)
        self.bullet = bullet

    def checkDamageCollisions(self):
        main_scene = get_main_layer()

        for tank in main_scene.tanksLayer.get_children():
            tank.cshape = cm.AARectShape(tank.position, tank.width // 2, tank.height // 2)

        damage_collisions = Global.CollisionManager.objs_colliding(self)

        if damage_collisions:
            # for damage_wall in main_scene.objectsLayer.get_children():
            #     if damage_wall.type == 'destroyable':
            #         if damage_wall in damage_collisions:
            #             damage_wall.damage(self.bullet)

            for player in main_scene.tanksLayer.get_children():
                if player in damage_collisions:
                    dmg = player.damage(self.bullet)
                    # print('FIRED TANK OBSERVATIONS', self.bullet.fired_tank.observations, self.bullet.fired_tank)

                    self.bullet.fired_tank.set_reward(dmg)

            # for enemy in Global.objects['enemies']:
            #     if enemy in damage_collisions:
            #         enemy.damage(self.bullet)

    def checkDamageCollisionsOLD(self):
        damage_collisions = Global.CollisionManager.objs_colliding(self)

        if damage_collisions:
            for damage_wall in Global.getGameWalls():
                if damage_wall in damage_collisions:
                    damage_wall.damage(self.bullet)

        for player in Global.getGameTanks():

            # if parent_id == player.id: continue

            player_points = player.getPoints()
            if Collisions.check(player_points, self.bullet.position):
                player.damage(self.bullet)

        # for enemy in Global.objects['enemies']:
        #
        #     #f parent_id == enemy.id: continue
        #
        #     enemy_points = enemy.getPoints()
        #     if Collisions.check(enemy_points, self.bullet.position):
        #         enemy_points.damage(self.bullet)
