import random


class Style:
    """
    Represent character's speaking style as probabilistic factors
    Colloquiality changes personal pronouns from "minä" to "mä"
    Brevity drops words (like personal pronouns) altogether
    """
    def __init__(self, colloquiality, brevity, hesitation):
        self.coll = colloquiality
        self.brev = brevity
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
        return " ".join(styled_sentence)

    def get_styled_word(self, word):
        if word == "minä" or word == "sinä":
            if self.coll > 0.5:
                return word[0] + word[3]
            if self.brev > 0.5:
                return None
        if word == "minulle" or word == "sinulle":
            if self.coll > 0.5:
                return word[0] + "ulle"
        return word

    def get_hesitant_expression(self, sentence):
        edited_sentence = [self.hesitation_particle]
        prev_dropped = False
        for word in sentence.split(" "):
            #todo: tavutus??
            if not prev_dropped and random.random() > 0.2:
                edited_sentence.append("...")
                prev_dropped = True
            else:
                edited_sentence.append(word)
                prev_dropped = False
        return " ".join(edited_sentence)
