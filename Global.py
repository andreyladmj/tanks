from pyglet.window import key
import cocos.collision_model as cm

CurrentKeyboard = key.KeyStateHandler()
CollisionManager = cm.CollisionManagerBruteForce()
MainLayer = None


def set_main_layer(layer):
    global MainLayer
    MainLayer = layer


def get_main_layer():
    return MainLayer

class GameFactory:
    def add_tank(self, *args, **kwargs):
        return MainLayer.add_tank(*args, **kwargs)
