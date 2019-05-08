from worldstate import WorldState
from concepts import location

import random
import copy


class Story:
    def __init__(self):
        self.world_state = WorldState()
        self.possible_transitions = self.init_possible_transitions()
        self.plotpoints = self.create_plot_points()
        for char in self.world_state.characters:
            char.set_perception(WorldState(self.world_state))
            char.set_goal(self.create_goal())
        self.create_plot_points()

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
        return transition_space

    def print_possible_transitions(self):
        print("Possible transitions:")
        for transition in self.possible_transitions:
            print(str(transition[0]), "->", str(transition[1]))

    def create_goal(self):
        """
        Tweaks the real world state to create a goal world state for a character
        Yes, right now all characters have goals relating to the first character
        """
        goal = copy.deepcopy(WorldState(self.world_state))
        pool = copy.copy(self.world_state.locations)
        pool.remove(self.world_state.characters[0].attributes["location"])
        goal_loc = random.choices(pool)[0]
        goal.characters[0].attributes.update({"location": goal_loc})

        return goal

    def create_plot_points(self):
        """
        Create a chain of fabula elements with a grammar
        Before executing each plot point, ensure we can make
        a chain that doesn't go back and forth between the same states
        Ie. this genotype can be evaluated before moving on
        """
        char = random.choices(self.world_state.characters)[0]
        # self.plotpoints = [(char, "acquire goal"), (char, "execute action"), (char, "percieve"), (char, "react")]
        plotpoints = [(char, {"location": location.Location(0)}), (char, (char, {"location": location.Location(0)})),
                      (char, WorldState(self.world_state)), (char, "sadness"),
                      {"element": "G", "subject": char, "data": {"location": location.Location(0)}},
                      {"element": "A", "subject": char, "data": (char, {"location": location.Location(0)})},
                      {"element": "P", "subject": char, "data": WorldState(self.world_state)},
                      {"element": "IE", "subject": char, "data": "sadness"}]
        return plotpoints
