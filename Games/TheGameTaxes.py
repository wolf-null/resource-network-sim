from Games.TheGame import TheGame
from Graph.GraphGenerator import GraphGenerator
import random as rnd

"""
There are two probable (combinable) models of taxing:
1. Progressive income based on income value (income tax)
    -- taken from income value and take away or uniformly distributed across the network
2. Progressive income based on receiving agent's (property tax)
    -- taken at the end of each simulation and uniformly distributed 
    
tax function depends on three parameters:
    (l) low value [units]. The game won't tax transactions or agents with lower values
    (h) hi value [units]. At this amount of wealth units increment of tax stops and doesn't grow higher
    (mx) maximum tax fraction [%]. 
          _____    -mx
         /|
    ____/ |        -zero tax
    |   | |
    0   l h
    
taxes income_tax and property_tax are described with tuple of three values: (l,h,mx) or None if this tax model is disabled
     
"""

def tax_function(value, model):
    return int(value * model[2] * min(1, max(0, (value-model[0])/(model[1]-model[0]))))

class TheGameTaxes(TheGame):
    def __init__(self,  graph=GraphGenerator, size=10, start_resource=10, max_payment=10, taxes_start_from=0, taxes_saturate_at=10, income_tax_model=None, property_tax_model=None):
        super(TheGameTaxes, self).__init__(graph, size, start_resource)
        self.max_payment = max_payment
        self.income_tax_model = income_tax_model
        self.property_tax_model = property_tax_model

    def simulate(self, number_of_steps):
        wealth_to_distribute = 0
        for step in range(number_of_steps):
            for step_2 in range(number_of_steps):
                node_a = rnd.randint(0, self.size-1)
                node_b = list(self.graph[node_a])[rnd.randint(0, len(self.graph[node_a])-1)]
                if rnd.random() >= 0.5:
                    node_a, node_b = node_b, node_a
                amount = rnd.randint(0, min(self.max_payment, self.wealth[node_a]))
                income_tax = 0
                if self.income_tax_model is not None:
                    income_tax = tax_function(amount, self.income_tax_model)
                self.wealth[node_a] -= amount
                self.wealth[node_b] += amount - income_tax
                wealth_to_distribute += income_tax

        if self.property_tax_model is not None:
            for node in range(self.size):
                property_tax = tax_function(self.wealth[node], self.property_tax_model)
                self.wealth[node] -= property_tax
                wealth_to_distribute += property_tax

        for coins in range(wealth_to_distribute):
            self.wealth[rnd.randint(0, self.size-1)] += 1

        print("\tsummary taxes ", wealth_to_distribute)
