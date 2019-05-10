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

    def getStyledExpression(self, word):
        if word.wc == "ppron":
            if random.random() < self.coll:
                return word.word[0] + word.word[3]
            if random.random() < self.brev:
                return ""
        return word.word
