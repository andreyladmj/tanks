import cocos


class HealthSprite(cocos.sprite.Sprite):
    healthLayer = None
    target = None
    spriteName = 'assets/50x5.png'

    def __init__(self):
        super(HealthSprite, self).__init__(self.spriteName)

    def updateHealthPosition(self, position):
        x, y = position
        self.position = (x - 5, y + 40)

    def setHealth(self, health):
        percent = max(health, 0) / 100.
        self.scale_x = percent
