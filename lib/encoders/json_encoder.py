import json


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        if hasattr(o, '__dict__'):
            return o.__dict__
        else:
            return super(CustomEncoder, self).default(o)
