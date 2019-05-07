from worldstate import WorldState

import random
import copy

class Story:
    def __init__(self):
        self.worldState = WorldState()
        self.initializePossibleTransitions()
        for char in self.worldState.characters:
            char.setPerception(WorldState(self.worldState))
            char.setGoal(self.createGoal())

    def initializePossibleTransitions(self):
        """
        Creates a list of tuples representing all possible transitions, keeping each transition at random
        """
        transitionSpace = []
        for loc in self.worldState.locations:
            for loc2 in self.worldState.locations:
                if loc != loc2:
                    if random.random() > 0.5:
                        transitionSpace.append((loc, loc2))
        self.possibleTransitions = transitionSpace

    def printPossibleTransitions(self):
        print("Possible transitions:")
        for transition in self.possibleTransitions:
            print(str(transition[0]), "->", str(transition[1]))

    def createGoal(self):
        """
        Tweaks the real world state to create a goal world state for a character
        Yes, right now all characters have goals relating to the first character
        """
        goal = copy.deepcopy(WorldState(self.worldState))
        pool = copy.copy(self.worldState.locations)
        pool.remove(self.worldState.characters[0].attributes["location"])
        goalLoc = random.sample(pool, 1)[0]
        goal.characters[0].attributes.update({"location": goalLoc})

        return goal
