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

SEQUENCE_TYPES = {"personal": {"proposal": ["STOE", "STOP", "STOPB", "SKÄS"], "statement": ["SVÄI"], "surprise": ["SEST", "STIPC", "STII"]},
        "impersonal": {"proposal": ["STOP"], "statement": ["SVÄI"], "surprise": ["SEST", "STIPC", "STII"]}}


class Situation:
    def __init__(self, world_state, embeddings, speakers, location):
        self.world_state = world_state
        self.embeddings = embeddings
        self.speakers = speakers
        self.location = location
        self.action_types = load_action_types()
        self.mood_change = {}
        self.main_sequence_id = 0
        self.sequences = []
        self.create_sequences()

    def affect_emotions(self):
        """
        When an event happens to a character, characters react emotionally to it
        NOT IN USE
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
        project = Project.get_hello_project(self.speakers)
        self.sequences.append(self.get_new_sequence(project, self.speakers))
        while len(self.speakers[0].goals) > 0 or len(self.speakers[1].goals) > 0:
            #higher dominance gets to speak
            if len(self.speakers[0].goals) == 0 or (len(self.speakers[1].goals) > 0 and self.speakers[0].mood.dominance + random.uniform(0, 0.5) < self.speakers[1].mood.dominance):
                project = self.speakers[1].goals[0]
                speaker = self.speakers[1]
                reacter = self.speakers[0]
            else:
                project = self.speakers[0].goals[0]
                speaker = self.speakers[0]
                reacter = self.speakers[1]

            mood = speaker.mood
            surprise = False
            self.sequences.append(self.get_new_sequence(project, [speaker, reacter]))
            if project.get_surprise(reacter):
                surprise = True
                #arrange so that cannot be surprised again by same thing

            if surprise:
                surprise_project = project.get_surprise_project()
                #todo: weight sequence type by mood?
                personal = "personal" if project.subj is Character else "impersonal"
                sequence_type = random.choice(SEQUENCE_TYPES[personal]["surprise"])
                prev = None if len(self.sequences) is 0 else self.sequences[-1]
                self.sequences.append(Sequence([reacter, speaker], surprise_project, sequence_type, self.action_types, self.world_state, prev))

            #resolve goal if both agree
            if project.speakers_agree(self.speakers):
                for speaker in self.speakers:
                    speaker.resolve_goal(project)

            else:
                #change mind if affected enough
                if speaker.mood.dominance > reacter.mood.dominance + 0.5:
                    reacter.set_goal(project)


    def get_new_sequence(self, project, speakers):
        #todo: expansions
        speaker = speakers[0]
        personal = "personal" if project.subj is Character else "impersonal"
        available_sequence_types = [seq_type for seq_type in SEQUENCE_TYPES[personal][project.proj_type] if speaker.mood.in_bounds(PAD_VALUES[seq_type][1])]
        if len(available_sequence_types) == 0:
            print("no available sequence types")
            return None
        available_sequence_types.sort(key=lambda x: norm(speaker.mood.as_array() - array((PAD_VALUES[x][0]))))
        sequence_type = available_sequence_types[0]
        if len(self.sequences) == 0:
            sequence_type = "STER"
        prev = None if len(self.sequences) is 0 else self.sequences[-1]
        return Sequence(speakers, project, sequence_type, self.action_types, self.world_state, prev)

    def to_json(self):
        return self.sequences
