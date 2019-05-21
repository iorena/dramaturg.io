import random

from sequence.sequencegrammar import sequence_dict
from sequence.adjacency_pair.adjacency_pair import AdjacencyPair


class Sequence:
    def __init__(self, speakers, fabula_element):
        self.fabula_element = fabula_element
        self.speakers = speakers
        self.adjacency_pairs = []
        self.topic = self.get_main_topic()
        pair_type = random.choices(sequence_dict[self.fabula_element.elem])[0]
        self.adjacency_pairs = self.generate_adjacency_pairs(self.topic, pair_type)

    def generate_adjacency_pairs(self, topic, pair_type):
        """
        Generate main adjacency pair and recursively add auxiliary pairs
        """
        generated = []
        generated.append(AdjacencyPair(self.speakers, pair_type, topic))
        if random.random() > 0.5:
            new_topic = topic
            new_pair_type = random.choices(["kys", "ilm", "hav"])[0]
            if random.random() > 0.7:
                new_topic = self.generate_new_topic()
            new_pairs = self.generate_adjacency_pairs(new_topic, new_pair_type)
            for pair in new_pairs:
                generated.append(pair)
        return generated

    def print_sequence(self):
        print(self)

    def get_main_topic(self):
        """
        Topic is a tuple of verb and world element
        Todo: make dictionaries of verbs related to different transitions
        """
        return {"verb": "siirtyä", "obj": list(self.fabula_element.transition.values())[0].keywords["type"], "subj": self.fabula_element.subj.name}

    def generate_new_topic(self):
        return {"verb": None, "subj": random.choices(self.speakers)[0].name, "obj": None}

    def __str__(self):
        ret = []
        for pair in self.adjacency_pairs:
            for pair_part in pair.inflected:
                speaker = pair_part[0]
                line = f"{speaker.name}: "
                line += pair_part[1]
                line += "\n"
                ret += line
        return "".join(ret)

def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
