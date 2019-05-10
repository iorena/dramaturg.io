import random


class Style:
    def __init__(self, colloquiality, brevity):
        self.coll = colloquiality
        self.brev = brevity

    def getStyledExpression(self, word):
        if word.wc == "ppron":
            if random.random() < self.coll:
                return word.word[0] + word.word[3]
            if random.random() < self.brev:
                return ""
        return word.word

