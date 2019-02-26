from cocos import sprite

from Global import get_main_layer


class OnceAnimation(sprite.Sprite):
    def on_animation_end(self):
        # Global.Layers.removeAnimation(self)
        get_main_layer().dispatch_event('remove_animation', self)
        self.delete()
