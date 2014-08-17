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
def calculate_stat(gen, stat_name, base_stat, level, iv=0, ev=0, nature=1):
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


def calculate_dv(stat_name, base_stat, level, stat_value, stat_exp=0):
    if stat_name == "hp":
        dv_value = [dv for dv in range(16)
                    if stat_value <= (2 * (dv + base_stat) + ceil(sqrt(stat_exp)) // 4) 
                    * level // 100 + level + 10 < stat_value + 1]
        if len(dv_value) > 1:
            return "Minimum DV: {}, maximum DV: {}".format(dv_value[0], dv_value[-1])
        elif len(dv_value) == 1:
            return "Exact DV: {}".format(dv_value)
        else:
            return "No DV can be calculated with the given stat"
    else:
        dv_value = [dv for dv in range(16)
                    if stat_value <= (2 * (dv + base_stat) + ceil(sqrt(stat_exp)) // 4)
                      * level // 100 + 5 < stat_value + 1]
        if len(dv_value) > 1:
            return "Minimum DV: {}, maximum DV: {}".format(dv_value[0], dv_value[-1])
        elif len(dv_value) == 1:
            return "Exact DV: {}".format(dv_value)
        else:
            return "No DV can be calculated with the given stat"


def calculate_iv(stat_name, base_stat, level, stat_value, ev=0, nature=1):
    if stat_name == "hp":
        iv_value = [iv for iv in range(32)
                    if stat_value <= (2 * base_stat + iv + ev // 4)
                        * level // 100 + level + 10 < stat_value + 1]
        if len(iv_value) > 1:
            return "Minimum IV: {}, maximum IV: {}".format(iv_value[0], iv_value[-1])
        elif len(dv_value) == 1:
            return "Exact IV: {}".format(iv_value)
        else:
            return "No IV can be calculated with the given stat"
    else:
        iv_value = [iv for iv in range(32)
                    if stat_value <= ((2 * base_stat + iv + ev // 4)
                      * level // 100 + 5) * nature < stat_value + 1]
        if len(iv_value) > 1:
            return "Minimum IV: {}, maximum IV: {}".format(iv_value[0], iv_value[-1])
        elif len(iv_value) == 1:
            return "Exact IV: {}".format(iv_value)
        else:
            return "No IV can be calculated with the given stat"


#Formula taken from Bulbapedia 
#http://bulbapedia.bulbagarden.net/wiki/Exp
#Parameters ignored from the formula:
#- Stuff for gen 6
#- Exp. All and Exp. Share
#- Pass Power
def calculate_exp(wild_pkmn, exp_yield, hold_item, fainted_level, pkmn_origin):
    pkmn_owner = 1.5 if pkmn_origin == True else 1
    hold_item = 1.5 if hold_item == "Lucky Egg" else 1
    
    if gen == 5:
        pass
    else:
        pass #exp = pkmn_owner * 