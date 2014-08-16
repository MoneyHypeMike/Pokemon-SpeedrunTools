class Species:
    """Defines a specie of pokémon
    
       dex_num (int): National pokédex number
       name (str): Name in the national pokédex
       type1 (str): Primary type
       type2 (str): Secondary type
       b_hp (int): Base hit points stat value
       b_atk (int): Base attack stat value
       b_def (int): Base defense stat value
       b_spatk (int): Base special attack stat value
       b_spdef (int): Base special defense stat value
       b_spd (int): Base speed stat value
       exp_curve (str): Experience curve name
       exp_yield (int): Base experience given when defeated
       ev_hp (int): HP effort value given when defeated
       ev_atk (int): Attack effort value given when defeated
       ev_def (int): Defense effort value given when defeated
       ev_spatk (int): Special attack effort value given when defeated
       ev_spdef (int): Special defense effort value given when defeated
       ev_spd (int): Speed effort value given when defeated
    """
    def __init__(self, dex_num, name, type1, type2, ability1, ability2,
                 h_ability, b_hp, b_atk, b_def, b_spatk, b_spdef, b_spd,
                 exp_curve, exp_yield, ev_hp, ev_atk, ev_def, ev_spatk, 
                 ev_spdef, ev_spd):
        self.dex_num = dex_num
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.b_hp = b_hp
        self.b_atk = b_atk
        self.b_def = b_def
        self.b_spatk = b_spatk
        self.b_spdef = b_spdef
        self.b_spd = b_spd
        self.ability1 = ability1
        self.ability2 = ability2
        self.h_ability = h_ability
        self.exp_curve = exp_curve
        self.exp_yield = exp_yield
        self.ev_hp = ev_hp
        self.ev_atk = ev_atk
        self.ev_def = ev_def
        self.ev_spatk = ev_spatk
        self.ev_spdef = ev_spdef
        self.ev_spd = ev_spd

p = Species(1, "Bulbasaur", "Grass", "Poison", "Overgrow", "", "Chlorophyll", 
            45, 49, 49, 65, 65, 45, "medium_slow", 64, 0, 0, 0, 0, 1, 0)