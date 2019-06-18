from sequence.sequencegrammar import sequence_dict
from sequence.turn import Turn
from concepts.project import Project

import random
import copy
import csv

PAIR_TYPES_POSITIVE = {
        "SKÄS": ("KÄS", "TOTN"),
        "STIP": ("TIP", "TIA+"),
        "STOP": ("TOP", "TOTN"),
        "SKAN": ("KAN", "SAM-KAN"),
        "SKOR": ("KOA", "TOI"),
        "STOI": ("TOI", "TOTN")
        }
PAIR_TYPES_NEGATIVE = {
        "SKÄS": ("KÄS", "TOTS"),
        "STIP": ("TIP", "TIA-"),
        "STOP": ("TOP", "TOTS"),
        "SKAN": ("KAN", "ERI-KAN"),
        "SKOR": ("KOA", "TOI"),
        "STOI": ("TOI", "TOTS")
        }

EXPANSIONS = {}
with open("sequence/expansion_types.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="\t")
    for row in csv_reader:
        EXPANSIONS[row[0]] = {"pre_expansions": row[1].split(", "), "infix_expansions": row[2].split(", "), "post_expansions": row[3].split(", ")}


class Sequence:
    def __init__(self, speakers, project, seq_type, action_types, parent=None):
        self.speakers = speakers
        self.project = project
        self.seq_type = seq_type
        self.action_types = action_types
        self.parent = parent
        self.pair_types = PAIR_TYPES_POSITIVE if project.valence else PAIR_TYPES_NEGATIVE
        reverse = False
        if seq_type in ["SKÄS", "STOE"] and self.speakers[0].name == self.project.subj and project.verb != "olla":
            print(project.verb)
            reverse = True
        self.first_pair_part = self.generate_pair_part(self.speakers[0], self.pair_types[self.seq_type][0], reverse)
        self.second_pair_part = self.generate_pair_part(self.speakers[1], self.pair_types[self.seq_type][1], reverse)
        self.pre_expansion = self.generate_expansion("pre_expansions", None)
        self.infix_expansion = self.generate_expansion("infix_expansions", self.first_pair_part, True)
        self.post_expansion = self.generate_expansion("post_expansions", self.second_pair_part)

    def generate_expansion(self, position, parent, switch_speakers=False):
        expansion = None
        if random.random() > 0.8:
            new_project = self.project
            if position not in EXPANSIONS[self.seq_type]:
                return None
            pool = EXPANSIONS[self.seq_type][position]
            new_seq_type = random.choices(pool)[0]
            #todo: implement more sequence types
            if new_seq_type in ["", "SJSK", "SJTK", "SJPM"]:
                return None
            #if random.random() > 0.7:
            #    new_project = self.generate_new_project()
            speakers = self.speakers
            if switch_speakers:
                speakers = [speakers[1], speakers[0]]
            expansion = Sequence(speakers, new_project, new_seq_type, self.action_types, parent)
        return expansion

    def generate_pair_part(self, speaker, action_name, reverse):
        if action_name == "TOI":
            action_type = self.action_types[self.parent.action_type.name]
        else:
            action_type = self.action_types[action_name]
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
