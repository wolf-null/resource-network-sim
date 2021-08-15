from TheGameSync import TheGameSync
from GraphGeneratorSwitching import GraphGeneratorSwitching

import keyboard
import matplotlib.pyplot as plt


sw = GraphGeneratorSwitching()
game = TheGameSync(graph=sw)
game.print_network()

while True:
    game.simulate(150)
    game.update_network()

    if keyboard.is_pressed(' '):
        plt.ioff()
        plt.show()
        break

exit(0)
