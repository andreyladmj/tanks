from threading import Timer

from cocos import sprite
from pyglet.image import load_animation

from objects.animations.AnimationTypes import OnceAnimation


class ExplosionTankAnimation(sprite.Sprite):
    # src = 'assets/booms/4517769.gif'
    src = 'assets/weapons/Metal-slug-sprites-explosions-001.gif'

    def __init__(self):
        self.animation = load_animation(self.src)
        self.animation.frames[-1].duration = None  # stop loop

        super(ExplosionTankAnimation, self).__init__(self.animation)

        self.anim = OnceAnimation(self.animation)
        self.anim.image_anchor = (self.animation.get_max_width() / 2, self.animation.get_max_height() / 4)
        self.anim.scale = 0.5

    def getAnimation(self):
        return self.animation

    def appendAnimationToLayer(self, position):
        self.anim.position = position
        addanimationToGame(self.anim)
        # Global.Layers.addAnimation(self.anim)
        # t = Timer(self.animation.get_duration(), lambda: Global.Layers.removeAnimation(self.anim))
        # t.start()
