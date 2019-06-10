import csv


class Emotion:
    def load_emotions():
        emotions = {}
        with open("concepts/affect/emotion_to_pad.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=" ")
            for row in csv_reader:
                emotions[row[0]] = Emotion(row[0], float(row[1]), float(row[2]), float(row[3]))

        return emotions
    def __init__(self, name, pleasure, arousal, dominance):
        self.name = name
        self.pleasure = pleasure
        self.arousal = arousal
        self.dominance = dominance

    def __hash__(self):
        return hash(self.name)
