from numpy import array


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
        return (Mood.get_default_pleasure(personality), Mood.get_default_arousal(personality), Mood.get_default_dominance(personality))

    #todo: check formula of degration towards default mood, does personality have an effect?
    def degrade_mood(self):
        self.pleasure = round((self.pleasure + self.default_pleasure) / 2, 2)
        self.arousal = round((self.arousal + self.default_arousal) / 2, 2)
        self.dominance = round((self.dominance + self.default_dominance) / 2, 2)

    #todo: add personality effect on how emotions affect mood
    def affect_mood(self, emotion):
        #print("affecting with", emotion.dominance)
        self.pleasure = self.pleasure + emotion.pleasure
        if self.pleasure > 1:
            self.pleasure = 1
        if self.pleasure < -1:
            self.pleasure = -1
        self.arousal = self.arousal + emotion.arousal
        if self.arousal > 1:
            self.arousal = 1
        if self.arousal < -1:
            self.arousal = -1
        self.dominance = self.dominance + emotion.dominance
        if self.dominance > 1:
            self.dominance = 1
        if self.dominance < -1:
            self.dominance = -1

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

    def get_character_description(self, dimension):
        if dimension == "pleasure":
            if self.pleasure > 0.2:
                return "hyväntuulinen"
            elif self.pleasure < -0.2:
                return "pahantuulinen"
            return None
        if dimension == "arousal":
            if self.arousal > 0.2:
                return "vireä"
            elif self.arousal < -0.2:
                return "vetelä"
            return None
        if dimension == "dominance":
            if self.dominance > 0.2:
                return "hallitseva"
            elif self.dominance < -0.2:
                return "alistuva"
            return None

    def as_array(self):
        return array((self.pleasure, self.arousal, self.dominance))

    def in_bounds(self, bounds):
        lower_bound = bounds[0]
        upper_bound = bounds[1]
        if self.pleasure < lower_bound[0] or self.pleasure > upper_bound[0]:
            return False
        if self.arousal < lower_bound[1] or self.arousal > upper_bound[1]:
            return False
        if self.dominance < lower_bound[2] or self.dominance > upper_bound[2]:
            return False

        return True

    def get_default_pleasure(personality):
        return 0.21 * personality["E"] + 0.59 * personality["A"] + 0.19 * personality["N"]

    def get_default_arousal(personality):
        return 0.15 * personality["O"] + 0.3 * personality["A"] - 0.57 * personality["N"]

    def get_default_dominance(personality):
        return 0.25 * personality["O"] + 0.17 * personality["C"] + 0.6 * personality["E"] - 0.32 * personality["A"]


