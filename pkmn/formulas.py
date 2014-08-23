from math import ceil, floor, sqrt

#Ceil is used instead of floor because of gen1 sqrt algorithm
#from dabomstew:
#set n = 1
#if n*n >= x or n=255 return n
#else increase n and try again

#Formula for gen 1-2 stats calculation taken from RouteOne
#https://github.com/Dabomstew/poke-router
#Formula for gen 3-5 stats calculation taken from Bulbapedia
#http://bulbapedia.bulbagarden.net/wiki/Stat
def calc_stat(gen, stat_name, base_stat, level, iv=0, ev=0, nature=1):
    """Returns the value of the specified stat.
    
    gen: Generation of the Pokémon game.
         Integer between 1-5.
    stat_name: Stat to check
               One of the following 2-3 letter string: 
               att (attack), def (defense), 
               hp (hit point) spa (special attack), 
               spd (special defense), spe (speed)
    base_stat: Base HP stat of the Pokémon.
               Integer between 1 and 255.
    level: Current level of the Pokémon.
           Integer between 1 and 100.
    iv: Current IV of the Pokémon.
        Integer between 0-15 (gen 1-2) or 0-31 (gen 3-5).
    ev: Current HP EV of the Pokémon.
        Integer between 0-65535 (gen 1-2) or 0-255 (gen 3-5).
    nature: Nature multiplier
            One of the follow float: 0.9, 1 and 1.1
    """
    if gen < 3:
        if stat_name == "hp":
            return floor((2 * (iv + base_stat) + ceil(sqrt(ev)) // 4)
                        * level // 100 + level + 10)
        else:
            return floor((2 * (iv + base_stat) + ceil(sqrt(ev)) // 4)
                      * level // 100 + 5)
    else:
        if stat_name == "hp":
            return floor((2 * base_stat + iv + ev // 4)
                        * level // 100 + level + 10)
        else:
            return floor(((2 * base_stat + iv + ev // 4)
                      * level // 100 + 5) * nature)

def calc_dv(stat_name, base_stat, level, stat_value, stat_exp=0):
    """Calculates the DV of a pokemon stat"""
    
    if stat_name == "hp":
        return [dv for dv in range(16)
                    if stat_value <= (2 * (dv + base_stat) + ceil(sqrt(stat_exp)) // 4) 
                    * level // 100 + level + 10 < stat_value + 1]
    else:
        return [dv for dv in range(16)
                    if stat_value <= (2 * (dv + base_stat) + ceil(sqrt(stat_exp)) // 4)
                      * level // 100 + 5 < stat_value + 1]

def calc_iv(stat_name, base_stat, level, stat_value, ev=0, nature=1):
    """Calculates the IV of a pokemon stat"""
    
    if stat_name == "hp":
        return [iv for iv in range(32)
                    if stat_value <= (2 * base_stat + iv + ev // 4)
                        * level // 100 + level + 10 < stat_value + 1]
    else:
        return [iv for iv in range(32)
                    if stat_value <= ((2 * base_stat + iv + ev // 4)
                      * level // 100 + 5) * nature < stat_value + 1]

#Formulas taken from http://www.upokecenter.com - Need to add gen 5
def calc_exp(gen, loser_level, exp_yield, num_poke = 1, trainer_battle = True,
             orig_trainer = True, hold_item = None, winner_level=0):
    """Calculates the experience points gained"""
    
    trainer_battle = 1.5 if trainer_battle == True else 1
    hold_item = 1.5 if hold_item == "Lucky Egg" else 1
    orig_trainer = 1 if orig_trainer == True else 1.5
    
    if gen < 3:
        return floor((loser_level * (exp_yield // num_poke) // 7)
                      * trainer_battle * orig_trainer * hold_item)
    elif 2 < gen < 5:
        return floor((max(1,(exp_yield * loser_level // 7) // num_poke))
                       * trainer_battle * orig_trainer * hold_item)