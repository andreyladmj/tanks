from threading import Thread
from time import sleep

from cocos import director
from cocos import scene

from Global import CurrentKeyboard
from MainSceneLayer import MainSceneLayer
from objects.Tank import Tank


def main():
    createInterface()
    # res = int(raw_input('1 - create new game, 2 - connect\n'))
    # if res == 1:
    #     createInterface(1, 1, None)
    # else:
    #     createInterface(2, 2, 'localhost')
    # res = int(raw_input('1 - create new game, 2 - connect\n'))
    # clan = raw_input('Select your clan: 1 or 2\n')
    # tanktype = int(raw_input('Select your tank type: 1 - 7\n'))
    # ip = None
    #
    # if res == 2:
    #     ip = raw_input('input ip\n')
    #
    # createInterface(tanktype, clan, ip)

    # pyglet.sprite.Sprite.__init__(self, img, x = 50, y = 30)


def createInterface():
    director.director.init(width=3000, height=960, autoscale=True, resizable=True)

    # initGlobalParams()

    # Create a scene and set its initial layer.

    main_scene_layer = MainSceneLayer()
    main_scene = scene.Scene(main_scene_layer)
    main_scene.schedule(main_scene_layer.buttonsHandler)
    main_scene_layer.register_event_type('on_clicked')

    main_scene_layer.register_event_type('add_tank')

    # game_layers = Layers(main_scene_layer)
    # init_global_variables(game_layers)

    # @main_scene_layer.event
    # def on_clicked(clicks):
    #     print('ovverided', clicks)
    #     pass

    main_scene_layer.dispatch_event('on_clicked', '12314124')

    main_scene_layer.dispatch_event('add_tank', Tank(500, 500, 180))
    main_scene_layer.dispatch_event('add_tank', Tank(500, 800, 0))

    # load_map()
    #
    # if ip is None:
    #     playerId = addGamePlayer(type=tanktype, clan=clan, position=(150, 150), add_moving_handler=True)
    #     setCurrentPlayerStats(playerId)
    #
    #     thread = Thread(target = Game.callUpdatePositions)
    #     thread.setDaemon(True)
    #     thread.start()
    #
    #     # thread = Thread(target = Game.callCheckCollisions)
    #     # thread.setDaemon(True)
    #     # thread.start()
    #
    #     #proc = Process(target=connectionsListenersPump, args=(addGamePlayer,))
    #     #proc.start()
    #     #proc.join()
    #
    #     # thread = Thread(target = connectionsListenersPump)
    #     # thread.setDaemon(True)
    #     # thread.start()
    #
    #     thread = Thread(target = Game.sendDataToPlayers)
    #     thread.setDaemon(True)
    #     thread.start()
    #
    # else:
    #     #main_scene_layer.connections_listener = NetworkListener(ip, 1332, tanktype)
    #     Global.TankNetworkListenerConnection = NetworkListener(ip, 1332, tanktype, clan)

    director.director.on_resize = main_scene_layer.resize
    director.director.window.push_handlers(CurrentKeyboard)
    director.director.run(main_scene)


def connectionsListenersPump(fn):
    Global.connections_listener = Network(localaddr=('localhost', 1332))

    while True:
        fn(type=1, clan=1, position=(1070, 200), bot=True, rotation=180)
        # addGamePlayer(type=1, clan=1, position=(1070, 200), bot=True, rotation=180)
        # addGamePlayer(type=1, clan=1, position=(1120, 200), bot=True, rotation=180)
        # addGamePlayer(type=1, clan=1, position=(1170, 200), bot=True, rotation=180)

        # addGamePlayer(type=2, clan=2, position=(1070, 3640), bot=True)
        # addGamePlayer(type=2, clan=2, position=(1120, 3640), bot=True)
        # addGamePlayer(type=2, clan=2, position=(1170, 3640), bot=True)

        # Global.AnimationsQueue.append({
        #     'anim': HeavyBulletFireAnimation,
        #     'position': (100,200),
        #     'rotation': 90
        # })
        # a = HeavyBulletFireAnimation()
        # a.appendAnimationToLayer((100,200), 90)

        sleep(30)
    # while True:
    # connections_listener.Pump()
    # sleep(0.0001)
    # sleep(0.8)
    # Global.EventDispatcher.dispatch_event('create_animation', (200, 200))


if __name__ == '__main__':
    main()
