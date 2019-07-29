from concepts.affect.mood import Mood

import random


class Relationship:
    def __init__(self, character, liking_in, liking_out,  dominance):
        self.character = character
        self.liking = {}
        self.liking["outgoing"] = liking_out
        #todo: belief can differ from reality
        self.liking["belief"] = liking_in
        #todo: formula?
        self.liking["desire"] = self.liking["outgoing"]
        self.dominance = {}
        self.dominance["outgoing"] = Mood.get_default_dominance(character.personality)
        self.dominance["belief"] = dominance
        self.dominance["desire"] = 1 - Mood.get_default_dominance(character.personality)
