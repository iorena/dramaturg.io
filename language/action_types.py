import csv


class ActionType:
    def load_action_types():
        actions = {}
        with open("language/action_types.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            for row in csv_reader:
                actions[row[0]] = ActionType(*row)
        return actions

    def __init__(self, name, neg, ques, subj, verb, aux_verb, modus, tempus, pre_add):
        self.name = name
        self.neg = neg == "TRUE"
        self.ques = ques == "TRUE"
        self.subj = subj
        self.verb = verb
        if verb == "None":
            self.verb = None
        if aux_verb == "None":
            self.aux_verb = None
        else:
            self.aux_verb = aux_verb.split(",")
        self.modus = modus
        self.tempus = tempus
        self.pre_add = pre_add
        if pre_add == "None":
            self.pre_add = None
