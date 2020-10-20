"""
Class Vegetable - defines a vegetable object
Class Attributes - name,price and unit
"""

class Vegetable:
    def __init__(self,name,price,unit):
        self.vegName = name
        self.vegPrice = price
        self.vegUnit = unit

    def printVegetableDetails(self):
        print('Name'+self.vegName+' Price:'+self.vegPrice+' Unit:'+self.vegUnit)

    def to_dist(self):
        return {
            'שם':self.vegName,
            'מחיר':self.vegPrice,
            'יחידה':self.vegUnit
        }
