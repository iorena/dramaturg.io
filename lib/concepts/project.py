from concepts.worldobject import WorldObject
from concepts.location import Location

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]


class Project:
    def __init__(self, subj, obj, topic_type, time):
        self.subj = subj
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.type = topic_type
        self.verb = self.get_verb()
        self.time = time
        if self.obj_type is "quality":
            time = "present"

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

    def get_appraisal(self, character):
        if self.obj_type is "owner":
            #todo: shouldn't this be the appraisal of the object owned?
            return WorldObject(93, APPRAISALS[3])
        elif type(self.obj) in [WorldObject, Location]:
            return character.perception.get_object(self.obj).attributes["appraisal"]
        return WorldObject(92, APPRAISALS[2])

    def speakers_agree(self, speakers):
        if self.type == "statement":
            first_perception = speakers[0].perception.get_object(self.subj)
            second_perception = speakers[1].perception.get_object(self.subj)
            if first_perception.attributes == second_perception.attributes:
                return True
            return False
        elif self.type == "action":
            evaluation = self.get_appraisal(speakers[1])
            if evaluation.id < 92:
                return False
            return True

    def get_new_project(speakers, main_project, world_state):
        #random topic: weather etc
        rand = random.random()
        if rand > 0.7:
            subj = world_state.weather
            obj = ("weather", speakers[0].attributes["location"].attributes["weather"])
            project = Project(subj, obj, "statement", main_project.time)
        #opposite topic
        elif rand > 0.3 and main_project.type is "statement":
            obj = (main_project.obj_type, world_state.get_opposite(main_project.obj))
            project = Project(main_project.subj, obj, "statement", main_project.time)
        #relationship between characters
        else:
            subj = speakers[0]
            obj = ("relationship", speakers[1])
            project = Project(subj, obj, "statement", "present")

        return project
