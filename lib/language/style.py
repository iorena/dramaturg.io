import random


class Style:
    """
    Represent character's speaking style as probabilistic factors
    Colloquiality changes personal pronouns from "minä" to "mä"
    Brevity drops words (like personal pronouns) alltogether
    """
    def __init__(self, colloquiality, brevity, hesitation):
        self.coll = colloquiality
        self.brev = brevity
        self.hesi = hesitation
        self.hesitation_particle = self.get_hesitation_particle()

    def get_hesitation_particle(self):
        if self.coll > 0.5 and self.brev < 0.5:
            return "tota,"
        elif self.coll < 0.5:
            return "tuota,"
        else:
            return "öö,"

    def get_styled_expression(self, sentence):
        styled_sentence = []
        for word in sentence:
            styled = self.get_styled_word(word)
            if styled is not None:
                styled_sentence.append(styled)
        if random.random() + 0.6 < self.hesi:
            styled_sentence.insert(0, self.hesitation_particle)
        return " ".join(styled_sentence)


    def get_styled_word(self, word):
        if word == "minä" or word == "sinä":
            if self.coll > 0.5:
                return word[0] + word[3]
            if self.brev > 0.5:
                return None
        return word
