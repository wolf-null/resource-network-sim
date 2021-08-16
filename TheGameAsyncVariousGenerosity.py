from TheGame import TheGame
from GraphGenerator import GraphGenerator
import random as rnd
import matplotlib.pyplot as plt


class TheGameAsyncVariousGenerosity(TheGame):
    def __init__(self,  graph=GraphGenerator, size=10, start_resource=10, max_payment=1, random_payment_direction=True):
        super(TheGameAsyncVariousGenerosity, self).__init__(graph, size, start_resource)
        # self.generosity = [float(rnd.choice([1, 0.5, 0])) for k in range(size)]
        self.generosity = [float(rnd.random()) for k in range(size)]
        self.max_payment = max_payment
        self.random_payment_direction = random_payment_direction

    def print_right_screen(self):
        links_counts = [len(node) for node in self.graph]
        colors = [(0, g, 0) for g in self.generosity]
        self.axes[2].scatter(links_counts, self.wealth, c=colors)
        self.axes[2].set_xlabel('Link count')
        self.axes[2].set_ylabel('Resource amount')
        # super(TheGameAsyncVariousGenerosity, self).print_right_screen()


    def simulate(self, number_of_steps):
        for step in range(number_of_steps):
            for step_2 in range(number_of_steps):
                node_a = rnd.randint(0, self.size-1)
                node_b = list(self.graph[node_a])[rnd.randint(0, len(self.graph[node_a])-1)]
                if rnd.random() >= 0.5 and self.random_payment_direction:
                    node_a, node_b = node_b, node_a
                #amount = rnd.randint(0, int(min(self.max_payment * self.generosity[node_a], self.wealth[node_a])))
                amount = rnd.random() * min(self.max_payment * self.generosity[node_a], self.wealth[node_a])
                self.wealth[node_a] -= amount
                self.wealth[node_b] += amount

    def print_network(self, absolute_painting=True, block_rendering = False):
        super(TheGameAsyncVariousGenerosity, self).print_network(absolute_painting, block_rendering=True)
        colors = self.axes[0].collections[0].get_facecolor()
        for k in range(self.size):
            colors[k][1] = self.generosity[k]
        self.axes[0].collections[0].set_facecolor(colors)
        if not block_rendering:
            plt.ion()
            plt.show()
            plt.suptitle('Hold [space] to end. Total amount of wealth: ' + str(sum(self.wealth)))
            plt.pause(2.01)

    def update_network(self, absolute_painting = True, block_rendering = False):
        super(TheGameAsyncVariousGenerosity, self).update_network(absolute_painting, block_rendering=True)

        colors = self.axes[0].collections[0].get_facecolor()
        for k in range(self.size):
            colors[k][1] = self.generosity[k]
        self.axes[0].collections[0].set_facecolor(colors)

        if not block_rendering:
            plt.suptitle('Hold [space] to end. Total amount of wealth: ' + str(round(sum(self.wealth),2)))
            plt.draw()
            plt.pause(0.01)