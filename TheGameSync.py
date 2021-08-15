from TheGame import TheGame
from GraphGenerator import GraphGenerator
import random as rnd


class TheGameSync(TheGame):
    """
    'Synchronous' game algorithm:

    1. each agent pays to each it's neighbor with probability [p]

    In this model, as more connection agent do have as more pay probability.
    From the other hand, having a lot of neighbors allows to receive more payments

    Assumption: a single central node (without concurrents) hit the jackpot

    After
    """

    def __init__(self, graph=GraphGenerator, size=10, start_resource=10, p=0.3):
        super(TheGameSync, self).__init__(graph, size, start_resource)
        self.p = p

    def simulate(self, number_of_steps):
        for step in range(number_of_steps):
            #if step % 1000 == 0:
            #    print(step, ' of ', number_of_steps)
            transaction_list = list()
            for pay_from in range(self.size):
                pay_to_candidates = list(self.graph[pay_from])
                rnd.shuffle(pay_to_candidates)
                max_possible_transaction = self.wealth[pay_from]
                for pay_to in pay_to_candidates:
                    if rnd.random() <= self.p and max_possible_transaction > 0:
                        transaction_list += [[pay_from, pay_to], ]
                        max_possible_transaction -= 1

            for transaction in transaction_list:
                self.wealth[transaction[0]] -= 1
                self.wealth[transaction[1]] += 1
