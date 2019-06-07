

class Project:
    def __init__(self, subj, obj, topic_type, time):
        self.subj = subj.name
        self.type = topic_type
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.verb = self.get_verb()
        self.time = time

    def get_verb(self):
        if self.type is "statement":
            return "olla"
        if self.obj_type is "location":
            return "siirtyä"
