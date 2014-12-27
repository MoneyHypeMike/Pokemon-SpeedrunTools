class Typedex():
    """Creates a typedex for generation 1 to 5."""
    
    def __init__(self):
        self.dex = {1: {}, 2: {}, 3: {}, 4:{}, 5:{}}
        
        for x in [1, 2, 3, 4, 5]:
            self.files(x)
        
    def files(self, gen):
        if gen < 2:
            filename = r".\typedex_data\gen1typedex.csv"
        else:
            filename = r".\typedex_data\gen25typedex.csv"
        
        self.create_dex(gen, filename)
    
    def create_dex(self, gen, filename):       
        with open(filename) as f:
            f.readline()
            for lines in f:
                name = lines.strip()
                type = Types(gen, name)
                
                self.dex[gen].update({name: type})

class Types():
    """
       
       Initialized variable:
       gen (int): Generation of the type
       name (str): Name of the type
       
       Generated variables:
       weak (set of str): Types it is weak against (0.5x)
       strong (set of str): Types it is strong against (2x)
       immune (set of str): Types it is immune to (0x)
    """
    
    def __init__(self, gen, name):
        self.gen = gen
        self.name = name.upper()
        
        self.table_multi()
    
    def table_multi(self):
        if self.gen < 2:
            types = ["BUG", "DRAGON", "ELECTRIC", "FIGHTING", "FIRE",
                     "FLYING", "GHOST", "GRASS", "GROUND", "ICE",
                     "NORMAL", "POISON", "PSYCHIC", "ROCK", "WATER"]
            
            try:
                row = types.index(self.name)
            except ValueError:
                raise NotImplementedError
            
            multipliers = [
            [1, 1, 1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 2, 2, 1, 1],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0.5, 0.5, 1, 1, 2, 1, 0.5, 0, 1, 1, 1, 1, 1, 2],
            [0.5, 1, 1, 1, 1, 0.5, 0, 1, 1, 2, 2, 0.5, 0.5, 2, 1],
            [2, 0.5, 1, 1, 0.5, 1, 1, 2, 1, 2, 1, 1, 1, 0.5, 0.5],
            [2, 1, 0.5, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 1],
            [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 0, 1, 1],
            [0, 0, 1, 1, 0, 0, 1, 0, 2, 1, 1, 0, 1, 2, 2],
            [0.5, 1, 2, 1, 2, 0, 1, 0.5, 1, 1, 1, 2, 1, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 2, 2, 0.5, 1, 1, 1, 1, 0.5],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0.5, 1],
            [2, 1, 1, 1, 1, 1, 0.5, 2, 0.5, 1, 1, 0.5, 1, 0.5, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 1],
            [2, 1, 1, 0.5, 2, 2, 1, 1, 0.5, 2, 1, 1, 1, 1, 1],
            [1, 0.5, 1, 1, 2, 1, 1, 0.5, 2, 1, 1, 1, 1, 2, 0.5]]
            
            self.weak = {types[x] for x in range(15) if multipliers[row][x] == 0.5}
            self.strong = {types[x] for x in range(15) if multipliers[row][x] == 2}
            self.immune = {types[x] for x in range(15) if multipliers[row][x] == 0}
        elif self.gen < 6:
            types = ["BUG", "DARK", "DRAGON", "ELECTRIC", "FIGHTING", 
                     "FIRE", "FLYING", "GHOST", "GRASS", "GROUND", "ICE",
                     "NORMAL", "POISON", "PSYCHIC", "ROCK", "STEEL", "WATER"]
            
            try:
                row = types.index(self.name)
            except ValueError:
                raise NotImplementedError
            
            multipliers = [
            [1, 2, 1, 1, 0.5, 0.5, 0.5, 0.5, 2, 1, 1, 1, 0.5, 2, 1, 0.5, 1],
            [1, 0.5, 1, 1, 0.5, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 0.5, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1],
            [1, 1, 0.5, 0.5, 1, 1, 2, 1, 0.5, 0, 1, 1, 1, 1, 1, 1, 2],
            [0.5, 2, 1, 1, 1, 1, 0.5, 0, 1, 1, 2, 2, 0.5, 0.5, 2, 2, 1],
            [2, 1, 0.5, 1, 1, 0.5, 1, 1, 2, 1, 2, 1, 1, 1, 0.5, 2, 0.5],
            [2, 1, 1, 0.5, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0.5, 0.5, 1],
            [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 2, 1, 0.5, 1],
            [0.5, 1, 0.5, 1, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 2],
            [0.5, 1, 1, 2, 1, 2, 0, 1, 0.5, 1, 1, 1, 2, 1, 2, 2, 1],
            [1, 1, 2, 1, 1, 0.5, 2, 1, 2, 2, 0.5, 1, 1, 1, 1, 0.5, 0.5],
            [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0.5, 0.5, 1],
            [1, 1, 1, 1, 1, 1, 1, 0.5, 2, 0.5, 1, 1, 0.5, 1, 0.5, 0, 1],
            [1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1],
            [2, 1, 1, 1, 0.5, 2, 2, 1, 1, 0.5, 2, 1, 1, 1, 1, 0.5, 1],
            [1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 0.5, 0.5],
            [1, 1, 0.5, 1, 1, 2, 1, 1, 0.5, 2, 1, 1, 1, 1, 2, 1, 0.5]]
            
            self.weak = {types[x] for x in range(17) if multipliers[row][x] == 0.5}
            self.strong = {types[x] for x in range(17) if multipliers[row][x] == 2}
            self.immune = {types[x] for x in range(17) if multipliers[row][x] == 0}
    
    def type_multi(self, pkmn_types): 
        """Returns the effectiveness multiplier"""
    
        multipliers = [1, 1]
    
        for x in range(len(pkmn_types)):
            if pkmn_types[x].name in self.weak:
                multipliers[x] = 0.5
            elif pkmn_types[x].name in self.strong:
                multipliers[x] = 2
            elif pkmn_types[x].name in self.immune:
                multipliers[x] = 0
    
        return (multipliers[0], multipliers[1])

all = Typedex()
