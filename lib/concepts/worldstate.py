from concepts.character import Character
from concepts.location import Location
from concepts.worldobject import WorldObject
from concepts.affect.relationship import Relationship
from concepts.affect.emotion import Emotion
from concepts.method import Method

import random
import copy

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]
WEATHER_TYPES = ["sunny", "cloudy", "rainy", "stormy"]


class WorldState:
    def __init__(self, embeddings, old=None):
        if old is None:
            self.initialize_story_world(embeddings)
        else:
            self.embeddings = embeddings
            self.appraisals = old.appraisals
            self.locations = old.locations
            self.characters = old.characters
            self.objects = old.objects
            self.weather = old.weather
            self.weather_types = old.weather_types

    def initialize_story_world(self, embeddings):
        self.embeddings = embeddings
        self.appraisals = [WorldObject("horrible", 90), WorldObject("bad", 91), WorldObject("okay", 92), WorldObject("good", 93), WorldObject("great", 94)]
        self.weather_types = [WorldObject("sunny", 95), WorldObject("cloudy", 96), WorldObject("rainy", 97), WorldObject("stormy", 98)]
        self.locations = [Location(), Location()]
        self.characters = [Character(self.locations[0]), Character(self.locations[1]), Character(self.locations[0], self.embeddings.get_relative())]
        self.objects = [WorldObject(self.embeddings.get_inheritance_object())]
        self.inheritance_object = self.objects[0]
        self.dead_relative = self.characters[2]
        for obj in self.objects:
            owner = self.characters[2]
            obj.set_owner(owner)
            obj.set_location(owner.attributes["location"])
        self.weather = WorldObject("sää", 95)
        self.influence_methods = [Method("pyytäminen", 1), Method("neuvottelu", 2), Method("lahjonta", 5), Method("uhkailu", 8)]
        for char in self.characters:
            char.set_methods(self.influence_methods)
        #set relationships
        char = self.characters[0]
        for other in self.characters:
            if char is other:
                pass
            else:
                liking_out = random.random()
                liking_in = random.random()
                dominance = random.random()
                char.set_relation(other.name, Relationship(other, liking_out, liking_in, dominance))
                other.set_relation(char.name, Relationship(char, liking_in, liking_out, 1 - dominance))
            other.set_relation(other.name, Relationship(other, 1, 1, 0.5))


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

    def get_object_by_name(self, name):
        locs = [loc.name for loc in self.locations]
        if name in locs:
            return self.locations[locs.index(name)]
        objs = [obj.name for obj in self.objects]
        if name in objs:
            return self.objects[objs.index(name)]
        chars = [char.name for char in self.characters]
        if name in chars:
            return self.characters[chars.index(name)]
        raise Exception("asked for object named", name)


    def get_object(self, obj):
        """
        Get a specific character's version of an object. Used by calling character.perception
        """
        if type(obj) is Character:
            return self.characters[obj.id]
        if type(obj) is Location:
            return self.locations[obj.id]
        if obj in self.weather_types:
            return self.weather_types[obj.id - 95]
        if obj in self.appraisals:
            return obj
        elif type(obj) is WorldObject:
            return self.objects[obj.id]
        return obj

    def get_opposite(self, obj):
        if type(obj) is Character:
            choices = copy.deepcopy(self.characters)
            choices.pop(obj.id)
        if type(obj) is Location:
            choices = copy.deepcopy(self.locations)
            choices.pop(obj.id)
        if obj in self.weather_types:
            choices = copy.deepcopy(self.weather_types)
            choices.pop(obj.id - 95)
        elif obj in self.appraisals:
            choices = copy.deepcopy(self.appraisals)
            choices.pop(obj.id - 90)
        elif type(obj) is WorldObject:
            choices = copy.deepcopy(self.objects)
            choices.pop(obj.id)
        if type(obj) is Emotion:
            opposite = Emotion(None, 1 - obj.pleasure, 1 - obj.arousal, 1 - obj.dominance)
        else:
            opposite = random.choices(choices)[0]
        return opposite

    def get_opposite_attribute(self, attribute):
        if attribute in self.appraisals:
            value = attribute.id
            if value < 92:
                return WorldObject(APPRAISALS[value - 88], value + 2)
            if value > 92:
                return WorldObject(APPRAISALS[value - 92], value - 2)
            if value == 92 and random.random() > 0.5:
                return WorldObject("great", 94)
            return WorldObject("horrible", 90)
        return self.get_opposite(attribute)


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

    def perception(self, subject, perception, success):
        if not success:
            return
        world_state = copy.deepcopy(subject.perception)
        if perception.obj in self.objects:
            world_state.objects[perception.obj.id].attributes[perception.attribute_name] = perception.end_value
        elif perception.obj in self.characters:
            world_state.characters[perception.obj.id].attributes[perception.attribute_name] = perception.end_value
        elif perception.obj in self.locations:
            world_state.locations[perception.obj.id].attributes[perception.attribute_name] = perception.end_value
        else:
            raise Exception("warning, this shouldn't happen", perception.obj)
        subject.perception = world_state

    def internal(self, subject, emotion):
        self.characters[subject.id].mood.affect(emotion)
