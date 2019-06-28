

class Project:
    def __init__(self, subj, obj, topic_type, time, valence):
        self.subj = subj if type(subj) is str else subj.name
        if type(subj) is str:
            print("haloo?", subj)
        self.type = topic_type
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.verb = self.get_verb()
        self.time = time
        self.valence = valence

    def get_verb(self):
        if self.type is "statement":
            return "olla"
        if self.obj_type is "location":
            return "siirtyä"
        if self.obj_type is "owner":
            return "hankkia"
