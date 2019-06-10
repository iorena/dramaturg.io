from concepts.worldstate import WorldState
from concepts.topic import Topic
from sequence.sequence import Sequence
from story.plot import PlotGraph

import random
import copy

class Story:
    def __init__(self):
        self.world_state = WorldState()
        self.possible_transitions = self.init_possible_transitions()
        for char in self.world_state.characters:
            char.set_perception(WorldState(self.world_state))
            char.set_goal(self.create_goal(char))
        self.graph = self.create_plot_points()
        self.topics = self.create_topics()
        self.sequences = self.create_sequences()

    def __str__(self):
        transitions = "\n".join(map(lambda x: f'{x[0]} -> {x[1]}', self.possible_transitions))
        return f"{self.world_state}\nPossible transitions:\n{transitions}"

    def init_possible_transitions(self):
        """
        Creates a list of tuples representing all possible transitions, keeping each transition at random
        """
        transition_space = []
        for loc in self.world_state.locations:
            for loc2 in self.world_state.locations:
                if loc != loc2:
                    if random.random() > 0.5:
                        transition_space.append((loc, loc2))
        if len(transition_space) is 0:
            return self.init_possible_transitions()
        return transition_space

    def print_possible_transitions(self):
        print("Possible transitions:")
        for transition in self.possible_transitions:
            print(str(transition[0]), "->", str(transition[1]))

    def create_goal(self, character):
        """
        Create an object that represents the change the character wants to see in the world state
        Yes, right now characters can only have goals related to themselves
        """
        pool = copy.copy(self.world_state.locations)
        pool.remove(character.attributes["location"])
        goal_loc = random.choices(pool)[0]
        goal = { character: { "location": goal_loc } }

        return goal

    def create_plot_points(self):
        """
        Create a graph of fabula elements
        Todo: Before executing each story point, ensure we can make
        a chain that doesn't go back and forth between the same states?
        Ie. this genotype can be evaluated before moving on
        """
        plot = PlotGraph(self.world_state, self.possible_transitions)
        plot.print_plot()
        return plot.graph

    def create_topics(self):
        """
        A list of things that have to be handled within the story. World state (including characters) must be introduced,
        and plot must be furthered
        Todo: not all introductions must be done before any plot points are handled
        """
        topics = []
        added = []
        main_char = self.world_state.characters[0]
        for attribute in main_char.attributes.items():
            topics.append(Topic(main_char, attribute, "statement", "present"))
        #add actual plot topics
        for plotpoint in self.graph.nodes:
            predecessors = list(self.graph.predecessors(plotpoint))
            if plotpoint.elem is "G":
                projects.append(Project(plotpoint.subj, plotpoint.transition, "action", "future"))
                added.append(plotpoint)
            if plotpoint.elem is "A":
                projects.append(Project(plotpoint.subj, plotpoint.transition, "action", "present"))
                added.append(plotpoint)
            if plotpoint.elem is "P":
                projects.append(Project(plotpoint.subj, plotpoint.transition, "statement", "present"))
                added.append(plotpoint)
            if plotpoint.elem is "IE":
                projects.append(Project(plotpoint.subj, plotpoint.transition, "statement", "present"))
                added.append(plotpoint)
            if len(predecessors) > 1:
                for predecessor in predecessors:
                    if predecessor not in added:
                        if predecessor.elem is "A":
                            projects.append(Project(predecessor.subj, predecessor.transition, "statement", "present"))
                            projects.append(Project(predecessor.subj, predecessor.transition, "action", "past"))
                            added.append(plotpoint)
                        if predecessor.elem is "P":
                            #relative clauses? "minä näin että..."
                            projects.append(Situation(predecessor.subj, predecessor.transition, "statement", "past"))
                            added.append(plotpoint)
            if len(list(self.graph.successors(plotpoint))) is 0:
                break

        return topics

    def create_sequences(self):
        """
        Generates sequences for each topic
        """
        init_sequences = []
        for topic in self.topics:
            init_sequences.append(Sequence(self.world_state.characters, topic))
        return init_sequences

    def get_sequences(self):
        return self.sequences


def main():
    s = Story()
    print(s)


if __name__ == "__main__":
    main()
