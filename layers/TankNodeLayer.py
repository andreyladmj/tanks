from cocos.batch import BatchNode


class TankNodeLayer(BatchNode):
    def add_tank(self, tank):
        self.add(tank, z=2)
        self.add(tank.GunSprite, z=3)
        self.add(tank.healthSprite, z=4)

    def remove_tank(self, tank):
        self.remove(tank)
        self.remove(tank.GunSprite)
        self.remove(tank.healthSprite)
