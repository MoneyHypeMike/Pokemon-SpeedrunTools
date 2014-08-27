from math import floor
import re

class Expgroupdex():
    """Creates a expgroupdex for generation 1 to 5."""
    
    def __init__(self):
        self.dex = dict()
        
        self.create_dex()
    
    def create_dex(self):
        with open(r".\expgroupdex_data\expgroupdex.csv") as f:
            f.readline()
            for lines in f:
                name = lines.strip()
                expgroup = Expgroup(name)
                
                self.dex.update({name: expgroup})

class Expgroup():
    """
       
       Initialized variables:
       name (str): Name of the experience group
       
       Generated variable:
       table (list of int): Amount of exp needed to reach each level
    """
    
    def __init__(self, name):
        self.name = name.upper()
        self.table = [0]
        
        self.generate_table()
       
    def generate_table(self):
        if re.fullmatch("ERRATIC", self.name):
            for level in range(2, 101):
                if level <= 50:
                    self.table.append(((level ** 3) * (100 - level)) // 50)
                elif level <= 68:
                    self.table.append(((level ** 3) * (150 - level)) // 100)
                elif level <= 98:
                    self.table.append(((level ** 3) * ((1911 - 10 * level) // 3)) // 500)
                else:
                    self.table.append(((level ** 3) * (160 - level)) // 100)
        elif re.fullmatch("FAST", self.name):
            for level in range(2, 101):
                self.table.append((4 * (level ** 3)) // 5)
        elif re.fullmatch("MEDIUM_FAST", self.name):
            for level in range(2, 101):
                self.table.append(level ** 3)
        elif re.fullmatch("MEDIUM_SLOW", self.name):
            for level in range(2, 101):
                self.table.append(floor((6 / 5 * (level ** 3)) - (15 * (level ** 2)) + (100 * level) - 140))
        elif re.fullmatch("SLOW", self.name):
            for level in range (2, 101):
                self.table.append(5 * (level ** 3) // 4)
        elif re.fullmatch("FLUCTUATING", self.name):
            for level in range(2, 101):
                if level <= 15:
                    self.table.append(floor((level ** 3) * (((level + 1) // 3) + 24) / 50))
                elif level <= 36:
                    self.table.append(floor((level ** 3) * ((level + 14) / 50)))
                else:
                    self.table.append(floor((level ** 3) * (((level // 2) + 32) / 50)))
        else:
            raise ValueError("Invalid experience group.")

def calc_level(group_name, current_exp, current_level=1):
    exp = Expgroup(group_name).table
    
    if current_level < 1:
        raise ValueError("Current level is lower than 1")
    elif current_exp >= exp[-1]:
        return 100
    elif current_exp < exp[current_level - 1]:
        raise ValueError("Current experience point value is lower than the amount needed for the current level")
    
    for level in range(current_level - 1, len(exp) - 1):
        if exp[level] <= current_exp < exp[level + 1]:
            return level + 1

all = Expgroupdex()