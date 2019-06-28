from concepts.worldstate import WorldState
from scene.situation import Situation
from concepts.project import Project
from story.plot import PlotGraph
from story.transition import Transition

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
        self.situations = self.create_situations()

    def __str__(self):
        transitions = "\n".join(map(lambda x: f'{x.start_value} -> {x.end_value}', self.possible_transitions))
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
                        for char in self.world_state.characters:
                            transition_space.append(Transition(char, "location", loc, loc2))
        for obj in self.world_state.objects:
            for char in self.world_state.characters:
                for char2 in self.world_state.characters:
                    if char != char2:
                        transition_space.append(Transition(obj, "owner", char, char2))
        if len(transition_space) is 0:
            return self.init_possible_transitions()
        return transition_space

    def print_possible_transitions(self):
        print("Possible transitions:")
        for transition in self.possible_transitions:
            print(str(transition.start_value), "->", str(transition.end_value))

    def create_goal(self, character):
        """
        Find a transition object whose end state represents the change the character wants to see in the world state
        """
        pool = list(filter(lambda x: x.get_person() is character, self.possible_transitions))
        goal = random.choices(pool)[0]

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

    def create_situations(self):
        """
        A list of things that have to be handled within the story. World state (including characters) must be introduced,
        and plot must be furthered
        Todo: not all introductions must be done before any plot points are handled
        """
        situations = []
        added = []
        main_char = self.world_state.characters[0]
        #add topics that introduce the starting state of the story
        for attribute in main_char.attributes.items():
            situations.append(Situation(self.world_state, "P", self.world_state.characters, Project(main_char, attribute, "present", True), main_char.attributes["location"]))
        for plotpoint in self.graph.nodes:
            predecessors = list(self.graph.predecessors(plotpoint))
            if plotpoint.elem is "G":
                success = True
            if plotpoint.elem is "A":
                success = plotpoint.goal.start_value != plotpoint.goal.end_value
            if plotpoint.elem is "P":
                success = plotpoint.goal.start_value != plotpoint.goal.end_value
            if plotpoint.elem is "IE":
                success = True
            situations.append(Situation(self.world_state, plotpoint.elem, self.world_state.characters, Project(plotpoint.subj, plotpoint.transition, "present", success), main_char.attributes["location"]))
            self.world_state.change(plotpoint.elem, plotpoint.subj, plotpoint.goal, success)
            added.append(plotpoint)

            if len(predecessors) > 1:
                for predecessor in predecessors:
                    if predecessor not in added:
                        if predecessor.elem is "A":
                            situations.append(Situation(self.world_state, "P", self.world_state.characters, Project(predecessor.subj, predecessor.transition, "past", True), main_char.attributes["location"]))
                            situations.append(Situation(self.world_state, predecessor.elem, self.world_state.characters, Project(predecessor.subj, predecessor.transition, "past", True), main_char.attributes["location"]))
                            added.append(plotpoint)
            if len(list(self.graph.successors(plotpoint))) is 0:
                break

        return situations


def main():
    s = Story()
    print(s)


if __name__ == "__main__":
    main()
