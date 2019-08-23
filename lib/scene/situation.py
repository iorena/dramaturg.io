from sequence.sequence import Sequence
from language.action_types import ActionType
from concepts.project import Project
from concepts.character import Character
from language.dictionary import pivot_dictionary

from loaders import load_emotions, load_action_types, load_pad_values

EMOTIONS = load_emotions()
PAD_VALUES = load_pad_values()

import random, copy
from numpy import array
from numpy.linalg import norm

ROOT_SEQUENCE_TYPES = {"personal": ["SKÄS", "STIP", "STIPC", "STOP", "STOE", "SVÄI", "SKAN"],
        "impersonal": ["STIP", "STIPC", "STOE","SVÄI", "SKAN"]}
SEQUENCE_TYPES = {"personal": {"in": ["STOE", "STOP", "SKÄS"], "out": ["SVÄI"], "meta": ["SEST", "STIPC", "STII"]},
        "impersonal": {"in": ["STOP"], "out": ["SVÄI"], "meta": ["SEST", "STIPC", "STII"]}}


class Situation:
    def __init__(self, world_state, element_type, speakers, main_project, location):
        self.world_state = world_state
        self.element_type = element_type
        self.speakers = speakers
        self.main_project = main_project
        self.location = location
        self.action_types = load_action_types()
        self.mood_change = {}
        if type(self.main_project.subj) is Character:
            self.affect_emotions()
        self.sequences = self.create_sequences()
        if self.element_type == "out":
            self.add_topic_pivot()

    def affect_emotions(self):
        """
        When an event happens to a character, characters react emotionally to it
        """
        for character in self.speakers:
            relationship = character.relations[self.main_project.subj.name].liking["outgoing"] > 0.5
            event_appraisal = self.main_project.get_appraisal(character).id > 92
            if self.main_project.get_appraisal(character).id is 92:
                #neutral event, nothing happens
                return
            is_self = character is self.main_project.subj
            emotion = EMOTIONS[self.get_emotion(is_self, relationship, event_appraisal)]
            old_mood = copy.copy(character.mood)
            character.mood.affect_mood(emotion)
            new_mood = copy.copy(character.mood)
            change = None
            if old_mood.get_character_description("pleasure") != new_mood.get_character_description("pleasure"):
                if old_mood.pleasure < new_mood.pleasure:
                    change = "ilahtuu"
                else:
                    change = "suuttuu"
            if old_mood.get_character_description("arousal") != new_mood.get_character_description("arousal"):
                if old_mood.arousal < new_mood.arousal:
                    change = "ilahtuu"
                else:
                    change = "suuttuu"
            if old_mood.get_character_description("dominance") != new_mood.get_character_description("dominance"):
                if old_mood.dominance < new_mood.dominance:
                    change = "ilahtuu"
                else:
                    change = "suuttuu"
            if change is not None:
                self.mood_change[character.name] = change

    def get_emotion(self, is_self, relationship, event):
        if is_self and event:
            return "joy"
        if is_self and not event:
            return "distress"
        if relationship and event:
            return "happy_for"
        if relationship and not event:
            return "pity"
        if not relationship and event:
            return "resentment"
        if not relationship and not event:
            return "gloating"

    def create_sequences(self):
        """
        Generates sequences for each project
        """
        mood = self.speakers[0].mood
        personal = "personal" if self.main_project.subj is Character else "impersonal"
        distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), SEQUENCE_TYPES[personal][self.element_type]))
        main_sequence_type = random.choices(SEQUENCE_TYPES[personal][self.element_type], distances)[0]
        main_sequence = Sequence(self.speakers, self.main_project, main_sequence_type, self.action_types, self.world_state)
        sequences = self.add_sequences(main_sequence)
        return sequences

    def add_sequences(self, sequence):
        """
        Takes a sequence and returns a list including that sequence and possible additions
        """
        sequences = [sequence]
        #pre-project
        #speaker is chosen from characters weighted by dominance
        dominances = list(map(lambda x: x.mood.dominance, self.speakers))
        character = random.choices(self.speakers, dominances)[0]

        if random.uniform(-0.5, 1.5) < character.mood.arousal:
            speakers = self.speakers
            speakers.remove(character)
            speakers.insert(0, character)

            pre_project = Project.get_new_project(speakers, self.main_project, self.world_state)

            mood = speakers[0].mood
            personal = "personal" if self.main_project.subj is Character else "impersonal"
            distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), ROOT_SEQUENCE_TYPES[personal]))
            seq_type = random.choices(ROOT_SEQUENCE_TYPES[personal], distances)[0]
            sequences = self.add_sequences(Sequence(speakers, pre_project, seq_type, self.action_types, self.world_state, sequence.first_pair_part)) + sequences

        #post-project
        character = random.choices(self.speakers, dominances)[0]
        if random.uniform(-0.5, 1.5) < character.mood.arousal:
            speakers = self.speakers
            speakers.remove(character)
            speakers.insert(0, character)

            #attribute expansion of main topic
            subj = sequence.project.obj
            attributes = list(sequence.project.obj.attributes.items())
            if len(attributes) is 0:
                #don't stack "hyvä on mainio" - type chains
                if sequence.project.obj_type in ["quality", "appraisal", "affect"]:
                    return sequences
                if subj.id < 90:
                    obj = ("quality", self.speakers[0].perception.objects[subj.id])
                elif subj.id < 95:
                    obj = ("quality", self.speakers[0].perception.appraisals[subj.id - 90])
                else:
                    obj = ("quality", self.speakers[0].perception.weather_types[subj.id - 95])

            else:
                obj = random.choices(attributes)[0]

            post_project = Project(subj, "olla", obj, self.main_project.time, 1)
            mood = speakers[0].mood
            personal = "personal" if self.main_project.subj is Character else "impersonal"
            distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), ROOT_SEQUENCE_TYPES[personal]))
            seq_type = random.choices(ROOT_SEQUENCE_TYPES[personal], distances)[0]

            sequences = sequences + self.add_sequences(Sequence(speakers, post_project, seq_type, self.action_types, self.world_state, sequence.second_pair_part))
        return sequences

    def add_topic_pivot(self):
        pre_exp_exists = self.sequences[0].pre_expansion is not None
        first_turn = self.sequences[0].pre_expansion.inflected if pre_exp_exists else self.sequences[0].first_pair_part.inflected
        if random.random() > 0.5:
        #type A: topic proposition
            pivoted = random.choices(pivot_dictionary)[0] + first_turn
            if pre_exp_exists:
                self.sequences[0].pre_expansion.inflected = pivoted
            else:
                self.sequences[0].first_pair_part.inflected = pivoted
        #else:
        #type B: stepwise transition


    def to_json(self):
        return self.sequences
