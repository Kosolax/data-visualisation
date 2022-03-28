from automaton import automaton
from datetime import datetime
import json

class unit:
    number : int
    automatons = []

    def __init__(self, number, automatons):
        self.number = number
        for i in range(len(automatons)):
            currentAutomaton = json.loads(automatons[i])
            self.automatons.append(automaton(currentAutomaton["number"], currentAutomaton["type"], currentAutomaton["tankTemperature"], currentAutomaton["outsideTemperature"], currentAutomaton["milkWeight"], currentAutomaton["ph"], currentAutomaton["k"], currentAutomaton["naci"], currentAutomaton["salmonel"], currentAutomaton["ecoli"], currentAutomaton["listeria"], currentAutomaton["generatedTime"]))