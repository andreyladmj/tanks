from cocos import sprite


class OnceAnimation(sprite.Sprite):
    def on_animation_end(self):
        Global.Layers.removeAnimation(self)
        self.delete()
