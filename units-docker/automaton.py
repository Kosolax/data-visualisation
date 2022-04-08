from random import randint, uniform
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

    def __init__(self, number, type):
        self.number = number
        self.type = type

    def generate(self):
        self.generate_tank_temperature()
        self.generate_outside_temperature()
        self.generate_milk_weight()
        self.generate_ph()
        self.generate_k()
        self.generate_naci()
        self.generate_salmonel()
        self.generate_ecoli()
        self.generate_listeria()
        self.generatedTime = datetime.utcnow()
    
    def generate_tank_temperature(self):
        self.tankTemperature = round(uniform(2.5, 4.5), 1)

    def generate_outside_temperature(self):
        self.outsideTemperature = round(uniform(8, 14), 1)

    def generate_milk_weight(self):
        self.milkWeight = randint(3512, 4607)

    def generate_ph(self):
        self.ph = round(uniform(6.8, 7.2), 1)

    def generate_k(self):
        self.k = randint(35, 47)

    def generate_naci(self):
        self.naci = round(uniform(1, 1.7), 1)

    def generate_salmonel(self):
        self.salmonel = randint(17, 37)

    def generate_ecoli(self):
        self.ecoli = randint(35, 49)

    def generate_listeria(self):
        self.listeria = randint(28, 54)