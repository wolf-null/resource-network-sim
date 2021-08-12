import random as rnd

import networkx
import matplotlib.pyplot as plt


class GraphInitializer:
    def __init__(self):
        self.size = 0
        self.graph = list()
        pass

    def build(self, size):
        self.size = size
        pass

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

    def print_networkx(self):
        figures, axes = plt.subplots(2, figsize=plt.figaspect(2))

        counts = [len(k) for k in self.graph]
        axes[1].hist(counts, bins=[k for k in range(max(counts) + 2)], density=True)
        axes[0].set_axis_off()

        networkx.draw_networkx(self.export_networkx(), ax=axes[0], with_labels=False, node_size=10, edge_color='gray')

        total_connections = sum(counts)
        max_total_connections = self.size ** 2 - self.size
        print("Connection probability: ", total_connections / max_total_connections)
        print("Number of links: ", total_connections/2)
        plt.title('Conn. prob = ' + str(round(total_connections / max_total_connections, 4)) + '\n' + type(self).__name__)

        plt.show()

    def burnout(self, number_of_breaks):
        while number_of_breaks > 0:
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
                continue
            print(number_of_breaks, ' left')
            number_of_breaks -= 1

    def random_connected_node(self, node_a):
        return rnd.choice(list(self.graph[node_a]))



class BinomialInitializer(GraphInitializer):
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
                return




class SwitchInitializer(GraphInitializer):
    def __init__(self, n_connections):
        super().__init__()
        self.n_connections = n_connections

    def random_burn(self, number_of_stages, burn_probability):
        for stage in range(number_of_stages):
            backup = self.graph
            for k in range(self.size):
                for j in self.graph[k]:
                    if rnd.random() >= burn_probability:
                        self.graph[k] -= {j,}
                        self.graph[j] -= {k,}
            if not self.check_total_connectivity():
                print("drop changes at stage ", stage)
                self.graph = backup

    def random_reconnect(self, number_of_stages):
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

        for k in range(size):
            end_point = min(k + self.n_connections + 1, size)
            reset_point = k + self.n_connections - size + 1
            self.graph[k] = self.graph[k] | set(range(k + 1, end_point))
            self.graph[k] = self.graph[k] | set(range(0, reset_point))
            for send_to in self.graph[k]:
                self.graph[send_to] |= {k,}

        self.print()

    def print(self):
        for k in range(self.size):
            print([int(j in self.graph[k]) for j in range(self.size)])





    def hist(self, plot_hist=False):
        #hist = [[k, 0] for k in range(self.size + 1)]
        #for node in self.graph:
        #    hist[len(node)][1] += 1
        #plt.figure()
        #plt.hist([])
        counts = [len(k) for k in self.graph]
        plt.subplots(2)
        plt.figure(2)
        plt.hist(counts, bins=[k for k in range(int(self.size/3))], density=True)
        return 0




class GraphGenerator:
    def __init__(self, size, initializer=GraphInitializer()):
        self.graph = initializer.build(size)


