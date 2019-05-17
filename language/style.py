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

    def getStyledExpression(self, sentence):
        styledSentence = []
        for word in sentence:
            styledSentence.append(self.getStyledWord(word))
        return " ".join(styledSentence)


    def getStyledWord(self, word):
        if word == "minä" or word == "sinä":
            if random.random() < self.coll:
                return word[0] + word[3]
            if random.random() < self.brev:
                return ""
        return word
