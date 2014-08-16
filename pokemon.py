import species

class Pokemon(species.Species):
    """Defines a pokemon based on a specie
    
        level (int): Current level
        nature (str): Current nature
        ability (str): Current ability
        hp (int): Value of the hit point stat
        atk (int): Value of the attack stat
        def (int): Value of the defense stat
        spatk (int): Value of the special attack stat
        spdef (int): Value of the special defense stat
        spd (int): Value of the speed stat
        iv_hp (int): Individual value of the hit points stat
        iv_atk (int): Individual value of the attack stat
        iv_def (int): Individual value of the defense stat
        iv_spatk (int): Individual value of the special attack stat
        iv_spdef (int): Individual value of the special defense stat
        iv_spd (int): Individual value of the speed stat
    """
    def __init__(self, level, nature, iv_hp, iv_atk, iv_def,
                 iv_spatk, iv_spdef, iv_spd, dex_num, name, type1, type2, ability1, ability2,
                 h_ability, b_hp, b_atk, b_def, b_spatk, b_spdef, b_spd,
                 exp_curve, exp_yield, ev_hp, ev_atk, ev_def, ev_spatk,
                 ev_spdef, ev_spd):
        super().__init__(dex_num, name, type1, type2, ability1, ability2,
                       h_ability, b_hp, b_atk, b_def, b_spatk, b_spdef,
                       b_spd, exp_curve, exp_yield, ev_hp, ev_atk, ev_def,
                       ev_spatk, ev_spdef, ev_spd)
        self.level = level
        self.nature = nature
        self.iv_hp = iv_hp
        self.iv_atk = iv_atk
        self.iv_def = iv_def
        self.iv_spatk = iv_spatk
        self.iv_spdef = iv_spdef
        self.iv_spd = iv_spd

s = species.Species(1, "Bulbasaur", "Grass", "Poison", "Overgrow", "", "Chlorophyll", 
            45, 49, 49, 65, 65, 45, "medium_slow", 64, 0, 0, 0, 0, 1, 0)
p = Pokemon(5, "Quirky", 31,31,31,31,31,31, 1, "Bulbasaur", "Grass", "Poison", "Overgrow", "", "Chlorophyll", 
            45, 49, 49, 65, 65, 45, "medium_slow", 64, 0, 0, 0, 0, 1, 0)