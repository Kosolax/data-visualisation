from automaton import automaton
from datetime import datetime
import json

class unit:
    number : int
    generatedTime : []
    automatons = []

    def __init__(self, number, generatedTime, automatons):
        self.number = number
        self.generatedTime = generatedTime
        for i in range(len(automatons)):
            currentAutomaton = json.loads(automatons[i])
            self.automatons.append(automaton(currentAutomaton["number"], currentAutomaton["type"], currentAutomaton["tankTemperature"], currentAutomaton["outsideTemperature"], currentAutomaton["milkWeight"], currentAutomaton["ph"], currentAutomaton["k"], currentAutomaton["naci"], currentAutomaton["salmonel"], currentAutomaton["ecoli"], currentAutomaton["listeria"], currentAutomaton["generatedTime"]))