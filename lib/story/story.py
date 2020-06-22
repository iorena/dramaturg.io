from concepts.worldstate import WorldState
from loaders import load_action_types, load_topics
from scene.situation import Situation
from concepts.project import Project
from story.transition import Transition
from language.dictionary import Dictionary

import random
import copy
import json


class Story:
    def __init__(self, embeddings, personalities, relationships, first_verb, second_verb):
        self.embeddings = embeddings
        self.world_state = WorldState(self.embeddings, personalities, relationships)
        for char in self.world_state.characters:
            char.set_random_perceptions(WorldState(None, None, None, self.world_state))
        self.action_types = load_action_types()
        #todo: get actual cases for verbs, and synonyms
        if first_verb not in Dictionary.verb_dictionary:
            Dictionary.verb_dictionary[first_verb] = [(first_verb, "NOM")]
        if second_verb not in Dictionary.verb_dictionary:
            Dictionary.verb_dictionary[second_verb] = [(second_verb, "NOM")]
        self.situations = self.create_situations(first_verb, second_verb)

    def __str__(self):
        return f"{self.world_state}"

    def get_title(self):
        bow = {}
        for sit in self.situations:
            for seq in sit.sequences:
                for turn in seq.turns:
                    if turn is None:
                        continue
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

    def create_situations(self, first_verb, second_verb):
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

        #char1 calls char2
        #char1 finds out that relative is dead (before scene)
        relative_died_project = Project(self.world_state.dead_relative, first_verb, (None, None),  "statement", "perf", 1)
        other_char.set_goal(relative_died_project)
        #set memory for character so isn't surprised by own news
        other_char.add_memory(relative_died_project)

        situations.append(Situation(self.world_state, self.embeddings, chars, main_char.attributes["location"]))

        #reset moods
        for char in chars:
            char.reset_mood()

        #char2 comes to get inheritance
        inheritance_want_project_main = Project(main_char, second_verb, ("object", self.world_state.inheritance_object), "proposal", "prees", 1)
        inheritance_want_project_other = Project(other_char, "ottaa", ("object", self.world_state.inheritance_object), "proposal", "prees", 1)

        main_char.set_goal(inheritance_want_project_main)
        other_char.set_goal(inheritance_want_project_other)

        situations.append(Situation(self.world_state, self.embeddings, chars, main_char.attributes["location"]))

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
