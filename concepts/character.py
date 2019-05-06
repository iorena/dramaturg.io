import random


class Character:
    def __init__(self, name):
        self.name = name

    def greet(self):
        if random.random() >= 0.5:
            return f"{self.name}: Hi!"
        return f"{self.name}: Hello!"
