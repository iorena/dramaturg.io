

class Mood:
    def __init__(self, personality):
        self.default_pleasure, self.default_arousal, self.default_dominance = self.default_mood(personality)
        self.pleasure = self.default_pleasure
        self.arousal = self.default_arousal
        self.dominance = self.default_dominance

    #formulas from Gebhard (2005)
    def default_mood(self, personality):
        return (0.21 * personality["E"] + 0.59 * personality["A"] + 0.19 * personality["N"],
                0.15 * personality["O"] + 0.3 * personality["A"] + 0.57 * personality["N"],
                0.25 * personality["O"] + 0.17 * personality["C"] + 0.6 * personality["E"] + 0.32 * personality["A"])

    #todo: check formula of degration towards default mood, does personality have an effect?
    def degrade_mood(self):
        self.pleasure = (self.pleasure + self.default_pleasure) / 2
        self.arousal = (self.arousal + self.default_arousal) / 2
        self.dominance = (self.dominance + self.default_dominance) / 2

    #todo: add personality effect on how emotions affect mood
    def affect_mood(self, emotion):
        self.pleasure = self.pleasure + emotion.pleasure
        self.arousal = self.arousal + emotion.arousal
        self.dominance = self.dominance + emotion.dominance

    def get_octant_name(self):
        if self.pleasure > 0:
            if self.arousal > 0:
                if self.dominance > 0:
                    return "exuberant"
                return "dependent"
            if self.dominance > 0:
                return "relaxed"
            return "docile"
        if self.arousal > 0:
            if self.dominance > 0:
                return "hostile"
            return "anxious"
        if self.dominance > 0:
            return "disdainful"
        return "bored"
