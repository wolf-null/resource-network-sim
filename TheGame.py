import random as rnd
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

    def sync_random_donation(self, number_of_steps):
        for step in range(number_of_steps):
            transaction_list = list()
            for donate_from in range(self.graph.size):
                donate_to = self.assume_random_donation(donate_from)
                if donate_to != -1:
                    transaction_list += [[donate_from, donate_to],]
            for transaction in transaction_list:
                self.resource[transaction[0]] -= 1
                self.resource[transaction[1]] += 1

    def sync_random_donation_link_based(self, number_of_steps, p):
        for step in range(number_of_steps):
            if step % 1000 == 0:
                print(step, ' of ', number_of_steps)
            transaction_list = list()
            for donate_from in range(self.graph.size):
                donate_to_candidates = list(self.graph.graph[donate_from])
                rnd.shuffle(donate_to_candidates)
                for donate_to in donate_to_candidates:
                    if rnd.random() <= p and self.resource[donate_from] > 0:
                        transaction_list += [[donate_from, donate_to], ]

            for transaction in transaction_list:
                self.resource[transaction[0]] -= 1
                self.resource[transaction[1]] += 1

    def hist_resources(self):
        plt.figure()
        plt.hist(self.resource)
        plt.show()




from GraphGenerator import BinomialInitializer
# sw = BinomialInitializer(0.04081632653061224)
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
game.sync_random_donation_link_based(150000, 0.5)
print('histing...')
game.hist_resources()
exit(0)
