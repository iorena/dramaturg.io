import networkx as nx
import matplotlib.pyplot as plt

from story.fabula_element import FabulaElement

import random


class PlotGraph:
    """
    Todo: more complex graph where more than one character can have goals and actions. Selection of nodes that are written out as story, rest are implicated?
    """
    def __init__(self, world_state, possible_transitions):
        self.world_state = world_state
        self.graph = nx.DiGraph()
        self.create_nodes()
        # make a graph of possible transitions and expand from there?
        self.possible_transitions = possible_transitions

    def create_nodes(self):
        """
        Excluding Events for now
        """
        for char in self.world_state.characters:
            for i in range(len(char.goals)):
                goal = char.goals.pop(-1)
                self.graph.add_node(FabulaElement("G", char, goal))
                #todo: check if goal is a possible transition, add possibility of failed action
                self.graph.add_node(FabulaElement("A", char, goal))
                self.graph.add_node(FabulaElement("P", char, goal))
                self.graph.add_node(FabulaElement("IE", char, None))

        nodes = list(self.graph.nodes())
        for i in range(len(nodes)):
            if i < len(nodes) - 1 and nodes[i+1].subj is nodes[i].subj:
                self.graph.add_edge(nodes[i], nodes[i+1])
            #add cross-character edge
            if nodes[i].elem is "A" and i > 2:
                self.graph.add_edge(nodes[i], nodes[i-3])

    def print_plot(self):
        color_map = ["green","green","green","green","blue","blue","blue","blue"]
        layout = nx.spring_layout(self.graph)
        nx.draw(self.graph, layout, node_color=color_map)
        labels = {x: x.elem for x in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, layout, labels)
        plt.show()
