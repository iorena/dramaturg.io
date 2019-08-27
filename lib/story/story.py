from concepts.worldstate import WorldState
from loaders import load_action_types, load_topics
from scene.situation import Situation
from concepts.project import Project
from story.transition import Transition

from nltk.parse.generate import generate
from nltk import CFG
from scene.situation_grammar import grammar

import random
import copy
import json


class Story:
    def __init__(self, embeddings):
        self.embeddings = embeddings
        self.world_state = WorldState()
        self.pos_topics, self.neg_topics = load_topics(self.world_state)
        self.pos_topics.sort(key=lambda x: x.score)
        self.neg_topics.sort(key=lambda x: x.score)
        self.possible_transitions = self.init_possible_transitions()
        for char in self.world_state.characters:
            char.set_random_perceptions(WorldState(self.world_state))
            char.set_goal(self.create_goal(char))
        self.action_types = load_action_types()
        self.grammar = CFG.fromstring(grammar)
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
        chars = [main_char, other_char]
        chars_reversed = copy.copy(chars)
        chars_reversed.reverse()


        #add topics that introduce the starting state of the story, alkutilanne
        for attribute in main_char.attributes.items():
            situations.append(Situation(self.world_state, self.embeddings, "in", chars, Project(main_char, "olla", attribute, "present", 1), None, main_char.attributes["location"]))

        cabin = self.world_state.get_opposite(main_char.attributes["location"])
        #let's go to the cabin
        #make sure second character doesn't want to go to the cabin
        chars[0].perception.locations[cabin.id].attributes["appraisal"] = self.world_state.appraisals[4]
        chars[1].perception.locations[cabin.id].attributes["appraisal"] = self.world_state.appraisals[1]

        for sit in generate(self.grammar, n=1):
            i = 0
            for situation in sit:
                if i == 0 or i == len(sit):
                    project = Project(main_char, "mennä", ("location", cabin), "present", 5)
                elif situation == "in":
                    project = situations[-2].main_project
                elif situation == "out":
                    #pick project from ordered list
                    if i % 2 == 0:
                        pool = self.pos_topics
                    else:
                        pool = self.neg_topics
                    project = random.choices(pool)[0]
                    for proj in pool:
                        pool.remove(proj)
                        if proj == project:
                            break
                elif situation == "meta":
                    project = situations[-1].main_project
                situations.append(Situation(self.world_state, self.embeddings, situation, self.world_state.characters, project, situations[i-1].main_project, main_char.attributes["location"]))
                i += 1

        situations.append(Situation(self.world_state, self.embeddings, "in", chars, Project(main_char, "mennä", ("location", cabin), "present", 5), situations[-1].main_project, main_char.attributes["location"]))


        #reprise main question
        situations.append(Situation(self.world_state, self.embeddings, "in", self.world_state.characters, Project(main_char, "mennä", ("location", self.world_state.get_opposite(main_char.attributes["location"])), "present", 5), Project(main_char, "mennä", ("location", cabin), "present", 5), main_char.attributes["location"]))

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
