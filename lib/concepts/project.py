from concepts.worldobject import WorldObject
from concepts.location import Location
from concepts.affect.emotion import Emotion

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]

class Project:
    def __init__(self, subj, verb, obj, proj_type, time, weight):
        self.subj = subj
        self.obj_type = obj[0]
        self.obj = obj[1]
        self.verb = verb
        self.proj_type = proj_type
        if self.obj is None:
            print("none", self.subj, self.obj_type, self.verb)
        if self.obj_type is "quality":
            time = "present"
        self.time = time
        self.weight = weight

    def __str__(self):
        return (f"{self.subj} {self.verb} {self.obj} {self.proj_type} {self.time} {self.weight}")

    def __eq__(self, other):
        return self.subj == other.subj and self.verb == other.verb and self.obj == other.obj and self.obj_type == other.obj_type and self.proj_type == other.proj_type

    def get_appraisal(self, character):
        if self.verb == "kuolla":
            print("death is not nice")
            return WorldObject(APPRAISALS[0], 90)
        if self.obj_type is "owner":
            #todo: shouldn't this be the appraisal of the object owned?
            return WorldObject(APPRAISALS[3], 93)
        elif type(self.obj) in [WorldObject, Location]:
            return character.perception.get_object(self.obj).attributes["appraisal"]
        return WorldObject(APPRAISALS[2], 92)

    def get_emotional_effect(self, character):
        #todo: neutral events are negative now
        if self.proj_type == "statement":
            if self.get_appraisal(character).id > 92:
                if self.get_surprise(character, True):
                    emotion = Emotion(None, 0.4, 0.2, 0.1) #joy
                else:
                    emotion = Emotion(None, 0.3, -0.2, 0.4) #satisfaction
            else:
                if self.get_surprise(character, True):
                    emotion = Emotion(None, -0.4, -0.2, -0.5) #distress
                else:
                    emotion = Emotion(None, -0.5, -0.3, -0.7) #fears-confirmed
        elif self.proj_type == "proposal":
            if self.get_appraisal(character).id > 92:
                emotion = Emotion(None, 0.4, 0.2, -0.3) #gratitude
            else:
                emotion = Emotion(None, -0.51, 0.59, 0.25) #anger
        else:
            print("emotional evaluation shouldn't be done on", self.proj_type)

        weighted_emotion = emotion * self.weight
        print("weighted", weighted_emotion)
        return weighted_emotion

    def is_in_conflict_with(self, other):
        if self.verb == other.verb and self.subj != other.subj and self.obj == other.obj:
            return True
        return False

    def speakers_agree(self, speakers):
        if self.proj_type in ["surprise", "expansion"]:
            return True

        agreement = True

        for goal in speakers[0].goals:
            if self.is_in_conflict_with(goal):
                print("disagreement")
                agreement = False
        for goal in speakers[1].goals:
            if self.is_in_conflict_with(goal):
                print("disagreement")
                agreement = False

        return agreement
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

    def get_surprise(self, subject, just_checking=False):
        if self.proj_type == "expansion":
            return False
        if self in subject.memory:
            return False
        if not just_checking:
            subject.add_memory(self)
        return True

    def get_surprise_project(self):
        #todo: happy surprise or sad surprise?
        if self.verb == "kuolla":
            verb = "sairastua"
        elif self.verb == "ottaa":
            verb = "haluta"
        else:
            verb = self.verb
        return Project(self.subj, verb, (self.obj_type, self.obj), "surprise", self.time, self.weight/1.5)

    def get_expansion_project(self):
        return Project(self.subj, self.verb, (self.obj_type, self.obj), "expansion", self.time, self.weight/2)

    def get_new_project(speakers, main_project, world_state):
        #random topic: weather etc
        rand = random.random()
        if rand > 0.7:
            subj = world_state.weather
            obj = ("weather", speakers[0].attributes["location"].attributes["weather"])
            #todo: can weather be something else besides statement?
            project = Project(subj, "olla", obj, "statement", main_project.time, 0.1)
        #opposite topic
        elif rand > 0.3 and main_project.verb is "olla":
            obj = (main_project.obj_type, world_state.get_opposite(main_project.obj))
            project = Project(main_project.subj, "olla", obj, "statement",  main_project.time, main_project.weight)
        #relationship between characters
        else:
            subj = speakers[0]
            obj = ("relationship", speakers[1])
            verb = "pitää"
            if subj.relations[speakers[1].name].liking["outgoing"] < 0.5:
                verb = "vihata"
            project = Project(subj, verb, obj, "statement", "present", 0.8)

        return project

    def get_hello_project(speakers):
        #same place
        if speakers[0].attributes["location"] == speakers[1].attributes["location"]:
            return Project(speakers[0], "tehdä", ("location", speakers[0].attributes["location"]), "statement", "present", 0.2)
        #different place -> phone call
        else:
            return Project(speakers[0], "soittaa", ("character", speakers[1]),  "statement", "past", 0.4)

