from language.style import Style
from concepts.affect.mood import Mood

import random


class Character:
    id_counter = 0
    names = ["Pekka", "Ville", "Kalle", "Maija"]

    def __init__(self, location):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location}
        self.goals = []
        self.name = self.random_name()
        self.perception = None
        self.relations = {}
        self.style = Style(random.random(), random.random())
        self.personality = self.random_personality()
        self.mood = Mood(self.personality)

    def __str__(self):
        """
        return self.name
        """
        return (f"{{Character{str(self.id)} {self.name}\nlocation: {self.attributes['location']}\n")

    def to_json(self):
        return {
            **self.__dict__
        }

    def __hash__(self):
        return hash(self.name)

    def random_name(self):
        name = random.choices(Character.names)[0]
        Character.names.remove(name)
        return name

    def random_personality(self):
        return {"O": random.uniform(-1, 1), "C": random.uniform(-1, 1), "E": random.uniform(-1, 1), "A": random.uniform(-1, 1), "N": random.uniform(-1, 1)}

    def set_perception(self, world_state):
        print(world_state)
        self.perception = world_state
        #todo: should we check and change only objects that don't have an appraisal yet?
        for obj in world_state.objects:
            obj.attributes["appraisal"] = random.choices(world_state.appraisals)[0]

    def set_goal(self, goal):
        self.goals.append(goal)

    def set_relation(self, other, relation):
        """
        After creating characters, set relations towards each character. For now, one-dimensional value between 0 and 1.
        Todo: factorize relationship into different aspects; closeness, appreciation...?
        """
        self.relations[other.name] = relation
