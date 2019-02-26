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


class ObjectsNodeLayer(BatchNode):
    def add_object(self, object, z=1):
        self.add(object, z=z)

    def remove_object(self, object):
        self.remove(object)
