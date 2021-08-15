from GraphGenerator import GraphGenerator
import random as rnd


class GraphGeneratorBinomial(GraphGenerator):
    def __init__(self, connection_prob=0.03):
        super().__init__()
        self.connection_prob = connection_prob

    def build(self, size):
        super().build(size)
        self.size = size

        while True:
            self.graph = [set() for k in range(size)]
            for k in range(size):
                for j in range(k+1, size):
                    if rnd.random() <= self.connection_prob:
                        self.graph[k] |= {j, }
                        self.graph[j] |= {k, }
            if self.check_total_connectivity():
                number_of_connections = sum([len(node) for node in self.graph])/2
                print("number of connections: ", number_of_connections)
                return self.graph
