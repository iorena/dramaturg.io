from language.style import Style
from concepts.affect.mood import Mood
from concepts.project import Project
from concepts.worldobject import WorldObject

import random, copy

alive = WorldObject("alive", 100)


class Character:
    id_counter = 0
    names = ["Pekka", "Ville", "Kalle", "Maija"]

    def __init__(self, location, name=None):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location, "vitality": alive}
        self.goals = []
        self.stress = 0
        if name is None:
            self.name = self.random_name()
        else:
            self.name = name
        self.perception = None
        self.relations = {}
        self.style = Style(random.random(), random.random(), random.random())
        self.personality = self.random_personality()
        self.mood = Mood(self.personality)
        self.memory = []
        self.world_model = self.init_causal_relations()
        #todo: make this vary by personality
        self.stress_capacity = 1

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

    def set_random_perceptions(self, world_state):
        world_state = copy.deepcopy(world_state)
        #todo: should we check and change only objects that don't have an appraisal yet?
        for obj in world_state.objects:
            obj.attributes["appraisal"] = random.choices(world_state.appraisals)[0]
        for obj in world_state.weather_types:
            obj.attributes["appraisal"] = random.choices(world_state.appraisals)[0]
        for obj in world_state.locations:
            obj.attributes["appraisal"] = random.choices(world_state.appraisals)[0]
        self.perception = world_state

    def set_goal(self, new_goal):
        #todo: arrange by weight?
        for goal in self.goals:
            #todo: refine checking goal conflict, now only works for inheritance object want goal
            if goal.verb == new_goal.verb and goal.subj != new_goal.subj and goal.obj == new_goal.obj:
                self.goals.remove(goal)
                print("removed conflicting goal", goal.subj, goal.verb, goal.obj)
        self.goals.append(new_goal)

    def set_relation(self, other):
        self.relations[other.name] = Mood(self.random_personality())

    def init_causal_relations(self):
        """
        Causal requirements for events. Determines whether a character is surprised by an event
        NOT IN USE, replaced by get_surprise_project
        """
        events = {
            "kuolla": [Project("someone", "tappaa", "self", None, None, 1)]
            }
        return events

    def resolve_goal(self, goal):
        if goal.proj_type not in ["expansion", "surprise"] and goal in self.goals:
            self.goals.remove(goal)

    def resolve_stress(self, project):
        self.set_goal(project)

    def add_memory(self, memory):
        self.memory.append(memory)

    def reset_mood(self):
        self.mood = Mood(self.personality)

    def set_methods(self, methods):
        self.methods = []
        for method in methods:
            self.methods.append(method)

    def add_stress(self, project):
        self.stress += 1
        print(self.stress)
        if self.stress > self.stress_capacity:
            self.resolve_stress(project)
            self.stress = 0
