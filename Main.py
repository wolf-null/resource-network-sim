from Graph.GraphGeneratorSwitching import GraphGeneratorSwitching
from Games.TheGameTaxes import TheGameTaxes

if __name__ == '__main__':
    # Generate the social network
    sw = GraphGeneratorSwitching(fraction_of_dropout=0.99, initial_n_connections=8, stages_of_reconnection=2000)

    # Initialize the game
    game = TheGameTaxes(graph=sw, max_payment=1000, size=200, start_resource=20000, property_tax_model=(0,0.1,0.01)) #property_tax_model=(90,90.1,0.00001)

    # Start snimation
    game.start_animation(absolute_painting=True)

