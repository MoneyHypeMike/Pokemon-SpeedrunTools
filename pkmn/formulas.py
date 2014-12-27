from math import ceil, floor, sqrt
import typedex

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

# Formulas taken from http://www.upokecenter.com
def calc_exp(gen, loser_level, exp_yield, trainer_battle = True, num_poke = 1, winner_level=0, hold_item = None, orig_trainer = True):
    """Calculates the experience points gained"""
    
    trainer_battle = 1.5 if trainer_battle == True else 1
    hold_item = 1.5 if hold_item == "LUCKY EGG" else 1
    orig_trainer = 1 if orig_trainer == True else 1.5
    
    if gen < 3:
        return floor((loser_level * (exp_yield // num_poke) // 7)
                      * trainer_battle * orig_trainer * hold_item)
    elif 2 < gen < 5:
        return floor((max(1,(exp_yield * loser_level // 7) // num_poke))
                       * trainer_battle * orig_trainer * hold_item)
    else:
        A = loser_level * 2 + 10
        B = exp_yield * loser_level // 5 * trainer_battle // num_poke
        C = loser_level + winner_level + 10
        exp = floor(floor(floor(floor(sqrt(A) * (A * A)) * B)) / floor(sqrt(C) * (C * C))) + 1
        return floor(exp * hold_item)

def calc_damage(atk_pkmn, def_pkmn, move, atk_mod=0, def_mod=0, crit=False, weather=[],
                screen=set(), battle_type="SINGLE", location="BUILDING"):
    """Calculates the damage range for a move"""
    
    type1, type2 = move.type.type_multi(def_pkmn.species.types)
    
    if 0 in (type1, type2):
        return [[0]]
    
    bp = base_power(atk_pkmn, def_pkmn, move, weather)
    atk = atk_stat(atk_pkmn, move, crit, weather, atk_mod)
    de = def_stat(def_pkmn, move, crit, weather, def_mod)
    mod_1 = mod1(atk_pkmn, move, weather, crit, screen, battle_type)
    mod_2 = mod2(atk_pkmn, move)
    mod_3 = mod3(atk_pkmn, def_pkmn, move, type1 * type2)
    damage = []
    
    if crit == True and atk_pkmn.ability == "SNIPER":
        ch = 3
    elif crit == True:
        ch = 2
    else:
        ch = 1
    
    if move.type.name in [x.name for x in atk_pkmn.species.types] and atk_pkmn.ability == "ADAPTABILITY":
        stab = 2
    elif move.type.name in [x.name for x in atk_pkmn.species.types]:
        stab = 1.5
    else:
        stab = 1
    
    for y in range(len(bp)):
        dmg_range = []
        for r in range(85, 101):
            dmg = floor(floor(floor(floor((floor(((floor(((((atk_pkmn.level * 2 // 5) + 2) * bp[y] * atk // 50) // de) * mod_1) + 2) * ch) * mod_2) * r // 100) * stab) * type1) * type2) * mod_3)
            dmg_range.append(dmg) if dmg > 0 else dmg_range.append(1)
        damage.append(dmg_range)
    return damage

# http://www.smogon.com/dp/articles/damage_formula#modifiers
def base_power(atk_pkmn, def_pkmn, move, weather):
    """Calculates the Base Power (damage formula)"""

    hh = 1
    it = bp_item_multi(atk_pkmn, move)
    chg = 1
    ms = 1
    ws = 1
    
    bp = move_bp(atk_pkmn, def_pkmn, move, weather)
    ua = bp_atk_multi(atk_pkmn, def_pkmn, move)
    fa = bp_def_multi(def_pkmn, move.type.name)
        
    return [floor(hh * bp_value * it * chg * ms * ws * ua * fa) for bp_value in bp]

# http://www.smogon.com/dp/articles/damage_formula#attack
def atk_stat(atk_pkmn, move, crit, weather, mod):
    """Calculates the atk stat (damage formula)"""

    if move.category == "PHYSICAL":
        stat = atk_pkmn.stat[1]
        sm = stat_mod_multi(mod, crit, True)
    elif move.category == "SPECIAL":
        stat = atk_pkmn.stat[3]
        sm = stat_mod_multi(mod, crit, True)
    im = atk_item_multi(atk_pkmn, move)
    am = atk_ability_multi(atk_pkmn, move, weather)
    
    return floor(stat * sm * am * im)

# http://www.smogon.com/dp/articles/damage_formula#defense
def def_stat(def_pkmn, move, crit, weather, mod):
    """Returns the def stat (damage formula)"""
    
    if move.category == "PHYSICAL":
        stat = def_pkmn.stat[2]
        sm = stat_mod_multi(mod, crit, False)
    elif move.category == "SPECIAL":
        stat = def_pkmn.stat[4]
        sm = stat_mod_multi(mod, crit, False)
    
    sx = 0.5 if move.name in ["SELFDESTRUCT", "EXPLOSION"] else 1
    mod = def_mod(def_pkmn, move, weather)
    
    return floor(stat * sm * sx * mod)

def mod1(atk_pkmn, move, weather, crit, screen, battle_type):
    """Returns the first modifier (damage formula)"""
    
    multi_target = ["SURF", "BUBBLE", "ROCK SLIDE"]
    move_category = move.category
    move_type = move.type.name
    ability = atk_pkmn.status
    
    if atk_pkmn.status == "BRN" and move_category == "PHYSICAL" and ability != "GUTS":
        brn = 0.5
    else:
        brn = 1
    
    if crit == True:
        rl = 1
    elif move_category == "PHYSICAL" and "REFLECT" in screen:
        if battle_type == "SINGLE":
            rl = 0.5
        elif battle_type == "DOUBLE":
            rl = 2/3
    elif move_category == "SPECIAL" and "LIGHT SCREEN" in screen:
        if battle_type == "SINGLE":
            rl = 0.5
        elif battle_type == "DOUBLE":
            rl = 2/3
    else:
        rl = 1
        
    if battle_type == "DOUBLE" and move.name in multi_target:
        tvt = 0.75
    else:
        tvt = 1
    
    if weather == "SUNNY DAY" and move_type == "FIRE":
        sr = 1.5
    elif weather == "RAIN DANCE" and move_type == "WATER":
        sr = 1.5
    elif weather == "SUNNY DAY" and move_type == "WATER":
        sr = 0.5
    elif weather == "RAIN DANCE" and move_type == "FIRE":
        sr = 0.5
    else:
        sr = 1
        
    if ability == "FLASH FIRE" and move_type == "FIRE":
        raise NotImplementedError
    else:
        ff = 1
    
    return (brn * rl * tvt * sr * ff)
    
# http://www.smogon.com/dp/articles/damage_formula#mod2
def mod2(atk_pkmn, move):
    """Returns the second modifier (damage formula)"""
    item = atk_pkmn.item
    
    if item == "LIFE ORB":
        return 1.3
    elif item == "METRONOME":
        raise NotImplementedError
    elif move.name == "ME FIRST":
        raise NotImplementedError
    else:
        return 1

# http://www.smogon.com/dp/articles/damage_formula#mod3
def mod3(atk_pkmn, def_pkmn, move, type_multiplier):
    """Returns the third modifier (damage formula)"""
    
    ability = def_pkmn.ability
    atk_item = atk_pkmn.item
    def_item = def_pkmn.item
    
    if ability in ["SOLID ROCK", "FILTER"] and type_multiplier > 1:
        srf = 0.75
    else:
        srf = 1
        
    if atk_item == "EXPERT BELT" and type_multiplier > 1:
        rb = 1.2
    else:
        rb = 1
    
    if atk_item == "TINTED LENS" and type_multiplier < 1:
        tl = 2
    else:
        tl = 1
    
    if mod3_berries(def_item, move.type.name, type_multiplier):
        trb = 0.5
    elif def_item == "CHILIAN BERRY" and type_multiplier > 1:
        trb = 0.5
    else:
        trb = 1
        
    return (srf * rb * tl * trb)

# http://veekun.com/dex/items/berries
def mod3_berries(item, type, multiplier):
    """Returns true if the move is super effective and match berry type"""
    
    if item == "BABIRI BERRY" and type == "STEEL" and multiplier > 1:
        return True
    elif item == "CHARTI BERRY" and type == "ROCK" and multiplier > 1:
        return True
    elif item == "CHOPLE BERRY" and type == "FIGHTING" and multiplier > 1:
        return True
    elif item == "COBA BERRY" and type == "FLYING" and multiplier > 1:
        return True
    elif item == "COLBUR BERRY" and type == "DARK" and multiplier > 1:
        return True
    elif item == "HABAN BERRY" and type == "DRAGON" and multiplier > 1:
        return True
    elif item == "KASIB BERRY" and type == "GHOST" and multiplier > 1:
        return True
    elif item == "KEBIA BERRY" and type == "POISON" and multiplier > 1:
        return True
    elif item == "OCCA BERRY" and type == "FIRE" and multiplier > 1:
        return True
    elif item == "PASSHO BERRY" and type == "WATER" and multiplier > 1:
        return True
    elif item == "PAYAPA BERRY" and type == "PSYCHIC" and multiplier > 1:
        return True
    elif item == "RINDO BERRY" and type == "GRASS" and multiplier > 1:
        return True
    elif item == "SHUCA BERRY" and type == "GROUND" and multiplier > 1:
        return True
    elif item == "TANGA BERRY" and type == "BUG" and multiplier > 1:
        return True
    elif item == "WACAN BERRY" and type == "ELECTRIC" and multiplier > 1:
        return True
    elif item == "YACHE BERRY" and type == "ICE" and multiplier > 1:
        return True
    else:
        return False

def def_mod(def_pkmn, move, weather):
    """Returns the def modifier (def_stat)"""
    
    move_category = move.category
    name = def_pkmn.species.name
    item = def_pkmn.item
    ability = def_pkmn.ability
    status = ["PRZ", "PSN", "BRN", "SLP"]
    
    if move_category == "PHYSICAL":
        if item == "METAL POWDER" and name == "DITTO":
            raise NotImplementedError
        elif ability == "MARVEL SCALE" and def_pkmn.status in status:
            return 1.5
        else:
            return 1
    elif move_category == "SPECIAL":
        if weather == "SANDSTORM" and "ROCK" in [x.name for x in def_pkmn.species.types]:
            return 1.5
        elif item == "SOUL DEW" and name in ["LATIOS", "LATIAS"]:
            return 1.5
        elif item == "METAL POWDER" and name == "DITTO":
            raise NotImplementedError
        elif item == "DEEPSEATOOTH" and name == "CLAMPERL":
            return 2
        elif ability == "FLOWER GIFT" and weather == "SUNNY DAY":
            return 1.5
        else:
            return 1
 
# Missing unaware and simple
# http://www.smogon.com/dp/articles/damage_formula#atk_stat
def stat_mod_multi(mod, crit, atk):
    """Calculates the stat modifier multiplier (atk_stat/def_stat)"""
    
    if mod == 0:
        return 1
    elif mod < 0:
        if crit and atk:
            return 1
        else:
            return (2 / (2 - mod))
    elif mod > 0:
        if crit and atk == False:
            return 1
        else:
            return ((2 + mod) / 2)

# http://www.smogon.com/dp/articles/damage_formula#atk_abilities
def atk_ability_multi(atk_pkmn, move, weather):
    """Calculates the ability multiplier (atk_stat)"""
    
    ability = atk_pkmn.ability
    move_category = move.category
    status = ["PRZ", "PSN", "BRN", "SLP"]
    
    if move_category == "PHYSICAL":
        if ability in ["PURE POWER", "HUGE POWER"]:
            return 2
        elif ability == "FLOWER GIFT" and weather == "SUNNY DAY":
            return 1.5
        elif ability == "GUTS" and atk_pkmn.status in status:
            return 1.5
        elif ability == "HUSTLE":
            move.accuracy -= 20
            return 1.5
        elif ability == "SLOW START":
            raise NotImplementedError
        else:
            return 1
    elif move_category == "SPECIAL":
        if ability == "PLUS":
            raise NotImplementedError
        elif ability == "MINUS":
            raise NotImplementedError
        elif ability == "SOLAR POWER":
            raise NotImplementedError
        else:
            return 1

# http://www.smogon.com/dp/articles/damage_formula#atk_items
def atk_item_multi(atk_pkmn, move):
    """Calculates the item multiplier (atk_stat)"""
    
    item = atk_pkmn.item
    name = atk_pkmn.species.name
    move_category = move.category
    
    if move_category == "PHYSICAL":
        if item == "CHOICE BAND":
            return 1.5
        elif item == "LIGHT BALL" and name == "PIKACHU":
            return 2
        elif item == "THICK CLUB" and name in ["CUBONE", "MAROWAK"]:
            return 2
        else:
            return 1
    elif move_category == "SPECIAL":
        if item == "CHOICE SPECS":
            return 1.5
        elif item == "LIGHT BALL" and name == "PIKACHU":
            return 2
        elif item == "SOUL DEW" and name in ["LATIOS", "LATIAS"]:
            return 1.5
        elif item == "DEEPSEATOOTH" and name == "CLAMPERL":
            return 2
        else:
            return 1

# http://www.smogon.com/dp/articles/damage_formula#bp_abilities_user
def bp_atk_multi(atk_pkmn, def_pkmn, move):
    """Returns the attack ability multiplier (base power)"""
   
    ability = atk_pkmn.ability
    move_type = move.type.name
    atk_gender = atk_pkmn.gender
    def_gender = def_pkmn.gender
    hp_ratio = atk_pkmn.calc_hp_ratio()
    if ability == "RIVALRY" and "GENDERLESS" not in {atk_gender, def_gender}:
        if atk_gender == def_gender:
            return 1.25
        else:
            return 0.75
    elif ability == "RECKLESS" and move.recoil == True:
        return 1.2
    elif ability == "IRON FIST" and move.base == "PUNCH":
        return 1.2
    elif ability == "BLAZE" and move_type == "FIRE" and hp_ratio <= 33:
        return 1.5
    elif ability == "OVERGROW" and move_type == "GRASS" and hp_ratio <= 33:
        return 1.5
    elif ability == "TORRENT" and move_type == "WATER" and hp_ratio <= 33:
        return 1.5
    elif ability == "SWARM" and move_type == "BUG" and hp_ratio <= 33:
        return 1.5
    elif ability == "TECHNICIAN" and move.power <= 60:
        return 1.5
    else:
        return 1

# http://www.smogon.com/dp/articles/damage_formula#bp_abilities_foe
def bp_def_multi(ability, type):
    """Returns the defense ability multiplier (base power)"""
    
    if ability == "THICK FAT" and type in ["ICE", "FIRE"]:
        return 0.5
    elif ability == "HEATPROOF" and type == "FIRE":
        return 0.5
    elif ability == "DRY SKIN" and type == "FIRE":
        return 1.25
    else:
        return 1

# http://bulbapedia.bulbagarden.net/wiki/Timespace_orbs
# http://bulbapedia.bulbagarden.net/wiki/Type-enhancing_item
# http://www.smogon.com/dp/articles/damage_formula#bp_items
def bp_item_multi(atk_pkmn, move):
    """Calculates the item multiplier (base power)"""
    
    category = move.category
    move_type = move.type.name
    pkmn_name = atk_pkmn.species.name
    item = atk_pkmn.item
    
    if item == "MUSCLE BAND" and category == "PHYSICAL":
        return 1.1
    elif item == "WISE GLASSES" and category == "SPECIAL":
        return 1.1
    elif plates(item, move_type):
        return 1.2
    elif incenses(item, move_type):
        return 1.2
    elif gems(item, move_type):
        return 1.5
    elif enhancing(item, move_type):
        return 1.1
    elif item == "PINK BOW" and move_type == "NORMAL":
        return 1.1
    elif item == "POLKADOT BOW" and move_name == "NORMAL":
        return 1.125
    elif item == "ADAMANT ORB" and pkmn.name == "DIALGA" and (move_type == "STEEL" or move_type == "DRAGON"):
        return 1.2
    elif item == "LUSTROUS ORB" and pkmn.name == "PALKIA" and (move_type == "WATER" or move_type == "DRAGON"):
        return 1.2
    elif item == "GRISEOUS ORB" and pkmn.name == "GIRATINA" and (move_type == "GHOST" or move_type == "DRAGON"):
        return 1.2
    else:
        return 1

# http://bulbapedia.bulbagarden.net/wiki/Plate
def plates(item, move_type):
    """Returns true if the item and move match the plate (bp_item_multi)"""
    
    if item == "DRACO PLATE" and move_type == "DRAGON":
        return True
    elif item == "DREAD PLATE" and move_type == "DARK":
        return True
    elif item == "EARTH PLATE" and move_type == "GROUND":
        return True
    elif item == "FIST PLATE" and move_type == "FIGHTING":
        return True
    elif item == "FLAME PLATE" and move_type == "FIRE":
        return True
    elif item == "ICICLE PLATE" and move_type == "ICE":
        return True
    elif item == "INSECT PLATE" and move_type == "BUG":
        return True
    elif item == "IRON PLATE" and move_type == "STEEL":
        return True
    elif item == "MEADOW PLATE" and move_type == "GRASS":
        return True
    elif item == "MIND PLATE" and move_type == "PSYCHIC":
        return True
    elif item == "SKY PLATE" and move_type == "FLYING":
        return True
    elif item == "SPLASH PLATE" and move_type == "WATER":
        return True
    elif item == "SPOOKY PLATE" and move_type == "GHOST":
        return True
    elif item == "STONE PLATE" and move_type == "ROCK":
        return True
    elif item == "TOXIC PLATE" and move_type == "POISON":
        return True
    elif item == "ZAP PLATE" and move_type == "ELECTRIC":
        return True
    else:
        return False

# http://bulbapedia.bulbagarden.net/wiki/Incense
def incenses(item, move_type):
    """Returns true if the item and move match the incense (bp_item_multi)"""
    
    if item == "ODD INCENSE" and move_type == "PSYCHIC":
        return True
    if item == "ROCK INCENSE" and move_type == "ROCK":
        return True
    if item == "ROSE INCENSE" and move_type == "GRASS":
        return True
    if item == "SEA INCENSE" and move_type == "WATER":
        return True
    if item == "WAVE INCENSE" and move_type == "WATER":
        return True
    else:
        return False

# http://bulbapedia.bulbagarden.net/wiki/Gem
def gems(item, move_type):
    """Returns true if the item and move match the gem (bp_item_multi)"""
    
    if item == "FIRE GEM" and move_type == "FIRE":
        return True
    elif item == "WATER GEM" and move_type == "WATER":
        return True
    elif item == "ELECTRIC GEM" and move_type == "ELECTRIC":
        return True
    elif item == "GRASS GEM" and move_type == "GRASS":
        return True
    elif item == "ICE GEM" and move_type == "ICE":
        return True
    elif item == "FIGHTING GEM" and move_type == "FIGHTING":
        return True
    elif item == "POISON GEM" and move_type == "POISON":
        return True
    elif item == "GROUND GEM" and move_type == "GROUND":
        return True
    elif item == "FLYING GEM" and move_type == "FLYING":
        return True
    elif item == "PSYCHIC GEM" and move_type == "PSYCHIC":
        return True
    elif item == "BUG GEM" and move_type == "BUG":
        return True
    elif item == "ROCK GEM" and move_type == "ROCK":
        return True
    elif item == "GHOST GEM" and move_type == "GHOST":
        return True
    elif item == "DRAGON GEM" and move_type == "DRAGON":
        return True
    elif item == "DARK GEM" and move_type == "DARK":
        return True
    elif item == "STEEL GEM" and move_type == "STEEL":
        return True
    elif item == "NORMAL GEM" and move_type == "NORMAL":
        return True
    else:
        return False
        
# http://bulbapedia.bulbagarden.net/wiki/Type-enhancing_item
def enhancing(item, move_type):
    """Returns true if the item and move match the item type (bp_item_multi)"""
    
    if item == "BLACK BELT" and move_type == "FIGHTING":
        return True
    elif item == "BLACK GLASSES" and move_type == "DARK":
        return True
    elif item == "CHARCOAL" and move_type == "FIRE":
        return True
    elif item == "DRAGON FANG" and move_type == "DRAGON":
        return True
    elif item == "HARD STONE" and move_type == "ROCK":
        return True
    elif item == "MAGNET" and move_type == "ELECTRIC":
        return True
    elif item == "METAL COAT" and move_type == "STEEL":
        return True
    elif item == "MIRACLE SEED" and move_type == "GRASS":
        return True
    elif item == "MYSTIC WATER" and move_type == "WATER":
        return True
    elif item == "NEVER-MELT ICE" and move_type == "ICE":
        return True
    elif item == "POISON BARB" and move_type == "POISON":
        return True
    elif item == "SHARP BEAK" and move_type == "FLYING":
        return True
    elif item == "SILK SCARF" and move_type == "NORMAL":
        return True
    elif item == "SILVER POWDER" and move_type == "BUG":
        return True
    elif item == "SOFT SAND" and move_type == "GROUND":
        return True
    elif item == "SPELL TAG" and move_type == "GHOST":
        return True
    elif item == "TWISTED SPOON" and move_type == "PSYCHIC":
        return True
    else:
        return False

# Hidden Power: # http://www.upokecenter.com/dex/?lang=en&move=237
# http://www.smogon.com/dp/articles/damage_formula#bp_variable
# Maximum values for Assurance, Avalanche, Fury Cutter, 
# Missing Fling, Natural Gift, Nature Power, Triple Kick, Weather Ball
def move_bp(atk_pkmn, def_pkmn, move, weather):
    """Returns the move base power (base power)"""
    
    atk_hp = atk_pkmn.hp
    atk_hp_ratio = atk_pkmn.calc_hp_ratio()
    weight = def_pkmn.species.weight
    move_name = move.name
    move_power = move.power
    
    if move_name == "ASSURANCE":
        return [move_power, move_power * 2]
    elif move_name == "AVALANCHE":
        return [move_power, move_power * 2]
    elif move_name == "BRINE":
        return [move_power, move_power * 2]
    elif move_name in ["CRUSH GRIP", "WRING OUT"]:
        return [1 + (120 * def_pkmn.hp // def_pkmn.stat[0])]
    elif move_name in ["ERUPTION", "WATER SPOUT"]:
        return [(150 * atk_hp // atk_pkmn.stat[0])]
    elif move_name == "FACADE":
        return [move_power, move_power * 2]
    elif move_name in ["FLAIL", "REVERSAL"]:
        return [20, 40, 80, 100, 150, 200]
    elif move_name == "FLING":
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 130]
    elif move_name == "FRUSTRATION":
        return max([1], [102 - (atk_pkmn.happiness * 2 // 5)])
    elif move_name == "FURY CUTTER":
        return [10, 20, 40, 80, 160]
    elif move_name in ["GRASS KNOT", "LOW KICK"]:
        if 0 < weight <= 10:
            return [20]
        elif 10 < weight <= 25:
            return [40]
        elif 25 < weight <= 50:
            return [60]
        elif 50 < weight <= 101:
            return [80]
        elif 100 < weight <= 200:
            return [100]
        else:
            return [120]
    elif move_name == "GYRO BALL":
        return min([150], 1 + (25 * def_pkmn.stat[5] // atk_pkmn.stat[5]))
    elif move_name in ["ICE BALL", "ROLLOUT"]:
        return [30, 60, 120, 240, 480, 960]
    elif move_name == "HIDDEN POWER":
        type = ("Fighting", "Flying", "Poison", "Ground", "Rock", "Bug",
                "Ghost", "Steel", "Fire", "Water", "Grass", "Electric",
                "Psychic", "Ice", "Dragon", "Dark")
        
        if atk_pkmn.species.gen == 2:
            var_a = 8 if atk_pkmn.iv[1] >= 8 else 0
            var_a += 4 if atk_pkmn.iv[2] >= 8 else 0
            var_a += 1 if atk_pkmn.iv[3] >= 8 else 0
            var_a += 2 if atk_pkmn.iv[5] >= 8 else 0
            
            bp = ((var_a * 5 + (atk_pkmn.iv[3] % 4)) / 2) + 31
            type_num = 4 * (atk_pkmn.stat[1] % 4) + (atk_pkmn.stat[2] % 4)
            move.type = typedex.all.dex[atk_pkmn.species.gen][type[type_num].upper()]
        else:
            var_x1 = 0 if (atk_pkmn.iv[0] // 2 % 2) == 0 else 1
            var_x1 += 0 if (atk_pkmn.iv[1] // 2 % 2) == 0 else 2
            var_x1 += 0 if (atk_pkmn.iv[2] // 2 % 2) == 0 else 4
            var_x1 += 0 if (atk_pkmn.iv[3] // 2 % 2) == 0 else 16
            var_x1 += 0 if (atk_pkmn.iv[4] // 2 % 2) == 0 else 32
            var_x1 += 0 if (atk_pkmn.iv[5] // 2 % 2) == 0 else 8
            bp = (var_x1 * 40 // 63) + 30
            
            var_x2 = 0 if (atk_pkmn.iv[0] % 2) == 0 else 1
            var_x2 += 0 if (atk_pkmn.iv[1] % 2) == 0 else 2
            var_x2 += 0 if (atk_pkmn.iv[2] % 2) == 0 else 4
            var_x2 += 0 if (atk_pkmn.iv[3] % 2) == 0 else 16
            var_x2 += 0 if (atk_pkmn.iv[4] % 2) == 0 else 32
            var_x2 += 0 if (atk_pkmn.iv[5] % 2) == 0 else 8
            type_num = (var_x2 * 15 // 63)
            move.type = typedex.all.dex[atk_pkmn.species.gen][type[type_num].upper()]
        return [bp]
    elif move_name == "MAGNITUDE":
        return [10, 30, 50, 70, 90, 110, 130, 150]
    elif move_name == "NATURAL GIFT":
        return [0]
    elif move_name == "NATURE POWER":
        raise NotImplementedError
    elif move_name == "PAYBACK":
        return [move_power, move_power * 2]
    elif move_name == "PRESENT":
        return [40, 80, 120]
    elif move_name == "PUNISHMENT":
        return min([200], [60 + (sum([x for x in atk_pkmn.stat_mod if x > 0]) * 20)])
    elif move_name == "PURSUIT":
        return [move_power, move_power * 2]
    elif move_name == "RETURN":
        return min([1], [atk_pkmn.happiness * 2 // 5])
    elif move_name == "REVENGE":
        return [move_power, move_power * 2]
    elif move_name == "SMELLINGSALT":
        return [move_power, move_power * 2]
    elif move_name == "SPIT UP":
        return [100, 200, 300]
    elif move_name == "STOMP":
        return [move_power, move_power * 2]
    elif move_name == "TRIPLE KICK":
        return [10, 20, 30]
    elif move_name == "TRUMP CARD":
        return [40, 50, 60, 80, 200]
    elif move_name == "WAKE-UP SLAP":
        return [move_power, move_power * 2]
    elif move_name == "WEATHER BALL":
        if weather in ["SUNNY DAY", "RAIN DANCE", "SANDSTORM", "HAIL"]:
            return [100]
        else:
            return [50]
    elif move_name == "SOLARBEAM" and weather in ["RAIN DANCE", "HAIL", "SANDSTORM"]:
        return [60]
    else:
        return [move_power]