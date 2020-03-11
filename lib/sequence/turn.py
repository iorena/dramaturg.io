from language.sentence import Sentence

import random
import copy

class Turn:
    """
    Todo: turns can have more than one sentence?
    """
    def __init__(self, speaker, listeners, action_type, project, reverse, hesitation):
        self.speaker = speaker
        self.listeners = listeners
        self.action_type = action_type
        self.obj_type = project.obj_type
        self.project = project
        self.speaker_mood = copy.copy(self.speaker.mood)
        self.listener_mood = copy.copy(self.listeners[0].mood)
        self.change = 0
        self.reversed = reverse
        self.hesitation = hesitation
        self.inflected = self.inflect()
        self.affect_mood()

    def __str__(self):
        space = "" if len(self.action_type.name) == 4 else " "
        return f"{self.action_type.name}{space} {self.speaker.name}: {self.inflected} | Mood: {str(self.speaker_mood)} | Hesitation: {self.hesitation}"

    def get_latex(self):
        return f"{str(self.speaker_mood)} & {self.speaker.name} & {self.inflected} \\\\"

    def inflect(self):
        sentence = Sentence(self.speaker, self.listeners, self.project, self.action_type, self.obj_type, self.reversed, self.hesitation)
        return sentence.styled

    def affect_mood(self):
        #todo: how do expansions affect mood? does this work as is? add importance coefficient?
        self.change = self.listeners[0].mood.affect_mood(self.action_type.effect)[1]
        if self.project.proj_type in ["statement", "proposal"]:
            self.change += self.listeners[0].mood.affect_mood(self.project.get_emotional_effect(self.listeners[0]))[1]

    def to_json(self):
        return {
            **self.__dict__,
            "pos": None,
        }


def main():
    print("Generated turn")


if __name__ == "__main__":
    main()
