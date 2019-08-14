from sequence.sequence import Sequence
from language.action_types import ActionType
from concepts.project import Project
from concepts.character import Character

from loaders import load_emotions, load_action_types, load_pad_values

EMOTIONS = load_emotions()
PAD_VALUES = load_pad_values()

import random
from numpy import array
from numpy.linalg import norm

ROOT_SEQUENCE_TYPES = ["SKÄS", "STIP", "STIPC", "STOP", "STOE", "SVÄI", "SKAN"]
SEQUENCE_TYPES = {"present": {"G": ["STOE"], "O": ["SVVÄI"], "A": ["SKÄS", "STIP", "STOP"], "P": ["SKAN", "SVÄI"], "IE": ["SKAN"]},
        "past": {"G": ["STOE"], "A": ["STIP", "STIPB"], "P": ["SKAN", "SVÄI"], "IE": ["SKAN"]}}


class Situation:
    def __init__(self, world_state, element_type, speakers, main_project, location):
        self.world_state = world_state
        self.element_type = element_type
        self.speakers = speakers
        self.main_project = main_project
        self.location = location
        self.action_types = load_action_types()
        if element_type == "P" and type(self.main_project.subj) is Character:
            self.affect_emotions()
        self.sequences = self.create_sequences()

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
            character.mood.affect_mood(emotion)

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
        distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), SEQUENCE_TYPES[self.main_project.time][self.element_type]))
        main_sequence_type = random.choices(SEQUENCE_TYPES[self.main_project.time][self.element_type], distances)[0]
        main_sequence = Sequence(self.speakers, self.main_project, main_sequence_type, self.action_types, self.world_state)
        sequences = self.add_sequences(main_sequence)
        hello_sequence = self.create_hello_sequence()
        return [hello_sequence] + sequences

    def create_hello_sequence(self):
        return Sequence(self.speakers, Project(self.speakers[0], ("greeting", self.speakers[0]), "statement", "present", True), "STER", self.action_types, self.world_state, None)

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
            distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), ROOT_SEQUENCE_TYPES))
            seq_type = random.choices(ROOT_SEQUENCE_TYPES, distances)[0]
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
            distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), ROOT_SEQUENCE_TYPES))
            seq_type = random.choices(ROOT_SEQUENCE_TYPES, distances)[0]

            sequences = sequences + self.add_sequences(Sequence(speakers, post_project, seq_type, self.action_types, self.world_state, sequence.second_pair_part))
        return sequences

    def to_json(self):
        return self.sequences
