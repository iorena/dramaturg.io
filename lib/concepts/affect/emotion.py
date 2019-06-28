class Emotion:
    def __init__(self, name, pleasure, arousal, dominance):
        self.name = name
        self.pleasure = pleasure
        self.arousal = arousal
        self.dominance = dominance
        #todo: add attributes??
        self.attributes = {}

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
