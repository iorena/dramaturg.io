class ActionType:

    def __init__(self, name, neg, ques, subj, verb, obj, aux_verb, modus, tempus, passive, pre_add, post_add):
        self.name = name
        self.neg = neg == "TRUE"
        self.ques = ques == "TRUE"
        self.subj = subj
        if self.subj == "None":
            self.subj = None
        self.verb = verb
        if verb == "None":
            self.verb = None
        self.obj = obj
        if obj == "None":
            self.obj = None
        if aux_verb == "None":
            self.aux_verb = None
        else:
            self.aux_verb = aux_verb.split(",")
        self.modus = modus
        self.tempus = tempus
        self.passive = passive == "TRUE"
        self.pre_add = pre_add
        if pre_add == "None":
            self.pre_add = None
        self.post_add = post_add
        if post_add == "None":
            self.post_add = None
