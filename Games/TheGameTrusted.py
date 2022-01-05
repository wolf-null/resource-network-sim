from Games.TheGame import TheGame
from Graph.GraphGenerator import GraphGenerator
import random as rnd


class TheGameTrusted(TheGame):
    def __init__(self,  graph=GraphGenerator, size=10, start_resource=10, max_payment=10):
        super(TheGameTrusted, self).__init__(graph, size, start_resource)
        self.max_payment = max_payment

        self.wealth_sent = {a: {b: 0 for b in self.graph[a]} for a in range(self.size)}
        self.wealth_received = {a: {b: 0 for b in self.graph[a]} for a in range(self.size)}

    def simulate(self, number_of_steps, smart_enabled=True):
        for step in range(number_of_steps):
            for step1 in range(number_of_steps):
                node_a = rnd.randint(0, self.size - 1)
                weights = [self.wealth_received[node_a][b] * self.wealth_sent[node_a][b] + 1 for b in self.graph[node_a]] #
                node_b = rnd.choices(list(self.graph[node_a]), weights, k=1)[0]

                if rnd.random() >= 0.5:
                    node_a, node_b = node_b, node_a

                amount = min(rnd.random()* self.max_payment, self.wealth[node_a])

                self.wealth[node_a] -= amount
                self.wealth[node_b] += amount

                self.wealth_sent[node_a][node_b] = amount
                self.wealth_received[node_b][node_a] = amount

    def set_max_payment(self, max_payment):
        self.max_payment = max_payment


