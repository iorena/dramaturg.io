from sequence.sequence import Sequence
from language.action_types import ActionType
from concepts.project import Project
from concepts.character import Character

from loaders.emotions_loader import load_emotions

EMOTIONS = load_emotions()

import random

ROOT_SEQUENCE_TYPES = ["STIPC"]#["SKÄS", "STIP", "STIPC", "STOP", "STOE", "SVÄI", "SKAN"]
SEQUENCE_TYPES = {"present": {"G": ["STOE"], "A": ["SKÄS", "STIP", "STOP"], "P": ["SKAN", "SVÄI"], "IE": ["SKAN"]},
        "past": {"G": ["STOE"], "A": ["STIP", "STIPB"], "P": ["SKAN", "SVÄI"], "IE": ["SKAN"]}}


class Situation:
    def __init__(self, world_state, element_type, speakers, main_project, location):
        self.world_state = world_state
        self.element_type = element_type
        self.speakers = speakers
        self.main_project = main_project
        self.location = location
        self.action_types = ActionType.load_action_types()
        if element_type == "P" and type(self.main_project.subj) is Character:
            self.affect_emotions()
        self.sequences = self.create_sequences()

    def affect_emotions(self):
        for character in self.speakers:
            relationship = character.relations[self.main_project.subj.name].liking["outgoing"] > 0.5
            event_appraisal = self.main_project.appraisal.id > 91
            if self.main_project.appraisal.id is 91:
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
        main_sequence_type = random.choices(SEQUENCE_TYPES[self.main_project.time][self.element_type])[0]
        main_sequence = Sequence(self.speakers, self.main_project, main_sequence_type, self.action_types, self.world_state)
        sequences = self.add_sequences(main_sequence)
        return sequences

    def add_sequences(self, sequence):
        """
        Takes a sequence and returns a list including that sequence and possible additions
        """
        sequences = [sequence]
        #pre-project
        if random.random() > 0.8:
            pre_project = Project.get_new_project(self.speakers, self.main_project, self.world_state)

            seq_type = random.choices(ROOT_SEQUENCE_TYPES)[0]
            sequences = self.add_sequences(Sequence(self.speakers, pre_project, seq_type, self.action_types, self.world_state, sequence.first_pair_part)) + sequences

        #post-project
        if random.random() > 0.8:
            #attribute expansion of main topic
            subj = sequence.project.obj
            attributes = list(sequence.project.obj.attributes.items())
            if len(attributes) is 0:
                #don't stack "hyvä on mainio" - type chains
                if sequence.project.obj_type in ["quality", "appraisal", "affect"]:
                    return sequences
                obj = ("quality", self.speakers[0].perception.objects[subj.id])
            else:
                obj = random.choices(attributes)[0]

            post_project = Project(subj, obj, "statement", self.main_project.time, True)
            seq_type = random.choices(ROOT_SEQUENCE_TYPES)[0]


            sequences = sequences + self.add_sequences(Sequence(self.speakers, post_project, seq_type, self.action_types, self.world_state, sequence.second_pair_part))
        return sequences

    def to_json(self):
        return self.sequences
