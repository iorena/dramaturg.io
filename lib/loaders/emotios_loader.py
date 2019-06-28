import csv

from concepts.affect.emotion import Emotion


def load_emotions(path="../data/emotion_to_pad.csv"):
    emotions = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=" ")
        for row in csv_reader:
            emotions[row[0]] = Emotion(row[0], float(row[1]), float(row[2]), float(row[3]))

    return emotions
