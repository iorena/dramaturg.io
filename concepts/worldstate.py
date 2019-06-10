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
    """

    def goal(self, subject, goal):
        state = copy.deepcopy(self)
        state.characters[goal[0]].attributes.update(goal[1])
        self.characters[subject.id].goals.append(state)

    def action(self, subject, action):
        state = copy.deepcopy(self)
        state.characters[action[0]].attributes.update(action[1])
        self.characters[subject.id].attributes.update(state)

    def perception(self, subject, perception):
        self.characters[subject.id].perception = perception

    def internal(self, subject, emotion):
        self.characters[subject.id].attributes.update({"affect": emotion})
