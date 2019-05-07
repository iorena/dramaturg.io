from worldstate import WorldState
import location

import random
import copy

class Story:
    def __init__(self):
        self.worldState = WorldState()
        self.initializePossibleTransitions()
        for char in self.worldState.characters:
            char.setPerception(WorldState(self.worldState))
            char.setGoal(self.createGoal())
        self.createPlotPoints()

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
        goalLoc = random.choices(pool)[0]
        goal.characters[0].attributes.update({"location": goalLoc})

        return goal

    def createPlotPoints(self):
        """
        Create a chain of fabula elements with a grammar
        Before executing each plot point, ensure we can make a chain that doesn't go back and forth between the same states
        Ie. this genotype can be evaluated before moving on
        """
        char = random.choices(self.worldState.characters)[0]
        #self.plotpoints = [(char, "acquire goal"), (char, "execute action"), (char, "percieve"), (char, "react")]
        self.plotpoints = [(char, {"location": location.Location(0)}), (char, (char, {"location": location.Location(0)})), (char, WorldState(self.worldState)), (char, "sadness")]
        self.plotpoints.append({"element": "G", "subject": char, "data": {"location": location.Location(0)}})
        self.plotpoints.append({"element": "A", "subject": char, "data": (char, {"location": location.Location(0)})})
        self.plotpoints.append({"element": "P", "subject": char, "data": WorldState(self.worldState)})
        self.plotpoints.append({"element": "IE", "subject": char, "data": "sadness"})

