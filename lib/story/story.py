import json

from concepts.worldstate import WorldState
from loaders import load_action_types
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
        self.action_types = load_action_types()
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

        disagreement = self.get_disagreement(other_char)
        #apply differing or incorrect belief
        self.world_state.perception(main_char, disagreement, True)

        print(disagreement)
        print(other_char.perception.get_object(disagreement.obj).attributes[disagreement.attribute_name])
        print(main_char.perception.get_object(disagreement.obj).attributes[disagreement.attribute_name])

        #add topics that introduce the starting state of the story, alkutilanne
        #todo: make sure at this point to talk only about agreed topics
        for attribute in main_char.attributes.items():
            situations.append(Situation(self.world_state, "P", self.world_state.characters, Project(main_char, attribute, "statement", "present"), main_char.attributes["location"]))

        #add conflict: introduce discussion about disagreement topic
        situations.append(Situation(self.world_state, "P", self.world_state.characters, Project(disagreement.obj, (disagreement.attribute_name, disagreement.end_value), "statement", "present"), main_char.attributes["location"]))
        situations.append(Situation(self.world_state, "IE", self.world_state.characters, Project(disagreement.obj, (disagreement.attribute_name, disagreement.end_value), "statement", "present"), main_char.attributes["location"]))
        #turning point: plan to action
        situations.append(Situation(self.world_state, "G", self.world_state.characters, Project(disagreement.obj, (disagreement.attribute_name, disagreement.end_value), "action", "present"), main_char.attributes["location"]))
        #plan gets excecuted
        situations.append(Situation(self.world_state, "A", self.world_state.characters, Project(disagreement.obj, (disagreement.attribute_name, disagreement.end_value), "action", "present"), main_char.attributes["location"]))
        situations.append(Situation(self.world_state, "P", self.world_state.characters, Project(disagreement.obj, (disagreement.attribute_name, disagreement.end_value), "statement", "present"), main_char.attributes["location"]))
        #resolution
        situations.append(Situation(self.world_state, "IE", self.world_state.characters, Project(disagreement.obj, (disagreement.attribute_name, disagreement.end_value), "statement", "present"), main_char.attributes["location"]))

        return situations

    def get_disagreement(self, char):
        """
        Get one random part of the worldstate that characters disagree on, that is the conflict of the story
        """
        pool = []
        for location in char.perception.locations:
            for attribute in location.attributes:
                pool.append(Transition(location, attribute, location.attributes[attribute], self.world_state.get_opposite_attribute(location.attributes[attribute])))
        for obj in char.perception.objects:
            for attribute in obj.attributes:
                pool.append(Transition(obj, attribute, obj.attributes[attribute], self.world_state.get_opposite_attribute(obj.attributes[attribute])))
        return random.choices(pool)[0]

    def to_json(self):
        return str(self)

    def get_situations(self):
        return self.situations


def main():
    s = Story()
    print(s)


if __name__ == "__main__":
    main()
