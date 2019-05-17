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
        self.topic = self.get_main_topic()
        self.generated = self.generate_empty_pairs()
        self.adjacency_pair_topics = self.generate_adjacency_pair_topics()
        self.generate_adjacency_pairs()

    def generate_empty_pairs(self):
        generated = []
        for pair in generate(self.grammar, depth=5):
            generated.append(pair)
        return generated

    def generate_adjacency_pairs(self):
        adjpairs = random.choices(self.generated)[0]
        for i in range(len(adjpairs)):
            adj_pair = AdjacencyPair(self.speakers, adjpairs[i], self.adjacency_pair_topics[i])
            self.adjacency_pairs.append(adj_pair)

    def print_sequence(self):
        print(self)

    def get_main_topic(self):
        """
        Topic is a tuple of verb and world element
        Todo: make dictionaries of verbs related to different transitions
        """
        return {"verb": "siirtyä", "obj": list(self.fabula_element.transition.values())[0].keywords["type"], "subj": self.fabula_element.subj.name}

    def generate_adjacency_pair_topics(self):
        topics = []
        for adj_pair in self.generated:
            topics.append(None)
        i = random.randint(0, len(topics) - 1)
        topics[i] = self.topic
        for i in range(len(topics)):
            if topics[i] is None:
                topics[i] = {"verb": None, "subj": random.choices(self.speakers)[0].name, "obj": None}
        return topics

    def __str__(self):
        ret = ""
        for pair in self.adjacency_pairs:
            for pair_part in pair.inflected:
                speaker = pair_part[0]
                line = f"{speaker.name}: "
                line += pair_part[1]
                line += "\n"
                ret += line
        return ret


def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
