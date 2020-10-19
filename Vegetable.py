"""
Class Vegetable - defines a vegetable object
"""

class Vegetable:
    def __init__(self,name,price,unit):
        self.vegName = name
        self.vegPrice = price
        self.vegUnit = unit
    def setVegetableName(self,name):
        self.vegName=name
    def set