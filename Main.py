from Graph.GraphGeneratorSwitching import GraphGeneratorSwitching
from Games.TheGameTrusted import TheGameTrusted
from Games.TheGameAsyncVariousGenerosity import TheGameAsyncVariousGenerosity
from Games.TheGameTaxes import TheGameTaxes

import keyboard
import matplotlib.pyplot as plt
import statistics as stat

import seaborn as sb
import pandas as pd

sw = GraphGeneratorSwitching(fraction_of_dropout=0.99, initial_n_connections=8, stages_of_reconnection=2000)
# game = TheGameTrusted(graph=sw, max_payment=100, size=500, start_resource=10000)
game = TheGameTaxes(graph=sw, max_payment=100, size=200, start_resource=20000, property_tax_model=(0,0.1,0.01)) #property_tax_model=(90,90.1,0.00001)
game.print_network()
iteration = 0

while True:
    print("\titer: ", iteration)

    game.simulate(number_of_steps=100)
    game.update_network(absolute_painting=True)

    if keyboard.is_pressed('pause'):
        plt.ioff()
        plt.show()
        break

    if keyboard.is_pressed('prtscn'):
        pass
    iteration += 1


exit(0)
