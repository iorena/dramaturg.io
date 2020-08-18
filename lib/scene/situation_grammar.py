import random


class SituationGrammar:
    def __init__(self):
        self.grammar = {
                    "lecture": ["are_bored_by", "look_up_to"],
                    "are_bored_by": ["complain"],
                    "look_up_to": ["are_indoctrinated_by"],
                    "complain": ["are_bored_by", "are_dismissed_by"],
                    "are_indoctrinated_by": ["lie_for"],
                    "lie_for": ["are_rewarded_by"]
                }

    def create_situations(self):
        situations = ["lecture"]
        token = situations[0]
        while token in self.grammar:
            token = random.choice(self.grammar[token])
            situations.append(token)
        return situations


