from concepts.worldobject import WorldObject
from concepts.location import Location
from concepts.affect.emotion import Emotion

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]

class Project:
    def __init__(self, subj, verb, obj, proj_type, time, weight):
        if type(subj) is tuple:
            self.subj = subj[1]
            self.subj_modifier = subj[0]
        else:
            self.subj = subj
            self.subj_modifier = None
        self.second_obj_type = None
        self.second_obj = None
        if type(obj) is tuple:
            self.obj_type = obj[0]
            self.obj = obj[1]
        else:
            self.obj_type = obj[0][0]
            self.obj = obj[0][1]
            self.second_obj_type = obj[1][0]
            self.second_obj = obj[1][1]

        self.verb = verb
        self.proj_type = proj_type
        if self.obj_type is "quality":
            time = "present"
        self.time = time
        self.weight = weight

    def __str__(self):
        return (f"{self.subj} {self.verb} {self.obj} {self.proj_type} {self.time} {self.weight}")

    def __eq__(self, other):
        return self.subj.name == other.subj.name and self.verb == other.verb and self.obj == other.obj and self.obj_type == other.obj_type and self.proj_type == other.proj_type

    def get_appraisal(self, character):
        #death is always bad
        if self.verb == "kuolla":
            return WorldObject(APPRAISALS[0], 90)
        if self.proj_type == "change":
            return WorldObject(APPRAISALS[3], 93)
        if self.obj_type is "owner":
            #todo: shouldn't this be the appraisal of the object owned?
            return WorldObject(APPRAISALS[3], 93)
        if self.obj_type is "static":
            attributes = character.perception.get_object_by_name(self.obj).attributes
            if "appraisal" in attributes:
                return attributes["appraisal"]
        if type(self.obj) in [WorldObject, Location]:
            attributes = character.perception.get_object(self.obj).attributes
            if "appraisal" in attributes:
                return attributes["appraisal"]
        if type(self.obj) is str:
            attributes = character.perception.get_object_by_name(self.obj).attributes
            if "appraisal" in attributes:
                return attributes["appraisal"]
        return WorldObject(APPRAISALS[2], 92)

    def get_emotional_effect(self, character):
        #todo: neutral events are negative now
        if self.proj_type == "statement":
            if self.get_appraisal(character).id > 92:
                if self.get_surprise(character, True):
                    emotion = Emotion(None, 0.4, 0.2, 0.1) #joy
                else:
                    emotion = Emotion(None, 0.3, -0.2, 0.4) #satisfaction
            elif self.get_appraisal(character).id < 92:
                if self.get_surprise(character, True):
                    emotion = Emotion(None, -0.4, -0.2, -0.5) #distress
                else:
                    emotion = Emotion(None, -0.5, -0.3, -0.7) #fears-confirmed
            else:
                emotion = Emotion(None, 0, 0, 0) #neutral

        elif self.proj_type == "proposal":
            if self.get_appraisal(character).id > 92:
                emotion = Emotion(None, 0.4, 0.2, -0.3) #gratitude
            elif self.get_appraisal(character).id < 92:
                emotion = Emotion(None, -0.51, 0.59, 0.25) #anger
            else:
                emotion = Emotion(None, 0, 0, 0) #neutral
        else:
            print("emotional evaluation shouldn't be done on", self.proj_type)

        weighted_emotion = emotion * self.weight
        return weighted_emotion

    def is_in_conflict_with(self, other):
        if self.verb == other.verb and self.subj != other.subj and self.obj == other.obj:
            return True
        if self.verb == other.verb and self.subj == other.subj and self.obj != other.obj:
            return True
        return False

    # returns tuple (boolean agreement, <project that is in conflict>, or None)
    def get_listener_conflicting_project(self, speakers, speaker_i, listener_i):
        agreement = False
        if self in speakers[listener_i].beliefs:
            agreement = True
        if self.proj_type in ["question", "surprise", "hello", "expansion", "pivot", "change", "why"]:
            return (True, None)
        if self.subj == speakers[listener_i] and self.verb == "tietää":
            return (True, None)
        if self.obj == "kiitollinen":
            return (True, None)

        # if character has conflicting belief, we assume they don't have the same belief
        # maybe this could be added in future development
        for goal in speakers[listener_i].goals:
            if self.is_in_conflict_with(goal):
                return (False, goal)

        for belief in speakers[listener_i].beliefs:
            if self.is_in_conflict_with(belief):
                return (False, belief)

        return (agreement, None)
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
        if self.proj_type in ["expansion"]:
            return False
        # cannot be surprised by statements about self (such as "you know so much")
        if self.subj == subject or self.subj == "Listener":
            return False
        if subject.has_memory(self):
            return False
        if not just_checking:
            subject.add_memory(self)
        return True

    def get_surprise_project(self):
        #todo: happy surprise or sad surprise?
        #todo: make more surprise projects for new verbs
        if self.verb == "kuolla":
            verb = "sairastua"
        elif self.verb == "ottaa" or self.verb == "mennä":
            verb = "haluta"
        else:
            verb = self.verb
        return Project(self.subj, verb, (self.obj_type, self.obj), "surprise", self.time, self.weight/1.5)

    def get_expansion_project(self):
        return Project(self.subj, self.verb, (self.obj_type, self.obj), "expansion", self.time, self.weight/2)

    def get_new_project(speakers, main_project, world_state):
        #random topic: weather etc
        rand = random.random()
        if rand >= 0:
            subj = world_state.weather
            obj = ("weather", speakers[0].attributes["location"].attributes["weather"])
            #todo: can weather be something else besides statement?
            project = Project(subj, "olla", obj, "statement", main_project.time, 0.1)
        #opposite topic
        elif rand > 0.3 and main_project.verb is "olla":
            obj = (main_project.obj_type, world_state.get_opposite(world_state.get_object_by_name(main_project.obj)))
            project = Project(main_project.subj, "olla", obj, "statement",  main_project.time, main_project.weight)
        #relationship between characters
        else:
            subj = speakers[0]
            obj = ("relationship", speakers[1])
            verb = "pitää"
            if subj.relations[speakers[1].name].pleasure < 0:
                verb = "vihata"
            project = Project(subj, verb, obj, "statement", "present", 0.8)

        return project


    def get_action_word(proj_type):
        words = {
            "statement": "puhua",
            "proposal": "ehdottaa",
            "question": "kysyä"
        }
        return words[proj_type]


    def get_complain_project(character, prev_proj, main_proj, listener):
        # todo ???
        return Project(listener, "kuunnella", (None, None), "question", "present", 1)

    def get_boredom_project(speakers, main_project, char, listener):
        return Project.get_new_project(speakers, main_project, char.perception)

    def get_dismissal_project(main_char, listener):
        return Project(main_char, "mennä", ("static", "pois"), "proposal", "prees", 1)

    def get_look_up_to_project(character, listener):
        return Project(character, "tietää", ("static", "niin paljon"), "statement", "present", 1)

    def get_reward_project(speaker, listener):
        return Project(speaker, "olla", ("static", "kiitollinen"), "statement", "prees", 1)

    def get_refer_back_project(prev_project, main_project, listener):
        if prev_project is None:
            return Project(listener, Project.get_action_word(main_project.proj_type), [("obj", main_project.subj), ("obj", "Maija")], "question", "imperf", 0.5)
        return Project(listener, Project.get_action_word(prev_project.proj_type), [("obj", prev_project.subj), ("obj", "Maija")], "question", "imperf", 0.5)

    def get_indoctrination_project(main_project, listener):
        return Project(main_project.subj, main_project.verb, (main_project.obj_type, main_project.obj), "indoctrination", "prees", 0.5)

    def get_hello_project(speakers):
        #same place
        if speakers[0].attributes["location"] == speakers[1].attributes["location"]:
            return Project(speakers[0], "tehdä", ("location", speakers[0].attributes["location"]), "hello", "present", 0.2)
        #different place -> phone call
        else:
            return Project(speakers[0], "soittaa", ("character", speakers[1]),  "hello", "past", 0.2)

    def get_change_project(listener):
        return Project(listener, "ymmärtää", (None, None), "change", "present", 0.1)

    def get_pivot_project(listener):
        return Project(listener, "kuunnella", (None, None), "pivot", "present", 0.1)

    def get_repetition_project(char, listener):
        return Project(listener, "hokea", ("static", "tuota"), "why", "present", 0.1)
