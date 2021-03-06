from automaton import automaton
from datetime import datetime
import json

class unit:
    number : int
    generatedTime : []
    automatons = []

    def __init__(self, number, generatedTime):
        automatonTypes = [47648, 47649, 47650, 47651, 47652, 47653, 47654, 47655, 47656, 47657]
        self.number = number
        self.generatedTime = generatedTime
        self.automatons = []
        for i in range(10):
            self.automatons.append(automaton(i+1, automatonTypes[i]))
    
    def json_serial(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if (isinstance(obj, automaton)):
            return json.dumps(obj.__dict__, default=self.json_serial)
        raise TypeError ("Type %s not serializable" % type(obj))

    def generate_json_file(self, nameFile):
        for automaton in self.automatons:
            automaton.generate()

        serialized_object = json.dumps(self.__dict__, default=self.json_serial)
        with open(nameFile, 'w') as outfile:
            json.dump(serialized_object, outfile)