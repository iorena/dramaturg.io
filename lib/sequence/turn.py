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
        self.verbalized_change = {}
        self.reversed = reverse
        self.hesitation = hesitation
        self.inflected = self.inflect()
        self.affect_mood()
        self.add_turn_memories()

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
        character = self.listeners[0]
        old_mood = copy.copy(character.mood)
        self.change = character.mood.affect_mood(self.action_type.effect)[1]
        if self.project.proj_type in ["statement", "proposal"]:
            self.change += character.mood.affect_mood(self.project.get_emotional_effect(character))[1]
        new_mood = copy.copy(character.mood)
        change = None
        if old_mood.get_character_description("pleasure") != new_mood.get_character_description("pleasure"):
            if old_mood.pleasure < new_mood.pleasure:
                change = "ilahtuu"
            else:
                change = "suuttuu"
        if old_mood.get_character_description("arousal") != new_mood.get_character_description("arousal"):
            if old_mood.arousal < new_mood.arousal:
                change = "ilahtuu"
            else:
                change = "suuttuu"
        if old_mood.get_character_description("dominance") != new_mood.get_character_description("dominance"):
            if old_mood.dominance < new_mood.dominance:
                change = "ilahtuu"
            else:
                change = "suuttuu"
        if change is not None:
            self.verbalized_change[character.name] = change


    def add_turn_memories(self):
        self.speaker.add_said_memory(self.action_type.name)
        for listener in self.listeners:
            listener.add_heard_memory(self.action_type.name, self.speaker)

    def get_sentence_type(self):
        names = {
            "TER": "tervehdys",
            "KYS": "kysymys",
            "TOP": "toimintapyyntö",
            "TTN": "myöntyminen (toimintapyyntöön)",
            "TTS": "kieltäytyminen (toimintapyyntöön)",
            "VÄI": "väite",
            "MYÖ": "myöntyminen (väitteeseen)",
            "KII": "kiistäminen (väitteen)",
            "YLL": "yllätys",
            "VYL": "yllätyksen kuittaus",
            "VSM": "myönteinen vastaus kysymykseen",
            "VSK": "kielteinen vastaus kysymykseen",
            "MMU": "mielen muutos",
            "MMK": "mielenmuutoksen kuittaus",
            "PVT": "aiheen vaihto/pohjustus",
            "PVK": "aiheen vaihdon kuittaus",
            "TPB": "kysymys (miksi)",
            "TOR": "kysymyksen torjunta",
            "VVA": "vastaväite",
            "VVK": "vastaväitteen kiistäminen",
            "EST": "passiivinen torjunta",
            "VAL": "valitus",
            "VLK": "valituksen kuittaus"
        }
        name = self.action_type.name[:3]
        if name in names:
            return names[name]
        return "muu"

    def to_json(self):
        return {
            **self.__dict__,
            "pos": None,
        }


def main():
    print("Generated turn")


if __name__ == "__main__":
    main()
