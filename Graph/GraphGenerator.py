import random as rnd

import networkx


class GraphGenerator:
    """
    Basic graph generator class.

    build(size) is to be override by inheritors, called by TheGame class at the initiation

    There are lots of possible network configuration. The following is implemented:
    - GraphGeneratorSync.py
    - GraphGeneratorAsync.py
    """
    def __init__(self):
        self.size = 0
        self.graph = list()
        pass

    def build(self, size):
        self.size = size
        pass

    def print(self):
        for k in range(self.size):
            print([int(j in self.graph[k]) for j in range(self.size)])

    def check_connectivity(self, a, b):
        if a == b:
            return True
        front_wave = {a}
        while True:
            new_wave = set()
            for element in front_wave:
                new_wave |= set(self.graph[element])
            if len(new_wave - front_wave) == 0:
                return False
            if b in new_wave:
                return True
            front_wave |= new_wave

    def check_total_connectivity(self):
        for a in range(self.size):
            for b in range(0, self.size):
                if not self.check_connectivity(a, b):
                    return False
        return True

    def export_networkx(self):
        exp = networkx.Graph()
        exp.add_nodes_from(list(range(self.size)))
        for k in range(self.size):
            for j in self.graph[k]:
                exp.add_edges_from([(k,j),(j,k)])
        return exp

    def dropout(self, goal_number_of_breaks, max_retries=-1):
        if max_retries == -1:
            max_retries = max(1000, goal_number_of_breaks*2)
        print("dropout...")
        retry_counter = 0
        n_breaks = 0
        while goal_number_of_breaks > 0 and retry_counter != max_retries:
            node_a = rnd.randint(0, self.size-1)
            links_from_a = self.graph[node_a]
            if len(links_from_a) <= 1:
                continue
            node_b = rnd.choice(list(links_from_a))
            if len(self.graph[node_b]) <= 1:
                continue
            self.graph[node_a] -= {node_b, }
            self.graph[node_b] -= {node_a, }
            if not self.check_connectivity(node_a, node_b):
                self.graph[node_a] |= {node_b, }
                self.graph[node_b] |= {node_a, }
                retry_counter += 1
                continue
            #retry_counter = 0
            goal_number_of_breaks -= 1
            n_breaks += 1
        print("end dropout")
        return n_breaks

    def random_connected_node(self, node_a):
        return rnd.choice(list(self.graph[node_a]))


