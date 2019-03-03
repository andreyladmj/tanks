import numpy as np

import matplotlib.pyplot as plt
import seaborn;

seaborn.set()


class CalcCoreHelper:
    def __init__(self, tanks, objects, bullets):
        self.tanks = tanks
        self.objects = objects
        self.bullets = bullets

    def get_tanks_coords(self):
        return np.array([tank.position for tank in self.tanks.get_children()])

    def get_objects_coords(self):
        return np.array([obj.position for obj in self.objects.get_children()])

    def get_bullets_coords(self):
        return np.array([bullet.position for bullet in self.bullets.get_children()])

    def get_nearest_tanks(self, K=3):
        pass

    def update_plt(self):
        X = self.get_tanks_coords()
        print('---------+++++++++-----------')
        print(X)
        print('--------------------')
        plt.clf()
        plt.scatter(X[:, 0], X[:, 1], s=100)
        plt.show()
