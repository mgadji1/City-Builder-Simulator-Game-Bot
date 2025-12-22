from ui.building_types import building_types, building_costs
from random import randint

MAP_SIZE = 10
INIT_POPULATION_SIZE = 100
INIT_MONEY_AMOUNT = 200

class City:
    def __init__(self, name):
        self.name = name
        self.population = INIT_POPULATION_SIZE
        self.money = INIT_MONEY_AMOUNT
        self.map = CityMap()

    def build(self, type: str, x: int, y: int) -> str:
        cost = building_costs[type]

        if self.money >= cost:
            self.map.table[x - 1][y - 1].building = Building(type)
            self.money -= cost

            if type == "H": self.population += randint(50, 200)

            return "Success"
        else:
            return "Not enough money"

class Building:
    def __init__(self, type):
        self.type = type
        self.name = building_types[self.type]
        self.cost = building_costs[type]

class CityMap:
    def __init__(self):
        self.table = [[Cell() for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    
    def show_city_map(self) -> str:
        text = ""
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell = self.table[i][j]

                if (cell.building is None):
                    text += "E "
                else:
                    text += f"{cell.building.type} "
                
                if j == MAP_SIZE - 1:
                    text += "\n"
        
        return text

class Cell:
    def __init__(self):
        self.building = None