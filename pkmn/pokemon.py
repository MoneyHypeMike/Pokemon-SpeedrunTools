from math import ceil, floor, sqrt
import movedex
import speciedex

class Pokemon():
    """Defines a pokemon
       
       Initialized variables:
       gen (int): Generation of the pokemon
       species (specie): Species of the pokemon
       gender (str): Gender of the pokemon
       level (int): Current level
       nature (str): Nature of the pokemon
       ability (str): Ability of the pokemon
       item (int): Current hold item
       move1 (move): First move name
       move2 (move): Second move name
       move3 (move): Third move name
       move4 (move): Fourth move name
       iv_hp (int): Individual value of the hit points stat
       iv_atk (int): Individual value of the attack stat
       iv_def (int): Individual value of the defense stat
       iv_spatk (int): Individual value of the special attack stat
       iv_spdef (int): Individual value of the special defense stat
       iv_spd (int): Individual value of the speed stat
       
       Calculated variables:
       stat (list of int): Current stat values
       hp (int): Current hit point value
       exp (int): Current amount of experience
       happiness (int): Current amount of happiness
       
       Variables with a default value:
       ev_hp (int): HP effort value given when defeated
       ev_atk (int): Attack effort value given when defeated
       ev_def (int): Defense effort value given when defeated
       ev_spatk (int): Special attack effort value given when defeated
       ev_spdef (int): Special defense effort value given when defeated
       ev_spd (int): Speed effort value given when defeated
       origin (str): Origin of the pokemon
       status (str): Current status of the pokemon
    """
    def __init__(self, gen, species, gender, level, nature, ability, item,
                 move1, move2, move3, move4, iv_hp, iv_atk, iv_def, iv_spatk, 
                 iv_spdef, iv_spd, ev_hp=0, ev_atk=0, ev_def=0, ev_spatk=0, ev_spdef=0, 
                 ev_spd=0, origin="Trainer", pokerus=False):
        
        self.gen = gen
        self.species = speciedex.all.dex[gen][species]
        self.gender = gender.upper()
        self.level = level
        self.nature = [nature.upper(), 0, 0, 0, 0, 0]
        self.ability = ability.upper()
        self.item = item.upper()
        self.moves = [movedex.all.dex[gen][x] for x in [move1, move2, move3, move4] if x != ""]
        self.iv = [iv_hp, iv_atk, iv_def, iv_spatk, iv_spdef, iv_spd]
        self.stat = [0, 0, 0, 0, 0, 0]
        self.ev = [ev_hp, ev_atk, ev_def, ev_spatk, ev_spdef, ev_spd]
        self.pokerus = pokerus
        self.boost = [0, 0, 0, 0, 0, 0]
        
        self.update_nature()
        self.update_stats()
        
        self.hp = self.stat[0]
        self.exp = self.species.exp_group.table[self.level - 1]
        self.happiness = self.species.base_happiness
        
        self.origin = origin
        self.status = "Normal"
        
    def level_up(self):
        self.level += 1
        self.update_stats()
        
    def rare_candy(self):
        self.level_up()
        self.exp = self.species.exp_group.table[self.level - 1]
    
    def update_level(self):
        current_level = self.level
        current_exp = self.exp
        exp = self.species.exp_group.table
        
        if current_level < 1:
            raise ValueError("Current level is lower than 1")
        elif current_exp >= exp[-1]:
            return 100
        elif current_exp < exp[current_level - 1]:
            raise ValueError("Current experience point value is lower than the amount needed for the current level")
        
        for level in range(current_level - 1, len(exp) - 1):
            if exp[level] <= current_exp < exp[level + 1]:
                actual_level = level + 1
        
        for x in range(actual_level - current_level):
            self.level_up()
    
    def update_nature(self):
        #This array is used to determinate the multiplier for each nature
        #The quotient indicates +nature, the remainder indicates -nature
        #Attack(0), Defense (1), Sp. Atk(3), Sp.Def (4), Speed (5)
        #If the remainder of the index is 0, the nature is neutral
        natures = ["HARDY", "LONELY", "ADAMANT", "NAUGHTY", "BRAVE",
                   "BOLD", "DOCILE", "IMPISH", "LAX", "RELAXED",
                   "MODEST", "MILD", "BASHFUL", "RASH", "QUIET",
                   "CALM", "GENTLE", "CAREFUL", "QUIRKY", "SASSY",
                   "TIMID", "HASTY", "JOLLY", "NAIVE", "SERIOUS"]
        if self.nature[0] in natures:
            index = natures.index(self.nature[0])
            (plus, minus) = divmod(index, 5)
            
            for x in range(1, 6):
                    self.nature[x] = 1
            
            if index % 6 != 0:
                self.nature[plus + 1] = 1.1
                self.nature[minus + 1] = 0.9
    
    def update_item(self, item):
        self.item = item
    
    def remove_item(self):
        self.item = ""
    
    def learn_move(self, move, slot):
        if slot > len(self.moves):
            self.moves.append(move)
        else:
            self.moves[slot - 1] = move
    
    def update_exp(self, amount):
        self.exp += amount
    
    def update_evs(self, ev_yield):
        multiplier = 2 if self.pokerus == True else 1
        
        if sum(self.ev + [multiplier * x for x in ev_yield]) < 511:
            self.ev = [(x + multiplier * y) for (x,y) in zip(self.ev, ev_yield)]
    
    def update_iv(self, stat, n):
        self.iv[stat] = n
        self.update_stats()
    
    def update_stats(self):
        if self.species.gen < 3:
            self.stat[0] = floor((2 * (self.iv[0] + self.species.base_stats[0])
                                  + ceil(sqrt(self.ev[0])) // 4) * self.level
                                  // 100 + self.level + 10)
            
            for x in range(1, 6):
                self.stat[x] = floor((2 * (self.iv[x] + self.species.base_stats[x])
                                      + ceil(sqrt(self.ev[x])) // 4) 
                                      * self.level // 100 + 5)
        else:
            self.stat[0] = floor((2 * self.species.base_stats[0] + self.iv[0] +
                                  self.ev[0] // 4) * self.level // 100 + 
                                  self.level + 10)
            
            
            
            for x in range(1, 6):
                self.stat[x] = floor(((2 * self.species.base_stats[x] + self.iv[x] +
                                       self.ev[x] // 4) * self.level // 100 +
                                       5) * self.nature[x])
    
    def calc_hp_ratio(self):
        return (self.hp * 100 // self.stat[0])