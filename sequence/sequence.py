import random

from sequence.sequencegrammar import sequence_dict
from sequence.turn import Turn
from concepts.project import Project

import copy

PAIR_TYPES_POSITIVE = {
        "SKÄS": ("KÄS", "TOTN"),
        "STIP": ("TIP", "TIA+"),
        "STOP": ("TOP", "TOTN")
        }
PAIR_TYPES_NEGATIVE = {
        "SKÄS": ("KÄS", "TOTS"),
        "STIP": ("TIP", "TIA-"),
        "STOP": ("TOP", "TOTS")
        }


class Sequence:
    def __init__(self, speakers, project, seq_type, action_types):
        self.speakers = speakers
        self.project = project
        self.seq_type = seq_type
        self.action_types = action_types
        self.pair_types = PAIR_TYPES_POSITIVE if project.valence else PAIR_TYPES_NEGATIVE
        reverse = False
        if seq_type in ["SKÄS", "STOE"] and self.speakers[0].name == self.project.subj and project.verb != "olla":
            print(project.verb)
            reverse = True
        self.first_pair_part = self.generate_pair_part(self.speakers[0], action_types[self.pair_types[self.seq_type][0]], reverse)
        self.second_pair_part = self.generate_pair_part(self.speakers[1], action_types[self.pair_types[self.seq_type][1]], reverse)
        self.pre_expansion = self.generate_expansion()
        self.infix_expansion = self.generate_expansion(True)
        self.post_expansion = self.generate_expansion()

    def generate_expansion(self, switch_speakers=False):
        expansion = None
        if random.random() > 0.8:
            new_project = self.project
            new_seq_type = random.choices(list(self.pair_types.keys()))[0]
            #if random.random() > 0.7:
            #    new_project = self.generate_new_project()
            speakers = self.speakers
            if switch_speakers:
                speakers = [speakers[1], speakers[0]]
            expansion = Sequence(speakers, new_project, new_seq_type, self.action_types)
        return expansion

    def generate_pair_part(self, speaker, action_type, reverse):
        listeners = copy.copy(self.speakers)
        listeners.remove(speaker)
        return Turn(speaker, listeners, action_type, self.project, reverse)

    def print_sequence(self):
        print(self)

    def generate_new_project(self):
        """
        Todo: how to generate new projects? Are new attributes invented for characters etc. and added to the world state?
        """
        return Project(random.choices(self.speakers)[0].name)

    def __str__(self):
        ret = []
        if self.pre_expansion is not None:
            ret.append(str(self.pre_expansion))
        ret.append(str(self.first_pair_part))
        if self.infix_expansion is not None:
            ret.append(str(self.infix_expansion))
        ret.append(str(self.second_pair_part))
        if self.post_expansion is not None:
            ret.append(str(self.post_expansion))
        return "\n".join(ret)

def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
