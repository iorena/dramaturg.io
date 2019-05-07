from character import Character
from location import Location

import random

class WorldState:
    def __init__(self, old=None):
        if old == None:
            self.initializeStoryWorld()
        else:
            self.locations = old.locations
            self.characters = old.characters

    def initializeStoryWorld(self):
        self.locations = [Location(), Location()]
        self.characters = [Character(self.getRandomLoc()), Character(self.getRandomLoc())]

    def getRandomLoc(self):
        return random.choices(self.locations)[0]

    def __str__(self):
        return "Locations: " + ", ".join(map(str, self.locations)) + "\nCharacters: " + ", ".join(map(str, self.characters))

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
    Functions for executing plot points that change the world state
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

