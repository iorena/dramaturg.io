from concepts.character import Character


class Transition:
    def __init__(self, obj, attribute_name, start_value, end_value):
        self.obj = obj
        self.attribute_name = attribute_name
        self.start_value = start_value
        self.end_value = end_value

    def get_person(self):
        if type(self.obj) is Character:
            return self.obj
        return self.end_value

    def get_object(self):
        if type(self.end_value) is Character:
            return self.obj
        return self.end_value

    def to_json(self):
        return {
            'obj': str(self.obj),
        }

    def __str__(self):
        return f"{self.obj}, {self.attribute_name}, {self.start_value} -> {self.end_value}"
