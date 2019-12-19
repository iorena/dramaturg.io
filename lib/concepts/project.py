from concepts.worldobject import WorldObject
from concepts.location import Location

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]

class Project:
    def __init__(self, subj, verb, obj, proj_type, time, score):
        self.subj = subj
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.verb = verb
        self.proj_type = proj_type
        self.time = time
        if self.obj is None:
            print("none", self.subj, self.obj_type, self.verb)
        if self.obj_type is "quality":
            time = "present"
        self.score = score

    def __str__(self):
        return (f"{self.subj} {self.verb} {self.obj}")

    def get_appraisal(self, character):
        if self.obj_type is "owner":
            #todo: shouldn't this be the appraisal of the object owned?
            return WorldObject(APPRAISALS[3], 93)
        elif type(self.obj) in [WorldObject, Location]:
            return character.perception.get_object(self.obj).attributes["appraisal"]
        return WorldObject(APPRAISALS[2], 92)

    def speakers_agree(self, speakers):
        if self in speakers[0].goals and self in speakers[1].goals:
            return True
        return False
    """
        if self.verb == "olla":
            first_perception = speakers[0].perception.get_object(self.subj)
            second_perception = speakers[1].perception.get_object(self.subj)
            if first_perception.attributes == second_perception.attributes:
                return True
            return False
        elif self.verb == "mennä":
            first_perception = speakers[0].perception.get_object(self.obj)
            second_perception = speakers[1].perception.get_object(self.obj)
            if first_perception.attributes == second_perception.attributes:
                return True
            return False
        else:
            evaluation = self.get_appraisal(speakers[1])
            if evaluation.id < 92:
                return False
            return True
    """

    def get_surprise(self, subject):
        if self in subject.memory:
            return False
        subject.add_memory(self)
        print("boo")
        return True

    """
    this stuff should be used for generating surprise projects, no?
        if not self.verb in subject.world_model:
            return True
        causes = subject.world_model[self.verb]
        for cause in causes:
            for event in subject.memory:
                surprise = False
                if self.verb != event.verb:
                    surprise = True
                if self.subj == "self" and event.subj != subject:
                    surprise = True
                #todo: more conditional clauses?
                if not surprise:
                    return False
        return True
    """

    def get_surprise_project(self):
        #todo: happy surprise or sad surprise?
        return Project(self.subj, self.verb, (self.obj_type, self.obj), "surprise", "present", self.score - 2)

    def get_new_project(speakers, main_project, world_state):
        #random topic: weather etc
        rand = random.random()
        if rand > 0.7:
            subj = world_state.weather
            obj = ("weather", speakers[0].attributes["location"].attributes["weather"])
            #todo: can weather be something else besides statement?
            project = Project(subj, "olla", obj, "statement", main_project.time, 0)
        #opposite topic
        elif rand > 0.3 and main_project.verb is "olla":
            obj = (main_project.obj_type, world_state.get_opposite(main_project.obj))
            project = Project(main_project.subj, "olla", obj, "statement",  main_project.time, main_project.score)
        #relationship between characters
        else:
            subj = speakers[0]
            obj = ("relationship", speakers[1])
            verb = "pitää"
            if subj.relations[speakers[1].name].liking["outgoing"] < 0.5:
                verb = "vihata"
            project = Project(subj, verb, obj, "statement", "present", 4)

        return project

    def get_hello_project(speakers):
        #same place
        if speakers[0].attributes["location"] == speakers[1].attributes["location"]:
            return Project(speakers[0], "tehdä", ("location", speakers[0].attributes["location"]), "statement", "present", 1)
        #different place -> phone call
        else:
            return Project(speakers[0], "soittaa", ("character", speakers[1]),  "statement", "past", 1)

