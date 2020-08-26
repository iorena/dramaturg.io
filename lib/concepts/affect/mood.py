from numpy import array


class Mood:
    def __init__(self, personality):
        if type(personality) is dict:
            self.default_pleasure, self.default_arousal, self.default_dominance = self.default_mood(personality)
        else:
            self.default_pleasure = personality.pleasure
            self.default_arousal = personality.arousal
            self.default_dominance = personality.dominance
        self.pleasure = round(self.default_pleasure, 2)
        self.arousal = round(self.default_arousal, 2)
        self.dominance = round(self.default_dominance, 2)

    def __str__(self):
        return f"{self.pleasure:.2f}P {self.arousal:.2f}A {self.dominance:.2f}D"

    def __sub__(self, other):
        return (abs(self.pleasure - other.pleasure), abs(self.arousal - other.arousal), abs(self.dominance - other.dominance))

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
        old_pleasure = self.pleasure
        old_arousal = self.arousal
        old_dominance = self.dominance

        self.pleasure = self.pleasure + emotion.pleasure
        if self.pleasure > 1:
            self.pleasure = 1
        if self.pleasure < -1:
            self.pleasure = -1
        pleasure_change = abs(old_pleasure - self.pleasure)
        self.arousal = self.arousal + emotion.arousal
        if self.arousal > 1:
            self.arousal = 1
        if self.arousal < -1:
            self.arousal = -1
        arousal_change = abs(old_arousal - self.arousal)
        self.dominance = self.dominance + emotion.dominance
        if self.dominance > 1:
            self.dominance = 1
        if self.dominance < -1:
            self.dominance = -1
        dominance_change = abs(old_dominance - self.dominance)
        total_change = pleasure_change + arousal_change + dominance_change

        return self, total_change

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

    def in_upper_half(self, axis):
        if axis == "pleasure":
            if self.pleasure > 0:
                return True
        if axis == "arousal":
            if self.arousal > 0:
                return True
        if axis == "dominance":
            if self.dominance > 0:
                return True

        return False

    def get_default_pleasure(personality):
        return 0.21 * personality["E"] + 0.59 * personality["A"] + 0.19 * personality["N"]

    def get_default_arousal(personality):
        return 0.15 * personality["O"] + 0.3 * personality["A"] - 0.57 * personality["N"]

    def get_default_dominance(personality):
        return 0.25 * personality["O"] + 0.17 * personality["C"] + 0.6 * personality["E"] - 0.32 * personality["A"]
