import networkx
import matplotlib.pyplot as plt
from GraphGenerator import GraphGenerator


class TheGame:
    def __init__(self, graph=GraphGenerator, size=10, start_resource=10):
        self.size = size
        self.graph = graph.build(size)
        self.wealth = [start_resource for k in range(size)]
        self.axes = list()

    def simulate(self, n_steps):
        pass

    def print_right_screen(self):
        links_counts = [len(node) for node in self.graph]
        self.axes[2].scatter(links_counts, self.wealth)
        self.axes[2].set_xlabel('Link count')
        self.axes[2].set_ylabel('Resource amount')


    """GRAPH VISUALIZATION"""

    def print_network(self, absolute_painting=True, block_rendering = False):
        # Find a max resource value:
        max_resource = max(self.wealth)
        min_resource = min(self.wealth)

        colors = list()
        for k in range(len(self.wealth)):
            if absolute_painting:
                colors += [(self.wealth[k] / max_resource, 0, 0), ]
            else:
                colors += [((self.wealth[k] - min_resource) / (max_resource - min_resource), 0, 0), ]

        """Visualization part"""
        figures, self.axes = plt.subplots(1,3, figsize=plt.figaspect(0.5))

        self.axes[0].set_axis_off()
        self.axes[1].hist(self.wealth, density=True)

        self.print_right_screen()

        networkx.draw_networkx(self._export_as_networkx(), ax=self.axes[0], with_labels=False, node_size=12, edge_color='gray', node_color = colors)

        figures.canvas.manager.window.attributes('-topmost',1)

        if not block_rendering:
            plt.ion()
            plt.show()
            plt.suptitle('Hold [space] to end')
            plt.pause(2.01)

    def update_network(self, absolute_painting = True, block_rendering = False):
        # Find a max resource value:
        max_resource = max(self.wealth)
        min_resource = min(self.wealth)

        colors = list()
        for k in range(len(self.wealth)):
            if absolute_painting:
                colors += [(self.wealth[k] / max_resource, 0, 0), ]
            else:
                colors += [((self.wealth[k] - min_resource) / (max_resource - min_resource), 0, 0), ]

        # Visualization part
        self.axes[1].clear()
        self.axes[2].clear()
        self.axes[1].hist(self.wealth, density=True)

        links_counts = [len(node) for node in self.graph]

        self.print_right_screen()

        self.axes[0].collections[0].set_facecolor(colors)
        #self.axes[0].collections[0].set_edgecolor('black')
        if not block_rendering:
            plt.draw()
            plt.pause(0.01)

    def hist_resources(self):
        plt.figure()
        plt.hist(self.wealth)
        plt.show()

    def _export_as_networkx(self):
        exp = networkx.Graph()
        exp.add_nodes_from(list(range(self.size)))
        for k in range(self.size):
            for j in self.graph[k]:
                exp.add_edges_from([(k, j), (j, k)])
        return exp




