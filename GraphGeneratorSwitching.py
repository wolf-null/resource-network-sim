from GraphGenerator import GraphGenerator
import random as rnd


class GraphGeneratorSwitching(GraphGenerator):
    def __init__(self, initial_n_connections=1, stages_of_reconnection=2000, fraction_of_dropout=0.4):
        super().__init__()
        self.n_connections = initial_n_connections
        self.stages_of_reconnection = stages_of_reconnection
        self.fraction_of_dropout = fraction_of_dropout

    def reconnect(self, number_of_stages):
        stage = 0
        while stage != number_of_stages:
            node_a = rnd.randint(0, self.size-1)
            node_b_old = rnd.choice(list(self.graph[node_a]))
            if len(self.graph[node_b_old]) == 1:
                # Can't brake. Will cause node isolation!
                continue

            possible_new_b = list(set(range(self.size)) - {node_a} - self.graph[node_a])
            if len(possible_new_b) == 0:
                continue
            node_b_new = rnd.choice(possible_new_b)
            # Delete old link:
            self.graph[node_a] -= {node_b_old, }
            self.graph[node_b_old] -= {node_a, }
            # Create new link:
            self.graph[node_a] |= {node_b_new, }
            self.graph[node_b_new] |= {node_a, }
            # Deletion of the node_b_olt might cause it's isolation, so have to check
            # Connectivity between node_a (and consequently node_b_new) and node_b_old
            if not self.check_connectivity(node_a, node_b_old):
                # Indian code undo if connectivity broke up:
                # Re-create old link:
                self.graph[node_a] |= {node_b_old, }
                self.graph[node_b_old] |= {node_a, }
                # Remove new link:
                self.graph[node_a] -= {node_b_new, }
                self.graph[node_b_new] -= {node_a, }
                continue

            stage += 1

    def build(self, size):
        super().build(size)
        self.graph = [set() for k in range(size)]

        # Build a cyclic graph
        for k in range(size):
            end_point = min(k + self.n_connections + 1, size)
            reset_point = k + self.n_connections - size + 1
            self.graph[k] = self.graph[k] | set(range(k + 1, end_point))
            self.graph[k] = self.graph[k] | set(range(0, reset_point))
            for send_to in self.graph[k]:
                self.graph[send_to] |= {k,}

        # Randomly reconnect the graph
        self.reconnect(self.stages_of_reconnection)

        # Dropout random connections
        number_of_connections = sum([len(node) for node in self.graph])/2
        number_of_dropouts = min(0, int(number_of_connections * self.fraction_of_dropout) - self.size)
        self.dropout(number_of_dropouts)

        return self.graph
