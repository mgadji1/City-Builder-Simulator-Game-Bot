from models.buildings_info import *
from random import randint
import time

MAP_SIZE = 10
INIT_POPULATION_SIZE = 100
INIT_MONEY_AMOUNT = 200.0
INIT_HAPPINESS_LEVEL = 10

NUMBER_OF_SPACES = 2

class City:
    def __init__(self, name):
        self.name = name
        self.population = INIT_POPULATION_SIZE
        self.money = INIT_MONEY_AMOUNT
        self.map = CityMap()
        self.last_update_time = time.time()
        self.happiness = INIT_HAPPINESS_LEVEL

    def is_game_win(self) -> bool:
        return self.happiness >= 100
    
    def is_game_over(self) -> bool:
        return self.happiness < 0 or self.money < 0

    def build(self, type: str, x: int, y: int) -> str:
        cost = building_costs[type]

        if self.money < cost:
            return "Not enough money"

        self.happiness += building_happiness_impact[type]
        self.map.table[x - 1][y - 1].building = Building(type)
        self.money -= cost

        if type == "H":
            self.population += randint(50, 200)

        return "Success"

    
    def earn_money(self):
        now = time.time()
        diff_seconds = now - self.last_update_time

        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell = self.map.table[i][j]

                if cell.building is not None:
                    self.money += building_incomes[cell.building.type] * (diff_seconds / 3600)
        self.last_update_time = now

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
                    text += ("E" + " " * NUMBER_OF_SPACES)
                else:
                    text += (f"{cell.building.type}" + " " * NUMBER_OF_SPACES)
                
                if j == MAP_SIZE - 1:
                    text += "\n" * NUMBER_OF_SPACES
        
        return text

class Cell:
    def __init__(self):
        self.building = None