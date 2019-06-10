

class Mood:
    def __init__(self, personality):
        self.default_pleasure, self.default_arousal, self.default_dominance = self.default_mood(personality)
        self.pleasure = self.default_pleasure
        self.arousal = self.default_arousal
        self.dominance = self.default_dominance

    def __str__(self):
        return f"{self.pleasure:.2f}P {self.arousal:.2f}A {self.dominance:.2f}D {self.get_octant_name()}"

    #formulas from Gebhard (2005)
    def default_mood(self, personality):
        return (0.21 * personality["E"] + 0.59 * personality["A"] + 0.19 * personality["N"],
                0.15 * personality["O"] + 0.3 * personality["A"] - 0.57 * personality["N"],
                0.25 * personality["O"] + 0.17 * personality["C"] + 0.6 * personality["E"] - 0.32 * personality["A"])

    #todo: check formula of degration towards default mood, does personality have an effect?
    def degrade_mood(self):
        self.pleasure = round((self.pleasure + self.default_pleasure) / 2, 2)
        self.arousal = round((self.arousal + self.default_arousal) / 2, 2)
        self.dominance = round((self.dominance + self.default_dominance) / 2, 2)

    #todo: add personality effect on how emotions affect mood
    def affect_mood(self, emotion):
        first = self.pleasure
        self.pleasure = self.pleasure + emotion.pleasure
        if self.pleasure > 1:
            self.pleasure = 1
        self.arousal = self.arousal + emotion.arousal
        if self.arousal > 1:
            self.arousal = 1
        self.dominance = self.dominance + emotion.dominance
        if self.dominance > 1:
            self.dominance = 1
        print(first, self.pleasure)

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
