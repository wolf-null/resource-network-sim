from TheGameSync import TheGameSync
from TheGameAsync import TheGameAsync
from GraphGeneratorSwitching import GraphGeneratorSwitching
from GraphGeneratorBinomial import GraphGeneratorBinomial
from TheGameAsyncVariousGenerosity import TheGameAsyncVariousGenerosity

import keyboard
import matplotlib.pyplot as plt


sw = GraphGeneratorSwitching(fraction_of_dropout=0.8, initial_n_connections=2, stages_of_reconnection=2000)
game = TheGameAsyncVariousGenerosity(graph=sw, max_payment=20, size=20, start_resource=20000, random_payment_direction=True)
game.print_network()

while True:
    game.simulate(number_of_steps=200)
    game.update_network()

    if keyboard.is_pressed(' '):
        plt.ioff()
        plt.show()
        break

exit(0)
