from TheGame import TheGame
from GraphGenerator import GraphGenerator
import random as rnd


class TheGameAsync(TheGame):
    def __init__(self,  graph=GraphGenerator, size=10, start_resource=10, max_payment=1, random_payment_direction=True):
        super(TheGameAsync, self).__init__(graph, size, start_resource)
        self.max_payment = max_payment
        self.random_payment_direction = random_payment_direction

    def simulate(self, sqrt_number_of_steps):
        for step in range(sqrt_number_of_steps):
            for step_2 in range(sqrt_number_of_steps):
                node_a = rnd.randint(0, self.size-1)
                node_b = list(self.graph[node_a])[rnd.randint(0, len(self.graph[node_a])-1)]
                if rnd.random() >= 0.5 and self.random_payment_direction:
                    node_a, node_b = node_b, node_a
                amount = rnd.randint(0, min(self.max_payment, self.wealth[node_a]))
                self.wealth[node_a] -= amount
                self.wealth[node_b] += amount
