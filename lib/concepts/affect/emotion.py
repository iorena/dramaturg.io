import csv, random


class Emotion:
    def __init__(self, name, pleasure, arousal, dominance):
        self.name = name
        self.pleasure = pleasure
        if pleasure is None:
            self.pleasure = round(random.random(), 2)
        self.arousal = arousal
        if arousal is None:
            self.arousal = round(random.random(), 2)
        self.dominance = dominance
        if dominance is None:
            self.dominance = round(random.random(), 2)

        if name is None:
            self.name = Emotion.identify_emotion(self.pleasure, self.arousal, self.dominance)
        #todo: add attributes??
        self.attributes = {}
        self.id = None

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name

    def __mul__(self, other):
        self.pleasure = round(self.pleasure * other, 2)
        self.arousal = round(self.arousal * other, 2)
        self.dominance = round(self.dominance * other, 2)
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

