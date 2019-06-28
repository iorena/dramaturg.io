

class Project:
    def __init__(self, subj, obj, time, valence):
        self.subj = subj if type(subj) is str else subj.name
        if type(subj) is str:
            print("haloo?", subj)
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.verb = self.get_verb()
        self.time = time
        if self.obj_type is "quality":
            time = "present"
        self.valence = valence

    def get_verb(self):
        if self.obj_type is "location":
            return "siirtyä"
        if self.obj_type is "owner":
            return "hankkia"
        return "olla"
