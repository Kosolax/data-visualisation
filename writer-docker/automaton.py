from datetime import datetime

class automaton :
    number : int
    type : int
    tankTemperature : float
    outsideTemperature : float
    milkWeight : int
    ph : float
    k : int
    naci : float
    salmonel : int
    ecoli : int
    listeria : int
    generatedTime: datetime

    def __init__(self, number, type, tankTemperature, outsideTemperature, milkWeight, ph, k, naci, salmonel, ecoli, listeria, generatedTime):
        self.number = number
        self.type = type
        self.tankTemperature = tankTemperature
        self.outsideTemperature = outsideTemperature
        self.milkWeight = milkWeight
        self.ph = ph
        self.k = k
        self.naci = naci
        self.salmonel = salmonel
        self.ecoli = ecoli
        self.listeria = listeria
        self.generatedTime = generatedTime