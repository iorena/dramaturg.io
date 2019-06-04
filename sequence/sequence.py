import random

from sequence.sequencegrammar import sequence_dict
from sequence.adjacency_pair.adjacency_pair import AdjacencyPair
from concepts.topic import Topic

PAIR_TYPES = ["kys", "ilm"]


class Sequence:
    def __init__(self, speakers, topic):
        self.speakers = speakers
        self.adjacency_pairs = []
        self.topic = topic
        pair_type = random.choices(PAIR_TYPES)[0]
        self.adjacency_pairs = self.generate_adjacency_pairs(self.topic, pair_type)

    def generate_adjacency_pairs(self, topic, pair_type):
        """
        Generate main adjacency pair and recursively add auxiliary pairs
        """
        generated = []
        generated.append(AdjacencyPair(self.speakers, pair_type, topic))
        #generate postfix pairs
        if random.random() > 0.5:
            new_topic = topic
            new_pair_type = random.choices(PAIR_TYPES)[0]
            #if random.random() > 0.7:
            #    new_topic = self.generate_new_topic()
            new_pairs = self.generate_adjacency_pairs(new_topic, new_pair_type)
            for pair in new_pairs:
                generated.append(pair)
        #generate infix pair(s)
        if random.random() > 0.5:
            generated_infix = [AdjacencyPair((self.speakers[1], self.speakers[0]), pair_type, topic)]
            generated[0].add_infix_pairs(generated_infix)
        return generated

    def print_sequence(self):
        print(self)

    def generate_new_topic(self):
        """
        Todo: how to generate new topics? Are new attributes invented for characters etc. and added to the world state?
        """
        return Topic(random.choices(self.speakers)[0].name)

    def __str__(self):
        ret = []
        for pair in self.adjacency_pairs:
            ret += self.get_pair_str(pair)
        return "".join(ret)

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
