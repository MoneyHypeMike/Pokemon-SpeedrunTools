class Species:
    """Defines a specie of pokemon
       
       dex_num (int): National pokedex number
       name (str): Name of the specie
       types (list of str): Types of the species [type1, type2]
       abilities (list of str): Possible abilities [ab1, ab2, h_ability]
       weight (float): Weight (kg) of the specie
       catch_rate (int): Catch rate of the specie
       happiness (int): Base happiness of the specie
       base_stats (list of int): Base stats [HP, atk, def, spatk, spdef, spd]
       exp_group (str): Experience group name of the specie
       base_exp (int): Experience yield. For gen 5 --> [bw_value, b2w2_value]
       ev_yield (list of int):  EV gained [HP, atk, def, spatk, spdef, spd]
       gen: Generation of the specie
    """
    def __init__(self, dex_num, name, types, abilities, weight, catch_rate,
                 happiness, base_stats, exp_group, base_exp, ev_yield, gen):
        self.dex_num = dex_num
        self.name = name
        self.types = types
        self.abilities = abilities
        self.weight = weight
        self.catch_rate = catch_rate
        self.happiness = happiness
        self.base_stats = base_stats
        self.exp_group = exp_group
        self.base_exp = base_exp
        self.ev_yield = ev_yield
        self.gen = gen
    
    def __str__(self):
        """Returns a paragraph describing the specie."""
        
        if self.types[0] in ["Ice", "Electric"]:
            type = "an {}".format("/".join(self.types).lower())
        else:
            type = "a {}".format("/".join(self.types).lower())
        
        group = self.exp_group.lower()
        
        if self.gen < 3:
            return "In generation {0}, {1} (#{2}) is {3} pokémon with "\
                   "the following base stats: {4[0]} hp, {4[1]} atk, {4[2]} "\
                   "def, {4[3]} spatk, {4[4]} spdef and {4[5]} speed. It "\
                   "has a catch rate of {5}, a base happiness of {6} and "\
                   "a base experience of {7}. It weights {8} kg and is part "\
                   "of the {9} experience group. When it faints, it yields "\
                   "the following stat exp: {10[0]} hp, {10[1]} atk, {10[2]} "\
                   "def, {10[3]} spatk, {10[4]} spdef and {10[5]} speed."\
                   .format(self.gen, self.name, self.dex_num, type,
                           self.base_stats, self.catch_rate, self.happiness, 
                           self.base_exp, self.weight, group, self.ev_yield)
        else:
            if len(self.abilities) == 1:
                ability = "ability is {0}".format(self.abilities[0])
            else:
                ability = "abilities are {0}".format("/".join(self.abilities))
            
            return "In generation {0}, {1} (#{2}) is {3} pokémon with "\
                   "the following base stats: {4[0]} hp, {4[1]} atk, "\
                   "{4[2]} def, {4[3]} spatk, {4[4]} spdef and {4[5]} speed. "\
                   "It {5} and has a catch rate of {6}, a base happiness of "\
                   "{7} with a base experience of {8}. It weights {9} kg and "\
                   "is part of the {10} experience group. When it faints, it "\
                   "yields the following stat exp: {11[0]} hp, {11[1]} atk, "\
                   "{11[2]} def, {11[3]} spatk, {11[4]} spdef and {11[5]} "\
                   "speed".format(self.gen, self.name, self.dex_num, type, 
                                  self.base_stats, ability, self.catch_rate,
                                  self.happiness, self.base_exp, self.weight, 
                                  group, self.ev_yield)