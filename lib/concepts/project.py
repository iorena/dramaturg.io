from concepts.worldobject import WorldObject

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]


class Project:
    def __init__(self, subj, obj, topic_type, time, valence):
        self.subj = subj if type(subj) is str else subj.name
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.type = topic_type
        self.verb = self.get_verb()
        self.time = time
        if self.obj_type is "quality":
            time = "present"
        self.appraisal = self.get_appraisal()
        self.valence = valence

    def get_verb(self):
        if self.type is "statement":
            return "olla"
        if self.obj_type is "location":
            return "siirtyä"
        if self.obj_type is "owner":
            return "hankkia"
        return "olla"

    def get_appraisal(self):
        if self.obj_type is "quality" and type(self.obj) is WorldObject:
            return self.obj
        if self.obj_type is "location":
            return self.obj.attributes["appraisal"]
        if self.obj_type is "owner":
            return WorldObject(93, APPRAISALS[3])
        return WorldObject(92, APPRAISALS[2])
