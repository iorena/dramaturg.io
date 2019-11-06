from loaders import load_expansion_types, load_sequence_types, load_pad_values
from sequence.turn import Turn
from concepts.project import Project

import random
import copy

from numpy import array
from numpy.linalg import norm

POS_SEQUENCES, NEG_SEQUENCES = load_sequence_types()

EXPANSIONS = load_expansion_types()
PAD_VALUES = load_pad_values()


class Sequence():
    def __init__(self, speakers, project, seq_type, action_types, world_state, parent=None):
        self.speakers = speakers
        self.project = project
        self.seq_type = seq_type
        self.action_types = action_types
        self.parent = parent
        self.world_state = world_state
        self.pair_types = POS_SEQUENCES if not self.project.get_surprise(self.speakers[1]) else NEG_SEQUENCES
        reverse = False
        if seq_type in ["SKÄS"] and self.speakers[0].name == self.project.subj.name and project.verb != "olla":
            reverse = True
        elif seq_type in ["SKÄS"] and self.speakers[0].name == self.project.subj.name:
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
        self.turns = []
        if self.pre_expansion is not None:
            for turn in self.pre_expansion.turns:
                self.turns.append(turn)
        self.turns.append(self.first_pair_part)
        if self.infix_expansion is not None:
            for turn in self.infix_expansion.turns:
                self.turns.append(turn)
        if self.second_pair_part is not None:
            self.turns.append(self.second_pair_part)
        if self.post_expansion is not None:
            for turn in self.post_expansion.turns:
                self.turns.append(turn)

    def generate_expansion(self, position, parent, switch_speakers=False):
        return None

        if self.second_pair_part is None:
            #return lisäkysymys: "onko kaikki hyvin", "soitinko huonoon aikaan?"
            return None
        speakers = self.speakers
        if switch_speakers:
            speakers = [speakers[1], speakers[0]]

        expansion = None
        rand = random.uniform(-0.5, 1.4)
        mood = speakers[0].mood.arousal
        if rand < mood:
            new_project = self.project
            if position not in EXPANSIONS[self.seq_type]:
                return None
            pool = EXPANSIONS[self.seq_type][position]
            if pool[0] == "":
                return None

            mood = speakers[0].mood
            distances = list(map(lambda x: norm(array((mood.pleasure, mood.arousal, mood.dominance)) - array((PAD_VALUES[x]))), pool))

            new_seq_type = random.choices(pool, distances)[0]
            if new_seq_type == "SKORB":
                # new project with old object as subject? check if there is an object to take?
                if self.project.obj:
                    target = self.project.obj
                    # todo: how to handle emotions? asking "mikä surullinen?" doesn't really make sense, does it?
                    attributes = list(target.attributes.items())
                    if len(attributes) is 0:
                        return None
                    else:
                        attribute = random.choices(attributes)[0]

                    new_project = Project(speakers[0], target, "olla", attribute, "present", 1)


            expansion = Sequence(speakers, new_project, new_seq_type, self.action_types, self.world_state, parent)
        return expansion

    def generate_pair_part(self, speaker, action_name, reverse):
        if action_name == "TOI":
            if self.parent is None:
                print(self.project.subj, self.project.verb, self.project.obj)
            action_type = self.action_types[self.parent.action_type.name]
        else:
            action_type = self.action_types[action_name]
        project = self.project
        if action_name == "SEL":
            project = Project.get_new_project(self.speakers, self.project, self.world_state)

        listeners = copy.copy(self.speakers)
        listeners.remove(speaker)
        return Turn(speaker, listeners, action_type, project, reverse)

    def print_sequence(self):
        print(self)

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
