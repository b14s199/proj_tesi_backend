import json


class OEE:
    def __init__(self, general, availability, performance, quality):
        self.general = general
        self.availability = availability
        self.performance = performance
        self.quality = quality

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)