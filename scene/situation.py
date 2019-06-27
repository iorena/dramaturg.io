from sequence.sequence import Sequence
from language.action_types import ActionType

import random

ROOT_SEQUENCE_TYPES = ["SKÄS", "STIP", "STOP", "STOE", "SVÄI", "SKAN"]
SEQUENCE_TYPES = {"present": {"G": ["STOE"], "A": ["SKÄS", "STIP", "STOP"], "P": ["SKAN", "SVÄI"], "IE": ["SKAN"]},
        "past": {"G": ["STOE"], "A": ["STIP", "STIPB"], "P": ["SKAN", "SVÄI"], "IE": ["SKAN"]}}


class Situation:
    def __init__(self, element_type, speakers, main_project, location):
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
        sequences = [main_sequence]
        #for project in self.projects:
        #    seq_type = random.choices(ROOT_SEQUENCE_TYPES)[0]
        #    sequences.append(Sequence(self.speakers, project, seq_type, self.action_types))
        return sequences
