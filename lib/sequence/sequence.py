from loaders import load_expansion_types, load_sequence_types
from sequence.turn import Turn
from concepts.project import Project
from concepts.affect.emotion import Emotion

import random
import copy

from numpy import array
from numpy.linalg import norm

POS_SEQUENCES, NEG_SEQUENCES, PASS_SEQUENCES = load_sequence_types()

EXPANSIONS = load_expansion_types()


class Sequence():
    def __init__(self, speaker_i, project, seq_type, surprise, action_types, world_state, parent=None):
        self.speakers = world_state.characters[:2]
        self.speaker_i = speaker_i
        self.reacter_i = 0 if speaker_i == 1 else 1
        self.project = project
        self.seq_type = seq_type
        self.action_types = action_types
        self.parent = parent
        self.world_state = world_state
        agreement = self.project.listener_agrees(self.speakers, self.speaker_i, self.reacter_i)
        self.pair_types = POS_SEQUENCES if agreement else NEG_SEQUENCES
        self.surprise = False
        if surprise:
            self.surprise = True
        reverse = False
        if seq_type in ["SKÄS"] and self.speakers[speaker_i].name == self.project.subj.name and project.verb != "olla":
            reverse = True
        elif seq_type in ["SKÄS"] and self.speakers[speaker_i].name == self.project.subj.name:
            self.seq_type = "SKAN"
        #todo: add emotional weights
        #also do this before second pair part is even determined?
        action_names = random.choice(self.pair_types[self.seq_type])
        self.first_pair_part = self.generate_pair_part(self.speakers[speaker_i], action_names[0], reverse)
        self.second_pair_part = self.generate_pair_part(self.speakers[self.reacter_i], action_names[1], reverse)
        self.pre_expansion = self.generate_expansion("pre_expansions", None)
        self.infix_expansion = self.generate_expansion("infix_expansions", self.first_pair_part, True)
        self.post_expansion = self.generate_expansion("post_expansions", self.second_pair_part)
        self.turns = []
        if self.pre_expansion is not None:
            for turn in self.pre_expansion.turns:
                self.turns.append(turn)
        self.turns.append(self.first_pair_part)
        if self.infix_expansion is not None:
            for turn in self.infix_expansion.turns:
                self.turns.append(turn)
        if self.second_pair_part is not None:
            self.turns.append(self.second_pair_part)
        if self.post_expansion is not None:
            for turn in self.post_expansion.turns:
                self.turns.append(turn)

        if agreement and self.project.proj_type in ["proposal", "statement"]:
            self.speakers[self.speaker_i].resolve_goal(self.project)


    def generate_expansion(self, position, parent, switch_speakers=False):
        if position == "infix_expansions" and self.surprise:
            surprise_project = self.project.get_surprise_project()
            #todo: weight sequence type by mood?
            #personal = "personal" if project.subj is Character else "impersonal"
            sequence_type = "SYLL"
            prev = self.parent
            return Sequence(self.reacter_i, surprise_project, sequence_type, False, self.action_types, self.world_state, prev)

        #toggle expansions (other than surprise) on or off
        return None

        if switch_speakers:
            speaker_i = 0 if self.speaker_i == 1 else 1
        else:
            speaker_i = self.speaker_i

        expansion = None
        rand = random.uniform(0, 2)
        mood = self.speakers[speaker_i].mood.arousal
        if rand < mood:
            new_project = self.project.get_expansion_project()
            if position not in EXPANSIONS[self.seq_type]:
                return None
            pool = EXPANSIONS[self.seq_type][position]
            if pool[0] == "":
                return None

            mood = self.speakers[speaker_i].mood
            #todo: weight by mood?

            new_seq_type = random.choice(pool)
            if new_seq_type == "SKORB":
                # new project with old object as subject? check if there is an object to take?
                if self.project.obj:
                    target = self.project.obj
                    # todo: how to handle emotions? asking "mikä surullinen?" doesn')t really make sense, does it?
                    attributes = list(target.attributes.items())
                    if len(attributes) is 0:
                        return None
                    else:
                        attribute = random.choices(attributes)[0]

                    new_project = Project(target, "olla", attribute, "expansion", "present", 0.2)
            expansion = Sequence(speaker_i, new_project, new_seq_type, False, self.action_types, self.world_state, parent)
        return expansion

    def generate_pair_part(self, speaker, action_name, reverse):
        if action_name == "TOI":
            if self.parent is None:
                print("parent is none", self.project.subj, self.project.verb, self.project.obj)
            action_type = self.action_types[self.parent.action_type.name]
        else:
            #print("action name", action_name)
            action_types_pool = [act_name for act_name in self.action_types.values() if act_name.class_name == action_name and act_name.can_use(self.speakers[self.speaker_i].mood)]
            if len(action_types_pool) == 0:
                print("no available turn types!", action_name)
                return None
            action_type = self.find_best_action_type(speaker, action_types_pool)
        project = self.project
        if action_name == "SEL":
            project = Project.get_new_project(self.speakers, self.project, self.world_state)

        listeners = []
        for char in self.speakers:
            if char.name is not speaker.name:
                listeners.append(char)
        hesitation = False
        if speaker == self.speakers[self.speaker_i]:
            hesitation = action_type.get_hesitation(speaker, self.speakers[self.reacter_i], self.project)
        return Turn(speaker, listeners, action_type, project, reverse, hesitation)

    def find_best_action_type(self, speaker, pool):
        other_char = self.world_state.get_opposite(speaker)
        target_mood = speaker.relations[other_char.name]
        current_mood = speaker.perception.get_object_by_name(other_char.name).mood
        best = pool[0]
        smallest_mood_diff = 9001.0
        mood_copy = copy.copy(current_mood)
        for act_type in pool:
            mood_diff = norm(mood_copy.affect_mood(act_type.effect)[0] - target_mood)
            if mood_diff < smallest_mood_diff:
                smallest_mood_diff = mood_diff
                best = act_type
        return best

    def print_sequence(self):
        print(self)

    def get_latex(self):
        ret = []
        if self.pre_expansion is not None:
            ret.append(str(self.pre_expansion))
        ret.append(self.first_pair_part.get_latex())
        if self.infix_expansion is not None:
            ret.append(self.infix_expansion.get_latex())
        if self.second_pair_part:
            ret.append(self.second_pair_part.get_latex())
        if self.post_expansion is not None:
            ret.append(str(self.post_expansion))
        return "\n".join(ret)


    def __str__(self):
        ret = []
        if self.pre_expansion is not None:
            ret.append(str(self.pre_expansion))
        ret.append(str(self.first_pair_part))
        if self.infix_expansion is not None:
            ret.append(str(self.infix_expansion))
        if self.second_pair_part:
            ret.append(str(self.second_pair_part))
        if self.post_expansion is not None:
            ret.append(str(self.post_expansion))
        return "\n".join(ret)

    def to_json(self):
        ret = []
        # if self.pre_expansion is not None:
        #     ret.append(str(self.pre_expansion))
        # ret.append(str(self.first_pair_part))
        # if self.infix_expansion is not None:
        #     ret.append(str(self.infix_expansion))
        # if self.second_pair_part:
        #     ret.append(str(self.second_pair_part))
        # if self.post_expansion is not None:
        #     ret.append(str(self.post_expansion))
        # return ret
        return {
            "speakers": self.speakers,
            # "project": self.project,
            "seq_type": self.seq_type,
            # "action_types": self.action_types,
            # "parent": str(self.parent),
            # "pair_types": self.pair_types,
            "first_pair_part": self.first_pair_part,
            "second_pair_part": self.second_pair_part,
            "pre_expansion": self.pre_expansion,
            "infix_expansion": self.infix_expansion,
            "post_expansion": self.post_expansion
        }


def main(sequence):
    sequence.print_sequence()


if __name__ == "__main__":
    s = Sequence([1, 2], 1)
    main(s)
