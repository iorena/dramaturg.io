from language.word_token import WordToken
from language.sentence import Sentence

import random

class AdjacencyPair:
    def __init__(self, speakers, name, topic):
        self.speakers = speakers
        self.name = name
        self.verb = topic.verb
        self.subj = topic.subj
        self.obj = topic.obj
        self.obj_type = topic.obj_type
        self.time = topic.time
        self.sentences = {
            "ter": ("ter", "ter"),
            "kys": ("kys", "vas"),
            "ilm": ("ilm", "kui")
        }
        self.word_tokens = {
            "ter": [WordToken("tpart")],
            "kys": [WordToken("ppron", "subj", self.subj), WordToken("verb", None, self.verb), WordToken("noun", None, self.obj)],
            "vas": [WordToken("vpart")],
            "ilm": [WordToken("ppron", "subj", self.subj), WordToken("verb", None, self.verb), WordToken("noun", None, self.obj)],
            "kui": [WordToken("kpart")]
        }
        self.first_pair_part = self.get_first_part(name)
        self.second_pair_part = self.get_second_part(name)
        self.skeleton = (self.first_pair_part, self.second_pair_part)
        self.inflected = (self.inflect(0), self.inflect(1))
        self.infix_pairs = []

    def __str__(self):
        return f"{self.sentences[self.name][0]} - {self.sentences[self.name][1]}"

    def get_first_part(self, name):
        return self.speakers[0], self.word_tokens[self.sentences[name][0]]

    def get_second_part(self, name):
        return self.speakers[1], self.word_tokens[self.sentences[name][1]]

    def add_infix_pairs(self, pairs):
        self.infix_pairs = pairs

    def inflect(self, part):
        sentence_type = self.sentences[self.name][part]
        tokens = self.word_tokens[sentence_type]
        ques = sentence_type is "kys"
        aux = False
        if random.random() > 0.5:
            aux = True
        if sentence_type in ["ter", "vas", "kui"]:
            #todo: change to accept cases with more than one token
            return (self.speakers[part], tokens[0].word)
        sentence = Sentence(self.speakers[part], [self.speakers[part+1]], {"subj": tokens[0], "verb": tokens[1], "obj": tokens[2]}, ques, aux, self.obj_type, self.time)
        return (self.speakers[part], sentence.styled)


def main():
    print("Generated adjacency pair")


if __name__ == "__main__":
    main()
