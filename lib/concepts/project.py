from concepts.worldobject import WorldObject

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]


class Project:
    def __init__(self, subj, obj, topic_type, time, valence):
        self.subj = subj
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
        if self.obj_type is "relationship":
            if self.subj.relations[self.obj.name].liking["outgoing"] > 0.5:
                return "pitää"
            else:
                return "vihata"
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

    def get_new_project(speakers, main_project, world_state):
        #random topic: weather etc
        rand = random.random()
        if rand > 0.7:
            subj = world_state.weather
            obj = ("quality", random.choices(world_state.appraisals)[0])
            project = Project(subj, obj, "statement", main_project.time, True)
        #opposite topic
        elif rand > 0.3 and main_project.type is "statement":
            obj = (main_project.obj_type, world_state.get_opposite(main_project.obj))
            project = Project(main_project.subj, obj, "statement", main_project.time, False)
        #relationship between characters
        else:
            subj = speakers[0]
            obj = ("relationship", speakers[1])
            project = Project(subj, obj, "statement", "present", True)

        return project
