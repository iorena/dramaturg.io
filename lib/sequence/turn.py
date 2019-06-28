from language.sentence import Sentence
from concepts.affect.emotion import Emotion

import random

class Turn:
    """
    Todo: turns can have more than one sentence?
    """
    def __init__(self, speaker, listeners, action_type, project, reverse):
        self.speaker = speaker
        #todo: where to do this??
        if project.obj_type is "affect" and self.speaker.name is project.subj:
            self.speaker.mood.affect_mood(project.obj)
        else:
            self.speaker.mood.degrade_mood()
        self.listeners = listeners
        self.action_type = action_type
        self.obj_type = project.obj_type
        self.project = project
        self.speaker_mood = str(self.speaker.mood)
        self.reversed = reverse
        self.inflected = self.inflect()

    def __str__(self):
        space = "" if len(self.action_type.name) == 4 else " "
        return f"{self.action_type.name}{space} {self.speaker.name}: {self.inflected}  |  Mood: {self.speaker_mood}"

    def inflect(self):
        sentence = Sentence(self.speaker, self.listeners, self.project, self.action_type, self.obj_type, self.reversed)
        return sentence.styled

    def to_json(self):
        return {
            **self.__dict__,
            "pos": None,
        }


def main():
    print("Generated turn")


if __name__ == "__main__":
    main()
