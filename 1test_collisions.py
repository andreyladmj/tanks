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
