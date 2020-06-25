from concepts.worldstate import WorldState
from loaders import load_action_types, load_topics, load_situations
from scene.situation import Situation
from concepts.project import Project
from story.transition import Transition
from language.dictionary import Dictionary
from scene.situation_grammar import SituationGrammar

import random
import copy
import json


class Story:
    def __init__(self, embeddings, personalities, relationships, first_verb, second_verb):
        self.embeddings = embeddings
        self.situation_rules = load_situations()
        self.world_state = WorldState(self.embeddings, personalities, relationships)
        self.create_objects()
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


    #must create all worldobjects before giving characters unique perceptions
    def create_objects(self):
        self.world_state.get_object_by_name("kyllästynyt")
        self.world_state.get_object_by_name("kiitollinen")
        self.world_state.get_object_by_name("juures")
        self.world_state.get_object_by_name("pois")

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
        situation_list = SituationGrammar().create_situations()
        situations = []
        main_char = self.world_state.characters[0]
        other_char = self.world_state.characters[1]
        chars = [main_char, other_char]
        print(situation_list)

        main_project = Project(self.world_state.inheritance_object, "olla", ("obj", self.world_state.get_object_by_name("juures")), "statement", "prees", 1)

        a_project = None
        b_project = None

        projects = {
            "none": None,
            "main_project": main_project,
            "prev_project": a_project,
            "boredom_project": Project(main_char, "olla", ("static", self.world_state.get_object_by_name("kyllästynyt")), "statement", "prees", 1),
            "dismissal_project": Project(other_char, "mennä", ("static", self.world_state.get_object_by_name("pois")), "proposal", "prees", 1),
            "reward_project": Project(other_char, "olla", ("static", self.world_state.get_object_by_name("kiitollinen")), "statement", "prees", 1)
        }

        for sit in situation_list:

            relative_died_project = Project(self.world_state.dead_relative, first_verb, (None, None),  "statement", "perf", 1)

            projects["prev_project"] = a_project
            a_project = projects[self.situation_rules[sit]["a_project"]]
            projects["prev_project"] = b_project
            b_project = projects[self.situation_rules[sit]["b_project"]]

            if a_project is not None:
                main_char.set_goal(a_project)
            if b_project is not None:
                other_char.set_goal(b_project)

            #todo: set memories?

            situations.append(Situation(self.world_state, self.embeddings, chars, self.situation_rules[sit], main_char.attributes["location"]))

            #reset moods
            for char in chars:
                char.reset_mood()

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
