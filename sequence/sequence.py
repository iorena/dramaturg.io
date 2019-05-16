from nltk.parse.generate import generate
from nltk import CFG

import random

from sequence.sequencegrammar import action_grammar, perception_grammar
from sequence.adjacency_pair.adjacency_pair import AdjacencyPair


class Sequence:
    def __init__(self, speakers, fabula_element):
        self.fabula_element = fabula_element
        if self.fabula_element.elem is "A":
            self.grammar = CFG.fromstring(action_grammar)
        else:
            self.grammar = CFG.fromstring(perception_grammar)
        self.speakers = speakers
        self.adjacency_pairs = []
        self.topic = self.getTopic()
        self.generate()

    def generate(self):
        generated = []
        for pair in generate(self.grammar, depth=5):
            generated.append(pair)
        adjpairs = random.choices(generated)[0]
        for pair in adjpairs:
            l = "".join(pair)
            adj_pair = AdjacencyPair(self.speakers, pair, self.topic)
            self.adjacency_pairs.append(adj_pair)

    def print_sequence(self):
        print(self)

    def getTopic(self):
        """
        Topic is a tuple of verb and world element
        Todo: make dictionaries of verbs related to different transitions
        """
        return "siirtyä", list(self.fabula_element.transition.values())[0].keywords["type"]

    def __str__(self):
        ret = []
        for pair in self.adjacency_pairs:
            for pair_part in pair.inflected:
                speaker = pair_part[0]
                words = ' '.join(map(lambda x: speaker.style.getStyledExpression(x), pair_part[1]))
                line = f"{speaker.name}: {words}"
                ret.append(line)
        return "\n".join(ret)


def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
