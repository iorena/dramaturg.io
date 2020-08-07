from sequence.sequence import Sequence
from language.action_types import ActionType
from language.sentence import Sentence
from concepts.project import Project
from concepts.character import Character

from loaders import load_emotions, load_action_types, load_pad_values

EMOTIONS = load_emotions()

from numpy import array
from numpy.linalg import norm

SEQUENCE_TYPES = {"proposal": "STOP", "statement": "SVÄI", "surprise": "SYLL", "question": "SKYS", "pivot": "SPVT", "change": "SMMU", "hello": "STER", "why": "STPB"}


class Situation:
    def __init__(self, world_state, embeddings, speakers, rules, location):
        self.world_state = world_state
        self.embeddings = embeddings
        self.speakers = speakers
        for char in self.speakers:
            char.reset_turn_memory()
        self.location = location
        self.rules = rules
        self.action_types = load_pad_values(load_action_types())
        self.mood_change = {}
        self.main_sequence_id = 0
        self.sequences = []
        self.create_sequences()


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
        while len(self.speakers[0].goals) > 0 or len(self.speakers[1].goals) > 0:
            #higher dominance gets to speak

            if len(self.speakers[0].goals) == 0 or (len(self.speakers[1].goals) > 0 and self.speakers[0].mood.dominance < self.speakers[1].mood.dominance):
                speaker_i = 1
                reacter_i = 0
            else:
                speaker_i = 0
                reacter_i = 1

            speaker = self.speakers[speaker_i]
            reacter = self.speakers[reacter_i]
            project = speaker.goals[0]

            mood = speaker.mood
            surprise = False
            if project.get_surprise(reacter):
                surprise = True
            self.sequences.append(self.get_new_sequence(project, speaker_i, surprise))
        # add hello sequence
        hello_project = Project.get_hello_project(self.speakers)
        #todo: can be surprised by hello?
        self.sequences.insert(0, self.get_new_sequence(hello_project, 0, False))

    def get_new_sequence(self, project, speaker_i, surprise):
        #todo: expansions
        speaker = self.speakers[speaker_i]
        personal = "personal" if project.subj is Character else "impersonal"
        sequence_type = SEQUENCE_TYPES[project.proj_type]
        prev = None if len(self.sequences) is 0 or project.proj_type == "hello" else self.sequences[-1]
        return Sequence(self.speakers, speaker_i, project, sequence_type, surprise, self.action_types, self.world_state, prev)

    def to_json(self):
        return self.sequences
