from nltk.parse.generate import generate, demo_grammar
from nltk import CFG
import networkx as nx
import matplotlib.pyplot as plt

from story.plot_cfg import grammar
from story.fabula_element import FabulaElement

import random


class PlotGraph:
    def __init__(self, world_state):
        self.grammar = CFG.fromstring(grammar)
        self.world_state = world_state
        self.graph = nx.DiGraph()
        self.createNodes()

    def createNodes(self):
        char = random.choices(self.world_state.characters)[0]

        generated = []
        for pair in generate(self.grammar, depth=5):
            generated.append(pair)
        plot = random.choices(generated)[0]

        for i in range(len(plot)):
            self.graph.add_node(FabulaElement(plot[i], char, self.world_state))
        nodes = list(self.graph.nodes())
        for i in range(len(nodes)):
            if i < len(nodes) - 1 and nodes[i+1].elem != "E":
                self.graph.add_edge(nodes[i], nodes[i+1])

    def printPlot(self):
        layout = nx.spring_layout(self.graph)
        nx.draw(self.graph, layout)
        labels = {x: x.elem for x in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, layout, labels)
        plt.show()
