import cProfile
from random import randint

from Cython.Shadow import profile
from pyglet.window import key
import cocos.collision_model as cm

CollisionManager = cm.CollisionManagerBruteForce()


class Point():
    def __init__(self, x, y, w=1, h=1):
        self.cshape = cm.AARectShape((x, y), w, h)


@profile
def benchmark():
    for i in range(200000):
        i = Point(randint(0, 200), randint(0, 200), randint(0, 5), randint(0, 5))
        CollisionManager.add(i)

    i = Point(100, 100)
    collisions = CollisionManager.objs_colliding(i)
    print(collisions)


# pr = cProfile.Profile()
# pr.enable()
# benchmark()
# pr.disable()
# pr.print_stats()

benchmark(1)



import sys
sys.path.extend(['/home/andrei/Python/tanks'])
sys.path.extend(['/home/andrei/Python/tanks/assets'])

import numpy as np
from cocos import director
from cocos import scene
from cocos.batch import BatchNode
from cocos import sprite
from objects.Tank import Tank
director.director.init(width=2048, height=960, resizable=True, autoscale=False)
layer = BatchNode()
c = sprite.Sprite('gil-brazo2.png')
c.position = (12,11)
layer.add(c)
layer.add(c)
layer.get_children()

t = tanks_list[3]

tanks_list.index(t)

tanks_list = layer.get_children()
tanks = np.array(list(map(lambda obj: obj.position, tanks_list)))
dist_sq = np.sum((tanks[:, np.newaxis] - tanks[np.newaxis, :]) ** 2, axis=-1)
K = 3
nearest_sorted = np.argsort(dist_sq, axis=1)[:, :K+1]


