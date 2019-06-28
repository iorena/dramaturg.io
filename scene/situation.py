from sequence.sequence import Sequence
from language.action_types import ActionType
from concepts.project import Project

import random

ROOT_SEQUENCE_TYPES = ["SKÄS", "STIP", "STOP", "STOE", "SVÄI", "SKAN"]
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
        self.sequences = self.create_sequences()

    def create_sequences(self):
        """
        Generates sequences for each project
        """
        main_sequence_type = random.choices(SEQUENCE_TYPES[self.main_project.time][self.element_type])[0]
        main_sequence = Sequence(self.speakers, self.main_project, main_sequence_type, self.action_types)
        sequences = self.add_sequences(main_sequence)
        return sequences

    def add_sequences(self, sequence):
        """
        Takes a sequence and returns a list including that sequence and possible additions
        """
        sequences = [sequence]
        #pre-project
        if random.random() > 0.8:
            #random topic: weather etc
            subj = self.world_state.weather
            obj = ("quality", random.choices(self.world_state.appraisals)[0])
            pre_project = Project(subj, obj, self.main_project.time, True)

            seq_type = random.choices(ROOT_SEQUENCE_TYPES)[0]
            sequences = self.add_sequences(Sequence(self.speakers, pre_project, seq_type, self.action_types)) + sequences

        #post-project
        if random.random() > 0.8:
            #expansion of main topic
            subj = sequence.project.obj
            attributes = list(sequence.project.obj.attributes.items())
            if len(attributes) is 0:
                obj = ("quality", random.choices(self.world_state.appraisals)[0])
            else:
                obj = random.choices(attributes)[0]
            post_project = Project(subj, obj, self.main_project.time, True)

            seq_type = random.choices(ROOT_SEQUENCE_TYPES)[0]
            sequences = sequences + self.add_sequences(Sequence(self.speakers, post_project, seq_type, self.action_types))
        return sequences



