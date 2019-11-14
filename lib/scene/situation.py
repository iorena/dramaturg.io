from sequence.sequence import Sequence
from language.action_types import ActionType
from language.sentence import Sentence
from concepts.project import Project
from concepts.character import Character
from language.dictionary import pivot_dictionary

from loaders import load_emotions, load_action_types, load_pad_values

EMOTIONS = load_emotions()
PAD_VALUES = load_pad_values()

import random, copy
from numpy import array
from numpy.linalg import norm

SEQUENCE_TYPES = {"personal": {"proposal": ["STOE", "STOP", "STOPB", "SKÄS"], "narration": ["SVÄI"], "surprise": ["SEST", "STIPC", "STII"]},
        "impersonal": {"proposal": ["STOP"], "narration": ["SVÄI"], "surprise": ["SEST", "STIPC", "STII"]}}


class Situation:
    def __init__(self, world_state, embeddings, element_type, speakers, main_project, prev_project, location):
        self.world_state = world_state
        self.embeddings = embeddings
        self.element_type = element_type
        self.speakers = speakers
        self.main_project = main_project
        self.prev_project = prev_project
        self.location = location
        self.action_types = load_action_types()
        self.mood_change = {}
        if type(self.main_project.subj) is Character:
            self.affect_emotions()
        self.main_sequence_id = 0
        self.open_questions = [Project.get_hello_project(self.speakers), self.main_project]
        self.sequences = self.create_sequences()

    def affect_emotions(self):
        """
        When an event happens to a character, characters react emotionally to it
        """
        for character in self.speakers:
            relationship = character.relations[self.main_project.subj.name].liking["outgoing"] > 0.5
            event_appraisal = self.main_project.get_appraisal(character).id > 92
            if self.main_project.get_appraisal(character).id is 92:
                #neutral event, nothing happens
                return
            is_self = character is self.main_project.subj
            emotion = EMOTIONS[self.get_emotion(is_self, relationship, event_appraisal)]
            old_mood = copy.copy(character.mood)
            character.mood.affect_mood(emotion)
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
                self.mood_change[character.name] = change

    def get_emotion(self, is_self, relationship, event):
        if is_self and event:
            return "joy"
        if is_self and not event:
            return "distress"
        if relationship and event:
            return "happy_for"
        if relationship and not event:
            return "pity"
        if not relationship and event:
            return "resentment"
        if not relationship and not event:
            return "gloating"

    def create_sequences(self):
        """
        Generates sequences for each project
        """
        sequences = []
        for i in range(len(self.open_questions)):
            project = self.open_questions[i]
            mood = self.speakers[0].mood
            surprise = False
            sequences.append(self.get_new_sequence(sequences, project))
            if project.get_surprise(self.speakers[1]):
                surprise = True

            if surprise:
                surprise_project = project.get_surprise_project()
                #todo: weight sequence type by mood?
                personal = "personal" if project.subj is Character else "impersonal"
                sequence_type = random.choice(SEQUENCE_TYPES[personal]["surprise"])
                prev = None if len(sequences) is 0 else sequences[-1]
                sequences.append(Sequence([self.speakers[1], self.speakers[0]], surprise_project, sequence_type, self.action_types, self.world_state, prev))

            disagreement = project == self.main_project and abs(self.speakers[0].mood.dominance - self.speakers[1].mood.dominance) < 0.75
            while disagreement:
                sequences.append(self.get_new_sequence(sequences, project))
                disagreement = project == self.main_project and abs(self.speakers[0].mood.dominance - self.speakers[1].mood.dominance) > 0.75

        return sequences

    def get_new_sequence(self, sequences, project):
        personal = "personal" if project.subj is Character else "impersonal"
        sequence_type = random.choice(SEQUENCE_TYPES[personal][self.element_type])
        if project == self.open_questions[0]:
            sequence_type = "STER"
        prev = None if len(sequences) is 0 else sequences[-1]
        return Sequence(self.speakers, project, sequence_type, self.action_types, self.world_state, prev)

    def to_json(self):
        return self.sequences
