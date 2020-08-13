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
        self.world_state.create_object("kyllästynyt", 0)
        self.world_state.create_object("kiitollinen", 4)
        self.world_state.create_object("rakennettava", 4)
        self.world_state.create_object("kulttuuri", 4)
        self.world_state.create_object("tärkeää", 4)
        self.world_state.create_object("pois", 0)
        self.world_state.create_object("niin paljon", 4)

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
        self.situation_list = SituationGrammar().create_situations()
        situations = []
        main_char = self.world_state.characters[0]
        other_char = self.world_state.characters[1]
        third_char = self.world_state.characters[2]
        chars = [main_char, other_char]

        main_project = Project(("uusi", self.world_state.inheritance_object), "olla", ("obj", self.world_state.get_object_by_name("rakennettava")), "statement", "prees", 1)
        pre_project = Project(self.world_state.get_object_by_name("kulttuuri"), "olla", ("static", "tärkeää"), "statement", "prees", 1)

        main_char.add_belief(main_project)

        a_project = None
        b_project = None

        prev_project = None

        projects = {
            "none": (lambda x: None, []),
            "main_project": (lambda x, y: x, [main_project]),
            "prev_project": (lambda x: prev_project, []),
            "boredom_project": (Project.get_boredom_project, [other_char]),
            "dismissal_project": (Project.get_dismissal_project, [main_char]),
            "look_up_to_project": (Project.get_look_up_to_project, [main_char]),
            "complain_project": (Project.get_complain_project, [main_char, prev_project, main_project]),
            "reward_project": (Project.get_reward_project, [main_char]),
            "refer_back_project": (Project.get_refer_back_project, [prev_project, main_project]),
            "indoctrination_project": (Project.get_indoctrination_project, [main_project]),
            "pre_project": (lambda x, y: x, [pre_project])
        }

        for sit in self.situation_list:

            for entry in self.situation_rules[sit]["a_project"]:
                project = projects[entry][0]
                parameters = projects[entry][1]
                a_project = project(*parameters, other_char)
                print("%", project)
                if a_project is not None:
                    main_char.set_goal(a_project)
                    prev_project = a_project

            for entry in self.situation_rules[sit]["b_project"]:
                project = projects[entry][0]
                parameters = projects[entry][1]
                b_project = project(*parameters, main_char)
                print("#", b_project)
                if b_project is not None:
                    other_char.set_goal(b_project)
                    prev_project = b_project

            if sit == "lie_for":
                chars = [main_char, third_char]
            else:
                chars = [main_char, other_char]

            #todo: set memories?

            situations.append(Situation(sit, self.world_state, self.embeddings, chars, self.situation_rules[sit], main_char.attributes["location"]))

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
