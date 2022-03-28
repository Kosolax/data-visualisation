from automaton import automaton
from datetime import datetime

class unit:
    number : int
    automatons = []

    def __init__(self, number, automatons):
        self.number = number
        for i in range(len(automatons)):
            self.automatons.append(automaton(**automatons[i]))