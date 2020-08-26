import random


class SituationGrammar:
    def __init__(self):
        # todo: move to excel
        self.grammar = {
                    "are_lectured_by": (["are_bored_by", "look_up_to",], "pleasure"),
                    "are_bored_by": ["complain"],
                    "look_up_to": ["are_indoctrinated_by"],
                    "complain": (["are_bored_by", "are_dismissed_by"], "dominance"),
                    "are_indoctrinated_by": ["lie_for"],
                    "lie_for": ["are_rewarded_by"]
                }

    def get_next_situation(self, character, previous):
        if previous is None:
            return "are_lectured_by"
        if previous not in self.grammar:
            print("not found", previous)
            return None
        next_sit = self.grammar[previous]
        if len(next_sit) == 1:
            return next_sit[0]
        # story can branch in two, but not more options
        if character.mood.in_upper_half(next_sit[1]):
            return next_sit[0][1]
        else:
            return next_sit[0][0]
