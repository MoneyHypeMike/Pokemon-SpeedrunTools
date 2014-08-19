from species import Species
from moves import Moves
from math import ceil, floor, sqrt

class Pokemon():
    """Defines a pokemon
       
       Initialized variables:
       level (int): Current level
       nature (str): Current nature
       ability (str): Current ability
       item (int): Current hold item
       move1 (move): First move name
       move2 (move): Second move name
       move3 (move): Third move name
       move4 (move): Fourth move name
       exp (int): Total experience gained
       origin (str): Origin (wild, trainer)
       iv_hp (int): Individual value of the hit points stat
       iv_atk (int): Individual value of the attack stat
       iv_def (int): Individual value of the defense stat
       iv_spatk (int): Individual value of the special attack stat
       iv_spdef (int): Individual value of the special defense stat
       iv_spd (int): Individual value of the speed stat
       ev_hp (int): HP effort value given when defeated
       ev_atk (int): Attack effort value given when defeated
       ev_def (int): Defense effort value given when defeated
       ev_spatk (int): Special attack effort value given when defeated
       ev_spdef (int): Special defense effort value given when defeated
       ev_spd (int): Speed effort value given when defeated
       species (species): Specie of the pokemon
       status (str): Status of the pokemon
    """
    def __init__(self, level, nature, ability, item, move1, move2,
                 move3, move4, exp, origin, iv_hp, iv_atk, iv_def,
                 iv_spatk, iv_spdef, iv_spd, ev_hp, ev_atk, ev_def, 
                 ev_spatk, ev_spdef, ev_spd, species, status="Normal"):
        self.level = level
        self.nature = [nature, 0, 0, 0, 0, 0]
        self.ability = ability
        self.item = item
        self.move = {1: move1, 2: move2, 3: move3, 4: move4}
        self.exp = exp
        self.origin = origin
        self.status = status
        self.stat = [0, 0, 0, 0, 0, 0]
        self.iv = [iv_hp, iv_atk, iv_def, iv_spatk, iv_spdef, iv_spd]
        self.ev = [ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_spd]
        self.species = species
        self.calc_nature()
        self.calc_stat(1)
        
    def calc_ev(self, ev_yield):
        """Calculates the amount of ev gained by a pokemon
           
           ev_yield (int + list): ev gained for each stat
        """
        self.ev = [(x + y) for (x,y) in zip(self.ev, ev_yield)]
    
    def calc_stat(self, gen):
        """Calculates the stats of a pokemon
           
           gen (int): Generation of the game
        """
        
        if gen < 3:
            self.stat[0] = floor((2 * (self.iv[0] + self.species.base[0])
                                  + ceil(sqrt(self.ev[0])) // 4) * self.level
                                  // 100 + self.level + 10)
            
            for x in range(1, 6):
                self.stat[x] = floor((2 * (self.iv[x] + self.species.base[x])
                                      + ceil(sqrt(self.ev[x])) // 4) 
                                      * self.level // 100 + 5)
        else:
            self.stat[0] = floor((2 * self.species.base[0] + self.iv[0] +
                                  self.ev[0] // 4) * self.level // 100 + 
                                  self.level + 10)
        
            for x in range(1, 6):
                self.stat[x] = floor(((2 * self.species.base[x] + self.iv[x] +
                                       self.ev[x] // 4) * self.level // 100 +
                                       5) * self.nature[x])
    def calc_nature(self):
        """Calculates the nature multipliers"""
        #This array is used to determinate the multiplier for each nature
        #The quotient indicates +nature, the remainder indicates -nature
        #Attack(0), Defense (1), Sp. Atk(3), Sp.Def (4), Speed (5)
        #If the remainder of the index is 0, the nature is neutral
        natures = ["Hardy", "Lonely", "Adamant", "Naughty", "Brave",
                   "Bold", "Docile", "Impish", "Lax", "Relaxed",
                   "Modest", "Mild", "Bashful", "Rash", "Quiet",
                   "Calm", "Gentle", "Careful", "Quirky", "Sassy",
                   "Timid", "Hasty", "Jolly", "Naive", "Serious"]
        if self.nature[0] in natures:
            index = natures.index(self.nature[0])
            (plus, minus) = divmod(index, 5)
            
            for x in range(1, 6):
                    self.nature[x] = 1
            
            if index % 6 != 0:
                self.nature[plus + 1] = 1.1
                self.nature[minus + 1] = 0.9

#data used for test
m1 = Moves("Hyper Beam", "Physical", "Normal", 150, 5, 90)
m2 = Moves("Water Pulse", "Special", "Water", 60, 20, 100)
m3 = Moves("Rock Blast", "Physical", "Rock", 25, 10, 90)
m4 = Moves("Ice Shard", "Physical", "Ice", 40, 30, 100)

s = Species(1, "Bulbasaur", "Grass", "Poison", "Overgrow", "", "Chlorophyll",
            15.2, 45, 70, 45, 49, 49, 65, 65, 45, "medium_slow", 64, 0, 0, 0, 
            0, 1, 0)
            
p1 = Pokemon(100, "Jolly", "Overgrow", "", m1, m2, m3, m4, "Trainer", 0, 15,
             15, 15, 15, 15, 15, 0, 0, 0, 0, 0, 0, s)
            
p4 = Pokemon(100, "Jolly", "Overgrow", "", m1, m2, m3, m4, "Trainer", 0, 31,
             31, 31, 31, 31, 31, 0, 0, 0, 0, 0, 0, s)