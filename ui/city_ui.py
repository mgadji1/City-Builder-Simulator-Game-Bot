from ui.building_types import building_types

MAP_SIZE = 10
INIT_POPULATION_SIZE = 100
INIT_MONEY_AMOUNT = 1000

class City:
    def __init__(self, name):
        self.name = name
        self.population = INIT_POPULATION_SIZE
        self.money = INIT_MONEY_AMOUNT
        self.map = CityMap()

class Building:
    def __init__(self, type, cost):
        self.type = type
        self.name = building_types[self.type]
        self.cost = cost

class CityMap:
    def __init__(self):
        self.table = [[Cell() for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    
    def show_city_map(self):
        for i in range(MAP_SIZE):
            for j in range(MAP_SIZE):
                cell = self.table[i][j]

                if (cell is None): print("E")
                else: print(Building(Cell(cell).building).type)

class Cell:
    def __init__(self):
        self.building = None