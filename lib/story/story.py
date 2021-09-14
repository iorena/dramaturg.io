from concepts.worldstate import WorldState
from concepts.project import Project
from concepts.affect.emotion import Emotion
from language.dictionary import Dictionary
from loaders import load_action_types, load_topics, load_situations
from scene.situation import Situation
from scene.situation_grammar import SituationGrammar
from story.transition import Transition

import copy
import json
import random


class Story:
    def __init__(self, embeddings, personalities, relationships, verbs):
        self.embeddings = embeddings
        self.situation_rules = load_situations()
        self.world_state = WorldState(self.embeddings, personalities, relationships)
        self.create_objects()
        for char in self.world_state.characters:
            char.set_random_perceptions(WorldState(None, None, None, self.world_state))
        #todo: get actual cases for verbs, and synonyms
        for verb in verbs:
            if verb not in Dictionary.verb_dictionary:
                Dictionary.verb_dictionary[verb] = [(verb, "NOM")]
        self.situation_grammar = SituationGrammar()
        self.situations, self.situation_names  = self.create_situations(verbs)

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
        self.world_state.create_object("kallis", 0)
        self.world_state.create_object("niin paljon", 4)
        self.world_state.create_object(self.embeddings.main_object, 4)
        self.world_state.create_object(self.embeddings.pre_object, 4)

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

    def create_situations(self, verbs):
        """
        A list of things that have to be handled within the story. World state (including characters) must be introduced,
        and plot must be furthered
        Todo: not all introductions must be done before any plot points are handled
        """
        situations = []
        main_char = self.world_state.characters[0]
        other_char = self.world_state.characters[1]
        third_char = self.world_state.characters[2]
        chars = [main_char, other_char]

        main_project = Project(self.world_state.subjects[1], verbs[1], ("obj", self.world_state.objects[1]), "statement", "prees", 1)

        # Maija has a contradicting belief about museums that necessitates lying to convince her
        counter_project = Project(self.world_state.subjects[2], verbs[2], ("obj", self.world_state.objects[2]), "argument", "prees", 1)

        pre_project = Project(self.world_state.subjects[0], verbs[0], ("static", self.world_state.objects[0]), "statement", "prees", 1)

        main_char.add_belief(main_project)
        #main_char.add_belief(pre_project)
        third_char.add_belief(counter_project)

        a_project = None
        b_project = None

        prev_project = main_project

        projects = {
            "none": (lambda x: None, []),
            "main_project": (lambda x, y: x, [main_project]),
            "prev_project": (lambda x: prev_project, []),
            "boredom_project": (Project.get_boredom_project, [[main_char, other_char], pre_project, other_char]),
            "dismissal_project": (Project.get_dismissal_project, [other_char]),
            "look_up_to_project": (Project.get_look_up_to_project, [main_char]),
            "complain_project": (Project.get_complain_project, [other_char, prev_project, main_project]),
            "reward_project": (Project.get_reward_project, [main_char]),
            "refer_back_project": (Project.get_refer_back_project, [prev_project, main_project]),
            "indoctrination_project": (Project.get_indoctrination_project, [main_project]),
            "pre_project": (lambda x, y: x, [pre_project])
        }

        sit = self.situation_grammar.get_next_situation(other_char, None)
        situation_names = []

        while sit is not None:

            if sit == "lie_for":
                chars = [other_char, third_char]
            else:
                chars = [main_char, other_char]

            #todo: collect situations into scenes
            #reset moods
            if sit in ["lecture", "lie_for", "are_rewarded_by"]:
                for char in chars:
                    char.reset_mood()

            # todo: other emotional effects for other situations?
            if sit == "are_bored_by":
                other_char.mood.affect_mood(Emotion(None, -2, -2, -2))

            for entry in self.situation_rules[sit]["a_project"]:
                project = projects[entry][0]
                parameters = projects[entry][1]
                a_project = project(*parameters, chars[1])
                if a_project is not None:
                    chars[0].set_goal(a_project, True)
                    prev_project = a_project

            for entry in self.situation_rules[sit]["b_project"]:
                project = projects[entry][0]
                parameters = projects[entry][1]
                b_project = project(*parameters, chars[0])
                if b_project is not None:
                    chars[1].set_goal(b_project, True)
                    prev_project = b_project


            #todo: set memories?

            situations.append(Situation(sit, self.world_state, chars, self.situation_rules[sit], main_char.attributes["location"]))

            situation_names.append(sit)

            # sometimes next situation depends on main char's mood, sometimes on other character's
            if sit in ["complain"]:
                sit = self.situation_grammar.get_next_situation(main_char, sit)
            else:
                sit = self.situation_grammar.get_next_situation(other_char, sit)

        return situations, situation_names

    def to_json(self):
        return str(self)

    def get_situations(self):
        return self.situations


def main():
    s = Story()
    print(s)


if __name__ == "__main__":
    main()
