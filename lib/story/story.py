import json

from concepts.worldstate import WorldState
from loaders import load_action_types, load_topics
from scene.situation import Situation
from concepts.project import Project
from story.plot import PlotGraph
from story.transition import Transition

import random
import copy


class Story:
    def __init__(self):
        self.world_state = WorldState()
        self.pos_topics, self.neg_topics = load_topics(self.world_state)
        self.pos_topics.sort(key=lambda x: x.score)
        self.neg_topics.sort(key=lambda x: x.score)
        self.possible_transitions = self.init_possible_transitions()
        for char in self.world_state.characters:
            char.set_perception(WorldState(self.world_state))
            char.set_goal(self.create_goal(char))
        self.action_types = load_action_types()
        self.graph = self.create_plot_points()
        self.situations = self.create_situations()

    def __str__(self):
        transitions = "\n".join(map(lambda x: f'{x.start_value} -> {x.end_value}', self.possible_transitions))
        return f"{self.world_state}\nPossible transitions: ({len(self.possible_transitions)})" #"\n{transitions}"

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

    def create_goal(self, character):
        """
        Find a transition object whose end state represents the change the character wants to see in the world state
        """
        pool = list(filter(lambda x: x.get_person() is character, self.possible_transitions))
        goal = random.choices(pool)[0]

        return goal

    def create_plot_points(self, plot_plot=False):
        """
        Create a graph of fabula elements
        Todo: Before executing each story point, ensure we can make
        a chain that doesn't go back and forth between the same states?
        Ie. this genotype can be evaluated before moving on
        """
        plot = PlotGraph(self.world_state, self.possible_transitions)
        if plot_plot:
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
        main_char = random.choices(self.world_state.characters)[0]
        other_char = self.world_state.characters[0] if main_char.id == 1 else self.world_state.characters[1]


        #add topics that introduce the starting state of the story, alkutilanne
        for attribute in main_char.attributes.items():
            situations.append(Situation(self.world_state, "P", self.world_state.characters, Project(main_char, "olla", attribute, "present", 1), main_char.attributes["location"]))

        situations.append(Situation(self.world_state, "P", self.world_state.characters, self.pos_topics[0], main_char.attributes["location"]))
        situations.append(Situation(self.world_state, "IE", self.world_state.characters, self.neg_topics[0], main_char.attributes["location"]))
        situations.append(Situation(self.world_state, "P", self.world_state.characters, self.pos_topics[1], main_char.attributes["location"]))
        situations.append(Situation(self.world_state, "P", self.world_state.characters, self.neg_topics[1], main_char.attributes["location"]))

        return situations

    def to_json(self):
        return str(self)

    def get_situations(self):
        return self.situations


def main():
    s = Story()
    print(s)


if __name__ == "__main__":
    main()
