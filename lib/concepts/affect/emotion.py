import csv


class Emotion:
    def __init__(self, name, pleasure, arousal, dominance):
        self.name = name
        if name is None:
            self.name = Emotion.identify_emotion(pleasure, arousal, dominance)
        self.pleasure = pleasure
        self.arousal = arousal
        self.dominance = dominance
        #todo: add attributes??
        self.attributes = {}
        self.id = None

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __mul__(self, other):
        self.pleasure *= other
        self.arousal *= other
        self.dominance *= other
        return self

    def identify_emotion(pleasure, arousal, dominance):
        pleasure = pleasure > 0
        arousal = arousal > 0
        dominance = dominance > 0
        as_string = Emotion.get_sign(pleasure) + "P" + Emotion.get_sign(arousal) + "A" + Emotion.get_sign(dominance) + "D"
        with open("../data/emotion_to_pad.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            for row in csv_reader:
                if row[4] == as_string:
                    return row[0]
        return "unknown"


    def get_sign(value):
        if value:
            return "+"
        return "-"

