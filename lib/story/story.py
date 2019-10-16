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
        self.world_state = WorldState(self.embeddings)
        #self.pos_topics, self.neg_topics = load_topics(self.world_state)
        #self.pos_topics.sort(key=lambda x: x.score)
        #self.neg_topics.sort(key=lambda x: x.score)
        self.possible_transitions = self.init_possible_transitions()
        for char in self.world_state.characters:
            char.set_random_perceptions(WorldState(None, self.world_state))
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

    def get_title(self):
        bow = {}
        for sit in self.situations:
            for seq in sit.sequences:
                for turn in seq.turns:
                    for word in turn.inflected.split(" "):
                        if word in bow:
                            bow[word] = bow[word] + 1
                        else:
                            bow[word] = 1
        sorted_bow = sorted(bow.items(), key=lambda x: x[1])
        source_word_idx = random.choices([-3, -4, -5, -6])[0]
        strip_punc = sorted_bow[source_word_idx][0].replace(",", "")
        similar = self.embeddings.get_similar(strip_punc)
        return similar

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
        main_char = self.world_state.characters[0]
        other_char = self.world_state.characters[1]
        chars = [main_char, other_char]
        chars_reversed = [other_char, main_char]

        #char1 calls char2
        #char1 finds out that relative is dead (before scene)

        situations.append(Situation(self.world_state, self.embeddings, "in", chars, Project(self.world_state.dead_relative, "kuolla", ("character", other_char), "past", 5), None, main_char.attributes["location"]))

        #char2 comes to get inheritance
        situations.append(Situation(self.world_state, self.embeddings, "in", chars_reversed, Project(other_char, "ottaa", ("object", self.world_state.inheritance_object), "present", 5), Project(main_char, "soittaa", ("character", other_char), "present", 5), main_char.attributes["location"]))

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
