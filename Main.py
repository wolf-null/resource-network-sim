from TheGameSync import TheGameSync
from TheGameAsync import TheGameAsync
from GraphGeneratorSwitching import GraphGeneratorSwitching
from GraphGeneratorBinomial import GraphGeneratorBinomial
from TheGameAsyncVariousGenerosity import TheGameAsyncVariousGenerosity

import keyboard
import matplotlib.pyplot as plt


sw = GraphGeneratorSwitching(fraction_of_dropout=0.5, initial_n_connections=2, stages_of_reconnection=1000)
# sw = GraphGeneratorBinomial(connection_prob=0.001)
# game = TheGameSync(graph=sw, start_resource=100, size=1000, p=0.999)
game = TheGameAsyncVariousGenerosity(graph=sw, max_payment=20, size=60, start_resource=20000, random_payment_direction=True)
game.print_network()

while True:
    game.simulate(number_of_steps=100)
    game.update_network()

    if keyboard.is_pressed(' '):
        plt.ioff()
        plt.show()
        break

exit(0)
