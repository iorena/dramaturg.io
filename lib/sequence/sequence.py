from loaders import load_expansion_types
from loaders import load_sequence_types
from sequence.turn import Turn
from concepts.project import Project

import random
import copy

POS_SEQUENCES, NEG_SEQUENCES = load_sequence_types()

EXPANSIONS = load_expansion_types()


class Sequence():
    def __init__(self, speakers, project, seq_type, action_types, parent=None):
        self.speakers = speakers
        self.project = project
        self.seq_type = seq_type
        self.action_types = action_types
        self.parent = parent
        self.pair_types = POS_SEQUENCES if project.valence else NEG_SEQUENCES
        reverse = False
        if seq_type in ["SKÄS"] and self.speakers[0].name == self.project.subj and project.verb != "olla":
            reverse = True
        elif seq_type in ["SKÄS"] and self.speakers[0].name == self.project.subj:
            self.seq_type = "SKAN"
        action_names = random.choices(self.pair_types[self.seq_type])[0]
        self.first_pair_part = self.generate_pair_part(self.speakers[0], action_names[0], reverse)
        if action_names[1] is None:
            self.second_pair_part = None
        else:
            self.second_pair_part = self.generate_pair_part(self.speakers[1], action_names[1], reverse)
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
            # todo: implement more sequence types
            if new_seq_type in ["", "SJTK", "SJPM"]:
                return None
            if new_seq_type == "SKORB":
                # new project with old object as subject? check if there is an object to take?
                if self.project.obj:
                    target = self.project.obj
                    # todo: how to handle emotions? asking "mikä surullinen?" doesn't really make sense, does it?
                    attributes = list(target.attributes.items())
                    if len(attributes) is 0:
                        attribute = ("attribute", None)
                    else:
                        attribute = random.choices(attributes)[0]

                    new_project = Project(target, attribute, "statement", "present", True)

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
        if self.second_pair_part:
            ret.append(str(self.second_pair_part))
        if self.post_expansion is not None:
            ret.append(str(self.post_expansion))
        return "\n".join(ret)

    def to_json(self):
        ret = []
        # if self.pre_expansion is not None:
        #     ret.append(str(self.pre_expansion))
        # ret.append(str(self.first_pair_part))
        # if self.infix_expansion is not None:
        #     ret.append(str(self.infix_expansion))
        # if self.second_pair_part:
        #     ret.append(str(self.second_pair_part))
        # if self.post_expansion is not None:
        #     ret.append(str(self.post_expansion))
        # return ret
        return {
            "speakers": self.speakers,
            # "project": self.project,
            "seq_type": self.seq_type,
            # "action_types": self.action_types,
            # "parent": str(self.parent),
            # "pair_types": self.pair_types,
            "first_pair_part": self.first_pair_part,
            "second_pair_part": self.second_pair_part,
            "pre_expansion": self.pre_expansion,
            "infix_expansion": self.infix_expansion,
            "post_expansion": self.post_expansion
        }


def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
