class Species:
    """Defines a specie of pokemon
       
       dex_num (int): National pokedex number
       name (str): Name in the national pokedex
       types (list of str): Types of the species [type1, type2]
       ability (list of str): Possible abilities [ab1, ab2, h_ability]
       weight (float): Weight (lbs)
       catch_rate (int): Catch rate
       happiness (int): Base happiness
       base_stats (list of int): Base stats [HP, atk, def, spatk, spdef, spd]
       exp_curve (str): Experience curve name
       base_exp (int): Experience yield. For gen 5 --> [bw_value, b2w2_value]
       ev_yield (list of int):  EV gained [HP, atk, def, spatk, spdef, spd]
    """
    def __init__(self, dex_num, name, types, abilities, weight, catch_rate, 
                 happiness, base_stats, exp_curve, base_exp, ev_yield):
        self.dex_num = dex_num
        self.name = name
        self.types = types
        self.abilities = abilities
        self.weight = weight
        self.catch_rate = catch_rate
        self.happiness = happiness
        self.base_stats = base_stats
        self.exp_curve = exp_curve
        self.base_exp = base_exp
        self.ev_yield = ev_yield
    
    def __str__(self):
        if len(self.abilities) == 0:
            return "{1} (#{0}) is a {2} pokémon with the following base " \
                   "stats: {3[0]} hp, {3[1]} atk, {3[2]} def, {3[3]} spatk, " \
                   "{3[4]} spdef and {3[5]} speed. It weights {4} lbs, has " \
                   "a catch rate of {5}, a base happiness of {6} and " \
                   "follows the {7} experience curve. When it faints, it " \
                   "yields {8} experience points and the following stat " \
                   "exp: {9[0]} hp, {9[1]} atk, {9[2]} def, {9[3]} " \
                   "spatk, {9[4]} spdef and {9[5]} speed." \
                   .format(self.dex_num,
                           self.name,
                           "/".join(self.types).lower(),
                           self.base_stats,
                           self.weight,
                           self.catch_rate,
                           self.happiness,
                           self.exp_curve.lower(),
                           self.base_exp,
                           self.ev_yield)
        elif len(self.abilities) == 1:
            return "{1} (#{0}) is a {2} pokémon which has the following " \
                   "ability: {3}. It base stats are: {4[0]} hp, " \
                   "{4[1]} atk, {4[2]} def, {4[3]} spatk, {4[4]} spdef and " \
                   "{4[5]} speed. It weights {5} lbs, has a catch rate of {6}, " \
                   "a base happiness of {7} and follows the {8} experience " \
                   "curve. When it faints, it yields {9} experience points and " \
                   "the following effort values: {10[0]} hp, {10[1]} atk, " \
                   "{10[2]} def, {10[3]} spatk, {10[4]} spdef and {10[5]} speed." \
                   .format(self.dex_num,
                           self.name, 
                           "/".join(self.types).lower(),
                           "/".join(self.abilities),
                           self.base_stats,
                           self.weight,
                           self.catch_rate,
                           self.happiness,
                           self.exp_curve.lower(),
                           self.base_exp,
                           self.ev_yield)
        else:
            return "{1} (#{0}) is a {2} pokémon with one of the following " \
                   "abilities: {3}. It base stats are: {4[0]} hp, " \
                   "{4[1]} atk, {4[2]} def, {4[3]} spatk, {4[4]} spdef and " \
                   "{4[5]} speed. It weights {5} lbs, has a catch rate of {6}, " \
                   "a base happiness of {7} and follows the {8} experience " \
                   "curve. When it faints, it yields {9} experience points and " \
                   "the following effort values: {10[0]} hp, {10[1]} atk, " \
                   "{10[2]} def, {10[3]} spatk, {10[4]} spdef and {10[5]} speed." \
                   .format(self.dex_num,
                           self.name, 
                           "/".join(self.types).lower(),
                           "/".join(self.abilities),
                           self.base_stats,
                           self.weight,
                           self.catch_rate,
                           self.happiness,
                           self.exp_curve.lower(),
                           self.base_exp,
                           self.ev_yield)