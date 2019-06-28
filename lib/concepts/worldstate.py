import copy

from concepts.character import Character
from concepts.location import Location
from concepts.worldobject import WorldObject

import random


class WorldState:
    def __init__(self, old=None):
        if old is None:
            self.initialize_story_world()
        else:
            self.locations = old.locations
            self.characters = old.characters
            self.objects = old.objects

    def initialize_story_world(self):
        self.locations = [Location(), Location()]
        self.characters = [Character(self.get_random_loc()), Character(self.get_random_loc())]
        self.objects = [WorldObject()]
        for obj in self.objects:
            owner = random.choices(self.characters)[0]
            obj.set_owner(owner)
            obj.set_location(owner.attributes["location"])
        self.weather = WorldObject(None, "sää")
        self.appraisals = [WorldObject(None, "bad"), WorldObject(None, "okay"), WorldObject(None, "good")]
        #set relationships
        for char in self.characters:
            for other in self.characters:
                if char is other:
                    relationship = 1
                else:
                    relationship = random.random()
                char.set_relation(other, relationship)

    def get_random_loc(self):
        return random.choices(self.locations)[0]

    def __str__(self):
        return f"Locations: {', '.join(map(str, self.locations))}\nCharacters: {', '.join(map(str, self.characters))}"

    def to_json(self):
        return {"wordstate": str(self)}

    def __eq__(self, other):
        if other is None:
            return False
        for i in range(len(self.locations)):
            if other.locations[i] != self.locations[i]:
                return False
        for i in range(len(self.characters)):
            if other.characters[i].attributes != self.characters[i].attributes:
                return False
        return True

    """
    Functions for executing story points that change the world state
    Goals are Transitions objects, except boolean in IE
    """
    def change(self, fe_type, subject, goal, success):
        if fe_type is "G":
            pass
            #self.goal(subject, goal)
        elif fe_type is "A":
            self.action(subject, goal, success)
        elif fe_type is "P":
            self.perception(subject, goal, success)
        elif fe_type is "IE":
            #mood change is handled in Turn?
            #self.internal(subject, emotion)
            pass

    def goal(self, subject, goal):
        state = copy.deepcopy(self)
        state.characters[subject.id].attributes.update(goal)
        self.characters[subject.id].goals.append(state)

    def action(self, subject, action, success):
        if success:
            if type(action.obj) is Character:
                self.characters[action.obj.id].attributes[action.attribute_name] = action.end_value
                print("updated", action.attribute_name, action.end_value)
            else:
                self.objects[action.obj.id].attributes[action.attribute_name] = action.end_value

    #todo: add perceptions
    def perception(self, subject, perception, success):
        self.characters[subject.id].perception = perception

    def internal(self, subject, emotion):
        self.characters[subject.id].mood.affect(emotion)
