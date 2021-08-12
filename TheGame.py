# TODO: Fucking refactoring
# TODO: Dependencies resources(numer of links)

import random as rnd
import networkx
from GraphGenerator import SwitchInitializer, GraphInitializer, BinomialInitializer
import matplotlib.pyplot as plt

import numpy as np

num_agents = 5
money_at_start = 10
connection_probability = 0.2

class TheGame:
    def __init__(self, graph=GraphInitializer(), start_resource=1):
        self.graph = graph
        self.resource = [start_resource for k in range(graph.size)]

    def random_donation(self, giving_node):
        receiving_node = self.graph.random_connected_node(giving_node)
        if self.resource[giving_node] == 0:
            return False
        self.resource[giving_node] -= 1
        self.resource[receiving_node] += 1
        return True

    def assume_random_donation(self, giving_node):
        receiving_node = self.graph.random_connected_node(giving_node)
        if self.resource[giving_node] == 0:
            return -1
        return receiving_node

    def async_random_donation(self):
        turn_order = list(range(self.graph.size))
        rnd.shuffle(turn_order)
        for node in turn_order:
            self.random_donation(node)

    def sync_random_donation(self, number_of_steps, max_amount_of_donation=1):
        for step in range(number_of_steps):
            if step % 1000 == 0:
                print(step, ' of ', number_of_steps)
            transaction_list = list()
            for donate_from in range(self.graph.size):
                donate_to = self.graph.random_connected_node(donate_from)
                if max_amount_of_donation <= self.resource[donate_from]:
                    transaction_list += [[donate_from, donate_to, rnd.randint(1,max_amount_of_donation)],]
            for transaction in transaction_list:
                self.resource[transaction[0]] -= transaction[2]
                self.resource[transaction[1]] += transaction[2]

    def sync_random_donation_link_based(self, number_of_steps, p):
        for step in range(number_of_steps):
            if step % 1000 == 0:
                print(step, ' of ', number_of_steps)
            transaction_list = list()
            for donate_from in range(self.graph.size):
                donate_to_candidates = list(self.graph.graph[donate_from])
                rnd.shuffle(donate_to_candidates)
                max_possible_donation = self.resource[donate_from]
                for donate_to in donate_to_candidates:
                    if rnd.random() <= p and max_possible_donation > 0:
                        transaction_list += [[donate_from, donate_to], ]
                        max_possible_donation -= 1

            for transaction in transaction_list:
                self.resource[transaction[0]] -= 1
                self.resource[transaction[1]] += 1

    # def update_resources_distribution(self):


    """GRAPH VISUALIZATION"""

    def export_networkx(self):
        exp = networkx.Graph()
        exp.add_nodes_from(list(range(self.graph.size)))
        for k in range(self.graph.size):
            for j in self.graph.graph[k]:
                exp.add_edges_from([(k,j),(j,k)])
        return exp

    def print_networkx(self):
        # Find a max resource value:
        max_resource = max(self.resource)

        colors = list()
        for k in range(len(self.resource)):
            colors += [(self.resource[k]/max_resource, 0, 0), ]

        """Visualization part"""
        figures, axes = plt.subplots(1,3, figsize=plt.figaspect(0.5))

        axes[0].set_axis_off()
        axes[1].hist(self.resource, density=True)

        links_counts = [len(node) for node in self.graph.graph]
        axes[2].scatter(links_counts, self.resource)
        axes[2].set_xlabel('Link count')
        axes[2].set_ylabel('Resource amount')



        exp = self.export_networkx()

        networkx.draw_networkx(self.export_networkx(), ax=axes[0], with_labels=False, node_size=12, edge_color='gray', node_color = colors)

        plt.show()

    def hist_resources(self):
        plt.figure()
        plt.hist(self.resource)
        plt.show()




from GraphGenerator import BinomialInitializer
# sw = BinomialInitializer(0.04081632653061224)
sw = SwitchInitializer(5)
sw.build(40)
#sw.random_reconnect(10000)
#sw.burnout(50)
#sw.random_reconnect(10000)
sw.print_networkx()

game = TheGame(sw, start_resource=10)
#game.hist_resources()
game.sync_random_donation_link_based(20000, 0.99999)
# game.sync_random_donation(1000, max_amount_of_donation=9)
print('histing...')
#game.hist_resources()
game.print_networkx()
exit(0)


"""
sw = SwitchInitializer(3)
sw.build(300)
sw.random_reconnect(20000)
sw.print_networkx()
sw.burnout(500)
sw.print_networkx()
sw.random_reconnect(20000)
sw.print_networkx()

game = TheGame(sw, 10)
game.hist_resources()
game.print_networkx()
game.sync_random_donation_link_based(150000, 0.5)
print('histing...')
game.hist_resources()
exit(0)
"""