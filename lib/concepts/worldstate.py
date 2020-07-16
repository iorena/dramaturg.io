from concepts.character import Character
from concepts.location import Location
from concepts.worldobject import WorldObject
from concepts.affect.emotion import Emotion
from concepts.method import Method

import random
import copy

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]
WEATHER_TYPES = ["sunny", "cloudy", "rainy", "stormy"]


class WorldState:
    def __init__(self, embeddings, personalities, relationships, old=None):
        if old is None:
            self.initialize_story_world(embeddings, personalities, relationships)
        else:
            self.embeddings = embeddings
            self.alive = old.alive
            self.appraisals = old.appraisals
            self.locations = old.locations
            self.characters = old.characters
            self.objects = old.objects
            self.weather = old.weather
            self.weather_types = old.weather_types

    def initialize_story_world(self, embeddings, personalities, relationships):
        self.embeddings = embeddings
        self.alive = WorldObject("alive", 100)
        self.appraisals = [WorldObject("horrible", 90), WorldObject("bad", 91), WorldObject("okay", 92), WorldObject("good", 93), WorldObject("great", 94)]
        self.weather_types = [WorldObject("sunny", 95), WorldObject("cloudy", 96), WorldObject("rainy", 97), WorldObject("stormy", 98)]
        self.locations = [Location(), Location()]
        self.characters = [Character(self.locations[0], personalities[0]), Character(self.locations[1], personalities[1]), Character(self.locations[1], None), Character(self.locations[0], None, self.embeddings.get_relative())]
        self.objects = [WorldObject(self.embeddings.get_inheritance_object())]
        self.inheritance_object = self.objects[0]
        self.dead_relative = self.characters[3]
        for obj in self.objects:
            owner = self.characters[3]
            obj.set_owner(owner)
            obj.set_location(owner.attributes["location"])
        self.weather = WorldObject("sää", 95)
        #set relationships
        for char in self.characters:
            for other_char in self.characters:
                if char == other_char:
                    pass
                char.set_relation(other_char, None)
        self.characters[0].set_relation(self.characters[1], relationships[0])
        self.characters[1].set_relation(self.characters[0], relationships[1])

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

    def create_object(self, name, appraisal):
        new_object = WorldObject(name)
        new_object.set_appraisal(self.appraisals[appraisal])
        self.objects.append(new_object)


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
        #no object found, creating new
        new_object = WorldObject(name)
        self.objects.append(new_object)
        print("length of objects", len(self.objects))
        return new_object

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
        if obj.id == 100:
            return self.alive
        if type(obj) is WorldObject:
            print(obj, obj.id)
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
            opposite = random.choice(choices)
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

