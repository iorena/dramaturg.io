from language.style import Style
from concepts.affect.mood import Mood
from concepts.project import Project
from concepts.worldobject import WorldObject

import random, copy

alive = WorldObject("alive", 100)


class Character:
    id_counter = 0
    names = ["Pekka", "Kalle", "Maija"]

    def __init__(self, location, personality=None, name=None):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location, "vitality": alive}
        self.goals = []
        self.stress = 0
        if name is None:
            self.name = Character.names[self.id]
        else:
            self.name = name
        self.perception = None
        self.relations = {}
        self.style = Style(random.random(), random.random(), random.random())
        if personality is None:
            self.personality = self.random_personality()
        else:
            self.personality = personality
        self.mood = Mood(self.personality)
        self.event_memory = []
        # for recognizing repetition
        self.said_memory = []
        self.heard_memory = []
        self.beliefs = []
        self.stress_capacity = 2
        if self.personality["N"] > 0.5:
            self.stress_capacity = 1
        elif self.personality["N"] < -0.5:
            self.stress_capacity = 3

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

        for obj in world_state.objects:
            #some objects have static appraisals
            if "appraisal" not in obj.attributes:
                obj.attributes["appraisal"] = world_state.appraisals[0]
        for obj in world_state.weather_types:
            obj.attributes["appraisal"] = random.choices(world_state.appraisals)[0]
        for obj in world_state.locations:
            obj.attributes["appraisal"] = random.choices(world_state.appraisals)[0]
        self.perception = world_state

    def set_goal(self, new_goal, priority=False):
        #todo: arrange by weight?
        for goal in self.goals:
            #todo: refine checking goal conflict, now only works for inheritance object want goal
            if goal.is_in_conflict_with(new_goal):
                self.goals.remove(goal)
        if new_goal not in self.goals:
            if priority:
                self.goals.insert(0, new_goal)
            else:
                self.goals.append(new_goal)

    def set_relation(self, other, relation):
        if relation is None:
            self.relations[other.name] = Mood(self.random_personality())
        else:
            self.relations[other.name] = relation

    def resolve_goal(self, goal):
        if goal in self.goals:
            self.goals.remove(goal)
        else:
            for old_goal in self.goals:
                if goal.is_in_conflict_with(old_goal):
                    self.goals.remove(old_goal)
                    return

    def resolve_stress(self, project):
        #todo: alternatively change relationship
        self.resolve_goal(project)


    def add_said_memory(self, turn):
        self.said_memory.append(turn)

    def add_heard_memory(self, turn, listener):
        self.heard_memory.append(turn)
        # check repetition
        if len(self.heard_memory) > 2 and self.heard_memory[-1] == self.heard_memory[-2] and self.heard_memory[-2] == self.heard_memory[-3]:
            #self.set_goal(Project.get_repetition_project(self, listener), True)
            self.heard_memory = []

    def reset_turn_memory(self):
        self.heard_memory = []
        self.said_mamory = []

    def add_memory(self, memory):
        self.event_memory.append(memory)

    def has_memory(self, memory):
        if memory in self.event_memory:
            return True
        return False

    def add_belief(self, belief):
        self.beliefs.append(belief)

    def remove_belief(self, belief):
        if belief in self.beliefs:
            self.beliefs.remove(belief)

    def reset_mood(self):
        self.mood = Mood(self.personality)

    def set_methods(self, methods):
        self.methods = []
        for method in methods:
            self.methods.append(method)

    def add_stress(self, project):
        if project.proj_type in ["statement", "proposal"]:
            self.stress += 1
            if self.stress > self.stress_capacity:
                self.resolve_stress(project)
                self.stress = 0
                return True
