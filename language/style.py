import random


class Style:
    """
    Represent character's speaking style as probabilistic factors
    Colloquiality changes personal pronouns from "minä" to "mä"
    Brevity drops words (like personal pronouns) alltogether
    """
    def __init__(self, colloquiality, brevity):
        self.coll = colloquiality
        self.brev = brevity

    def get_styled_expression(self, sentence):
        styled_sentence = []
        for word in sentence:
            styled_sentence.append(self.get_styled_word(word))
        return " ".join(styled_sentence)


    def get_styled_word(self, word):
        if word == "minä" or word == "sinä":
            if random.random() < self.coll:
                return word[0] + word[3]
            if random.random() < self.brev:
                return ""
        return word
