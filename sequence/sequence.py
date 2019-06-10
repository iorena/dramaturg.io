import random

from sequence.sequencegrammar import sequence_dict
from sequence.turn import Turn
from concepts.project import Project

import copy

PAIR_TYPES = ["kys", "ilm"]


class Sequence:
    def __init__(self, speakers, project, pair_type):
        self.speakers = speakers
        self.project = project
        self.pair_type = pair_type
        self.sentences = {
            "ter": ("ter", "ter"),
            "kys": ("kys", "vas"),
            "ilm": ("ilm", "kui")
        }
        self.first_pair_part = self.generate_pair_part(self.speakers[0], self.sentences[self.pair_type][0])
        self.second_pair_part = self.generate_pair_part(self.speakers[1], self.sentences[self.pair_type][1])
        self.pre_expansion = self.generate_expansion()
        self.infix_expansion = self.generate_expansion()
        self.post_expansion = self.generate_expansion()

    def generate_expansion(self):
        """
        Generate main adjacency pair and recursively add auxiliary pairs
        """
        expansion = None
        if random.random() > 0.8:
            new_project = self.project
            new_pair_type = random.choices(PAIR_TYPES)[0]
            #if random.random() > 0.7:
            #    new_project = self.generate_new_project()
            expansion = Sequence(self.speakers, new_project, new_pair_type)
        return expansion

    def generate_pair_part(self, speaker, turn_type):
        listeners = copy.copy(self.speakers)
        listeners.remove(speaker)
        return Turn(speaker, listeners, turn_type, self.project)

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

    def get_pair_str(self, pair):
        ret = []
        first_pair_part = pair.inflected[0]

        line = f"{first_pair_part[0].name}: "
        line += first_pair_part[1]
        line += "\n"
        ret += line
        for infix_pair in pair.infix_pairs:
            ret += self.get_pair_str(infix_pair)
        second_pair_part = pair.inflected[1]
        line = f"{second_pair_part[0].name}: "
        line += second_pair_part[1]
        line += "\n"
        ret += line
        return "".join(ret)


def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
