from Graph.GraphGeneratorSwitching import GraphGeneratorSwitching
from Games.TheGameTaxes import TheGameTaxes

import keyboard
import matplotlib.pyplot as plt

sw = GraphGeneratorSwitching(fraction_of_dropout=0.99, initial_n_connections=8, stages_of_reconnection=2000)
game = TheGameTaxes(graph=sw, max_payment=100, size=200, start_resource=20000, property_tax_model=(0,0.1,0.01)) #property_tax_model=(90,90.1,0.00001)
game.print_network()
iteration = 0

while True:
    print("\titer: ", iteration)

    game.simulate(number_of_steps=100)
    game.update_network(absolute_painting=True)

    if keyboard.is_pressed(' '):
        plt.ioff()
        plt.show()
        break

    iteration += 1


exit(0)
