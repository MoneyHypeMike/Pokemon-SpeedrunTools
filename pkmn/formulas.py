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

# Missing gen 5
# Formulas taken from http://www.upokecenter.com
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

def calc_damage(atk_pkmn, def_pkmn, move, crit=False, weather=None,
                screen=set(), battle_type="Single", location="Building"):
    """Calculates the damage range for a move"""
    
    if move.category not in {"Physical", "Special"}:
        return [0]
    
    bp = base_power(atk_pkmn, def_pkmn, move)
    atk = atk_stat(atk_pkmn, move, crit, weather)
    de = def_stat(def_pkmn, move, crit, weather)
    mod_1 = mod1(atk_pkmn, move, weather, crit, screen, battle_type)
    mod_2 = mod2(atk_pkmn, move)
    type1, type2 = effectiveness(move.type, def_pkmn.species.types)
    mod_3 = mod3(atk_pkmn, def_pkmn, move, type1 * type2)
    damage = []
    
    if crit == True and atk_pkmn.ability == "Sniper":
        ch = 3
    elif crit == True:
        ch = 2
    else:
        ch = 1
    
    if move.type.name in [x.name for x in atk_pkmn.species.types] and atk_pkmn.ability == "Adaptability":
        stab = 2
    elif move.type.name in [x.name for x in atk_pkmn.species.types]:
        stab = 1.5
    else:
        stab = 1
    
    for r in range (85, 101):
        damage += [floor((((((((atk_pkmn.level * 2 // 5) + 2) * bp * atk // 50) // de)\
                 * mod_1) + 2) * ch * mod_2 * r // 100) * stab * type1 * type2 * \
                 mod_3)]
    return damage

# http://www.smogon.com/dp/articles/damage_formula#modifiers
def base_power(atk_pkmn, def_pkmn, move):
    """Calculates the Base Power (damage formula)"""

    hh = 1
    it = bp_item_multi(atk_pkmn, move)
    chg = 1
    ms = 1
    ws = 1
    
    bp = move_bp(atk_pkmn, def_pkmn, move)
    ua = bp_atk_multi(atk_pkmn, def_pkmn, move)
    fa = bp_def_multi(def_pkmn, move.type)
        
    return floor(hh * bp * it * chg * ms * ws * ua * fa)

# http://www.smogon.com/dp/articles/damage_formula#attack
def atk_stat(atk_pkmn, move, crit, weather):
    """Calculates the atk stat (damage formula)"""

    if move.category == "Physical":
        stat = atk_pkmn.stat[1]
        sm = stat_mod_multi(atk_pkmn.stat_mod[1], crit)
    elif move.category == "Special":
        stat = atk_pkmn.stat[3]
        sm = stat_mod_multi(atk_pkmn.stat_mod[3], crit)
    
    im = atk_item_multi(atk_pkmn, move)
    am = atk_ability_multi(atk_pkmn, move, weather)
    
    return floor(stat * sm * am * im)

# http://www.smogon.com/dp/articles/damage_formula#defense
def def_stat(def_pkmn, move, crit, weather):
    """Returns the def stat (damage formula)"""
    
    if move.category == "Physical":
        stat = def_pkmn.stat[2]
        sm = stat_mod_multi(def_pkmn.stat_mod[2], crit)
    elif move.category == "Special":
        stat = def_pkmn.stat[4]
        sm = stat_mod_multi(def_pkmn.stat_mod[4], crit)
    
    sx = 0.5 if move.name in {"Selfdestruct", "Explosion"} else 1
    mod = def_mod(def_pkmn, move, weather)
    
    return floor(stat * sm * sx * mod)

def mod1(atk_pkmn, move, weather, crit, screen, battle_type):
    """Returns the first modifier (damage formula)"""
    
    multi_target = {}
    move_category = move.category
    move_type = move.type
    ability = atk_pkmn.status
    
    if atk_pkmn.status == "Burned" and move_category == "Physical" and \
       ability != "Guts":
        brn = 0.5
    else:
        brn = 1
    
    if crit == True:
        rl = 1
    elif move_category == "Physical" and "Reflect" in screen:
        if battle_type == "Single":
            rl = 0.5
        elif battle_type == "Double":
            rl = 2/3
    elif move_category == "Special" and "Light Screen" in screen:
        if battle_type == "Single":
            rl = 0.5
        elif battle_type == "Double":
            rl = 2/3
    else:
        rl = 1
        
    if battle_type == "Double" and move.target in multi_target:
        tvt = 0.75
    else:
        tvt = 1
    
    if weather == "Sunny Day" and move_type == "Fire":
        sr = 1.5
    elif weather == "Rain Dance" and move_type == "Water":
        sr = 1.5
    elif weather == "Sunny Day" and move_type == "Water":
        sr = 0.5
    elif weather == "Rain Dance" and move_type == "Fire":
        sr = 0.5
    else:
        sr = 1
        
    if ability == "Flash Fire" and move_type == "Fire":
        raise NotImplementedError
    else:
        ff = 1
    
    return (brn * rl * tvt * sr * ff)
    
# http://www.smogon.com/dp/articles/damage_formula#mod2
def mod2(atk_pkmn, move):
    """Returns the second modifier (damage formula)"""
    item = atk_pkmn.item
    
    if item == "Life Orb":
        return 1.3
    elif item == "Metronome":
        raise NotImplementedError
    elif move.name == "Me First":
        raise NotImplementedError
    else:
        return 1

# http://www.smogon.com/dp/articles/damage_formula#mod3
def mod3(atk_pkmn, def_pkmn, move, type_multiplier):
    """Returns the third modifier (damage formula)"""
    
    ability = def_pkmn.ability
    atk_item = atk_pkmn.item
    def_item = def_pkmn.item
    type = move.type
    
    if ability in {"Solid Rock", "Filter"} and type_multiplier > 1:
        srf = 0.75
    else:
        srf = 1
        
    if atk_item == "Expert Belt" and type_multiplier > 1:
        rb = 1.2
    else:
        rb = 1
    
    if atk_item == "Tinted Lens" and type_multiplier < 1:
        tl = 2
    else:
        tl = 1
    
    if mod3_berries(def_item, move.type, type_multiplier):
        trb = 0.5
    elif def_item == "Chilian Berry" and type_multiplier > 1:
        trb = 0.5
    else:
        trb = 1
        
    return (srf * rb * tl * trb)

def effectiveness(move_type, pkmn_type): 
    """Returns the effectiveness multiplier"""
    
    multiplier = [1, 1]
    
    for x in range(len(pkmn_type)):
        if pkmn_type[x].name in move_type.weak:
            multiplier[x] = 0.5
        elif pkmn_type[x].name in move_type.strong:
            multiplier[x] = 2
        elif pkmn_type[x].name in move_type.immune:
            multiplier[x] = 0
        else:
            multiplier[x] = 1
    
    return (multiplier[0], multiplier[1])

# http://veekun.com/dex/items/berries
def mod3_berries(item, type, multiplier):
    """Returns true if the move is super effective and match berry type"""
    
    if item == "Babiri Berry" and type == "Steel" and multiplier > 1:
        return True
    elif item == "Charti Berry" and type == "Rock" and multiplier > 1:
        return True
    elif item == "Chople Berry" and type == "Fighting" and multiplier > 1:
        return True
    elif item == "Coba Berry" and type == "Flying" and multiplier > 1:
        return True
    elif item == "Colbur Berry" and type == "Dark" and multiplier > 1:
        return True
    elif item == "Haban Berry" and type == "Dragon" and multiplier > 1:
        return True
    elif item == "Kasib Berry" and type == "Ghost" and multiplier > 1:
        return True
    elif item == "Kebia Berry" and type == "Poison" and multiplier > 1:
        return True
    elif item == "Occa Berry" and type == "Fire" and multiplier > 1:
        return True
    elif item == "Passho Berry" and type == "Water" and multiplier > 1:
        return True
    elif item == "Payapa Berry" and type == "Psychic" and multiplier > 1:
        return True
    elif item == "Rindo Berry" and type == "Grass" and multiplier > 1:
        return True
    elif item == "Shuca Berry" and type == "Ground" and multiplier > 1:
        return True
    elif item == "Tanga Berry" and type == "Bug" and multiplier > 1:
        return True
    elif item == "Wacan Berry" and type == "Electric" and multiplier > 1:
        return True
    elif item == "Yache Berry" and type == "Ice" and multiplier > 1:
        return True
    else:
        return False

def def_mod(def_pkmn, move, weather):
    """Returns the def modifier (def_stat)"""
    
    move_category = move.category
    name = def_pkmn.species.name
    item = def_pkmn.item
    ability = def_pkmn.ability
    status = {"Paralyzed", "Poisoned", "Burned", "Sleep"}
    
    if move_category == "Physical":
        if item == "Metal Powder" and name == "Ditto":
            raise NotImplementedError
        elif ability == "Marvel Scale" and def_pkmn.status in status:
            return 1.5
        else:
            return 1
    elif move_category == "Special":
        if weather == "Sandstorm" and "Rock" in def_pkmn.type:
            return 1.5
        elif item == "Soul Dew" and name in {"Latios", "Latias"}:
            return 1.5
        elif item == "Metal Powder" and name == "Ditto":
            raise NotImplementedError
        elif item == "Deepseatooth" and name == "Clamperl":
            return 2
        elif ability == "Flower Gift" and weather == "Sunny Day":
            return 1.5
        else:
            return 1
 
# Missing unaware and simple
# http://www.smogon.com/dp/articles/damage_formula#atk_stat
def stat_mod_multi(mod, crit):
    """Calculates the stat modifier multiplier (atk_stat/def_stat)"""
    
    if mod < 0:
        if crit == True:
            return 1
        else:
            return (2 / (2 - mod))
    elif mod > 0:
        return ((2 + mod) / 2)
    elif mod == 0:
        return 1

# http://www.smogon.com/dp/articles/damage_formula#atk_abilities
def atk_ability_multi(atk_pkmn, move, weather):
    """Calculates the ability multiplier (atk_stat)"""
    
    ability = atk_pkmn.ability
    move_category = move.category
    status = {"Paralyzed", "Poisoned", "Burned", "Sleep"}
    
    if move_category == "Physical":
        if ability in {"Pure Power", "Huge Power"}:
            return 2
        elif ability == "Flower Gift" and weather == "Sunny Day":
            return 1.5
        elif ability == "Guts" and pkmn.status in status:
            return 1.5
        elif ability == "Hustle":
            move.accuracy -= 20
            return 1.5
        elif ability == "Slow Start":
            raise NotImplementedError
        else:
            return 1
    elif move_category == "Special":
        if ability == "Plus":
            raise NotImplementedError
        elif ability == "Minus":
            raise NotImplementedError
        elif ability == "Solar Power":
            raise NotImplementedError
        else:
            return 1

# http://www.smogon.com/dp/articles/damage_formula#atk_items
def atk_item_multi(atk_pkmn, move):
    """Calculates the item multiplier (atk_stat)"""
    
    item = atk_pkmn.item
    name = atk_pkmn.species.name
    move_category = move.category
    
    if move_category == "Physical":
        if item == "Choice Band":
            return 1.5
        elif item == "Light Ball" and name == "Pikachu":
            return 2
        elif item == "Thick Club" and name in {"Cubone", "Marowak"}:
            return 2
        else:
            return 1
    elif move_category == "Special":
        if item == "Choice Specs":
            return 1.5
        elif item == "Light Ball" and name == "Pikachu":
            return 2
        elif item == "Soul Dew" and name in {"Latios", "Latias"}:
            return 1.5
        elif item == "Deepseatooth" and name == "Clamperl":
            return 2
        else:
            return 1

# http://www.smogon.com/dp/articles/damage_formula#bp_abilities_user
def bp_atk_multi(atk_pkmn, def_pkmn, move):
    """Returns the attack ability multiplier (base power)"""
   
    ability = atk_pkmn.ability
    move_type = move.type
    atk_gender = atk_pkmn.gender
    def_gender = def_pkmn.gender
    hp_ratio = atk_pkmn.calc_hp_ratio()
    
    if ability == "Rivalry" and "genderless" not in {atk_gender, def_gender}:
        if atk_gender == def_gender:
            return 1.25
        else:
            return 0.75
    elif ability == "Reckless" and move.recoil == True:
        return 1.2
    elif ability == "Iron Fist" and move.base == "Punch":
        return 1.2
    elif ability == "Blaze" and move_type == "Fire" and hp_ratio <= 33:
        return 1.5
    elif ability == "Overgrow" and move_type == "Grass" and hp_ratio <= 33:
        return 1.5
    elif ability == "Torrent" and move_type == "Water" and hp_ratio <= 33:
        return 1.5
    elif ability == "Swarm" and move_type == "Bug" and hp_ratio <= 33:
        return 1.5
    elif ability == "Technician" and move.power <= 60:
        return 1.5
    else:
        return 1

# http://www.smogon.com/dp/articles/damage_formula#bp_abilities_foe
def bp_def_multi(ability, type):
    """Returns the defense ability multiplier (base power)"""
    
    if ability == "Thick Fat" and (type == "Ice" or type == "Fire"):
        return 0.5
    elif ability == "Heatproof" and type == "Fire":
        return 0.5
    elif ability == "Dry Skin" and type == "Fire":
        return 1.25
    else:
        return 1

# http://bulbapedia.bulbagarden.net/wiki/Timespace_orbs
# http://bulbapedia.bulbagarden.net/wiki/Type-enhancing_item
# http://www.smogon.com/dp/articles/damage_formula#bp_items
def bp_item_multi(atk_pkmn, move):
    """Calculates the item multiplier (base power)"""
    
    category = move.category
    move_type = move.type
    pkmn_name = atk_pkmn.species.name
    item = atk_pkmn.item
    
    if item == "Muscle Band" and category == "Physical":
        return 1.1
    elif item == "Wise Glasses" and category == "Special":
        return 1.1
    elif plates(item, move_type):
        return 1.2
    elif incenses(item, move_type):
        return 1.2
    elif gems(item, move_type):
        return 1.5
    elif enhancing(item, move_type):
        return 1.1
    elif item == "Pink Bow" and move_type == "Normal":
        return 1.1
    elif item == "Polkadot Bow" and move_name == "Normal":
        return 1.125
    elif item == "Adamant Orb" and pkmn.name == "Dialga" and \
         (move_type == "Steel" or move_type == "Dragon"):
        return 1.2
    elif item == "Lustrous Orb" and pkmn.name == "Palkia" and \
         (move_type == "Water" or move_type == "Dragon"):
        return 1.2
    elif item == "Griseous Orb" and pkmn.name == "Giratina" and \
         (move_type == "Ghost" or move_type == "Dragon"):
        return 1.2
    else:
        return 1

# http://bulbapedia.bulbagarden.net/wiki/Plate
def plates(item, move_type):
    """Returns true if the item and move match the plate (bp_item_multi)"""
    
    if item == "Draco Plate" and move_type == "Dragon":
        return True
    elif item == "Dread Plate" and move_type == "Dark":
        return True
    elif item == "Earth Plate" and move_type == "Ground":
        return True
    elif item == "Fist Plate" and move_type == "Fighting":
        return True
    elif item == "Flame Plate" and move_type == "Fire":
        return True
    elif item == "Icicle Plate" and move_type == "Ice":
        return True
    elif item == "Insect Plate" and move_type == "Bug":
        return True
    elif item == "Iron Plate" and move_type == "Steel":
        return True
    elif item == "Meadow Plate" and move_type == "Grass":
        return True
    elif item == "Mind Plate" and move_type == "Psychic":
        return True
    elif item == "Sky Plate" and move_type == "Flying":
        return True
    elif item == "Splash Plate" and move_type == "Water":
        return True
    elif item == "Spooky Plate" and move_type == "Ghost":
        return True
    elif item == "Stone Plate" and move_type == "Rock":
        return True
    elif item == "Toxic Plate" and move_type == "Poison":
        return True
    elif item == "Zap Plate" and move_type == "Electric":
        return True
    else:
        return False

# http://bulbapedia.bulbagarden.net/wiki/Incense
def incenses(item, move_type):
    """Returns true if the item and move match the incense (bp_item_multi)"""
    
    if item == "Odd Incense" and move_type == "Psychic":
        return True
    if item == "Rock Incense" and move_type == "Rock":
        return True
    if item == "Rose Incense" and move_type == "Grass":
        return True
    if item == "Sea Incense" and move_type == "Water":
        return True
    if item == "Wave Incense" and move_type == "Water":
        return True
    else:
        return False

# http://bulbapedia.bulbagarden.net/wiki/Gem
def gems(item, move_type):
    """Returns true if the item and move match the gem (bp_item_multi)"""
    
    if item == "Fire Gem" and move_type == "Fire":
        return True
    elif item == "Water Gem" and move_type == "Water":
        return True
    elif item == "Electric Gem" and move_type == "Electric":
        return True
    elif item == "Grass Gem" and move_type == "Grass":
        return True
    elif item == "Ice Gem" and move_type == "Ice":
        return True
    elif item == "Fighting Gem" and move_type == "Fighting":
        return True
    elif item == "Poison Gem" and move_type == "Poison":
        return True
    elif item == "Ground Gem" and move_type == "Ground":
        return True
    elif item == "Flying Gem" and move_type == "Flying":
        return True
    elif item == "Psychic Gem" and move_type == "Psychic":
        return True
    elif item == "Bug Gem" and move_type == "Bug":
        return True
    elif item == "Rock Gem" and move_type == "Rock":
        return True
    elif item == "Ghost Gem" and move_type == "Ghost":
        return True
    elif item == "Dragon Gem" and move_type == "Dragon":
        return True
    elif item == "Dark Gem" and move_type == "Dark":
        return True
    elif item == "Steel Gem" and move_type == "Steel":
        return True
    elif item == "Normal Gem" and move_type == "Normal":
        return True
    else:
        return False
        
# http://bulbapedia.bulbagarden.net/wiki/Type-enhancing_item
def enhancing(item, move_type):
    """Returns true if the item and move match the item type (bp_item_multi)"""
    
    if item == "Black Belt" and move_type == "Fighting":
        return True
    elif item == "Black Glasses" and move_type == "Dark":
        return True
    elif item == "Charcoal" and move_type == "Fire":
        return True
    elif item == "Dragon Fang" and move_type == "Dragon":
        return True
    elif item == "Hard Stone" and move_type == "Rock":
        return True
    elif item == "Magnet" and move_type == "Electric":
        return True
    elif item == "Metal Coat" and move_type == "Steel":
        return True
    elif item == "Miracle Seed" and move_type == "Grass":
        return True
    elif item == "Mystic Water" and move_type == "Water":
        return True
    elif item == "Never-Melt Ice" and move_type == "Ice":
        return True
    elif item == "Poison Barb" and move_type == "Poison":
        return True
    elif item == "Sharp Beak" and move_type == "Flying":
        return True
    elif item == "Silk Scarf" and move_type == "Normal":
        return True
    elif item == "Silver Powder" and move_type == "Bug":
        return True
    elif item == "Soft Sand" and move_type == "Ground":
        return True
    elif item == "Spell Tag" and move_type == "Ghost":
        return True
    elif item == "Twisted Spoon" and move_type == "Psychic":
        return True
    else:
        return False

# Hidden Power: # http://www.upokecenter.com/dex/?lang=en&move=237
# http://www.smogon.com/dp/articles/damage_formula#bp_variable
# Maximum values for Assurance, Avalanche, Fury Cutter, 
# Ice Ball/Rollout (no defense curl), Magnitude, Payback, 
# Spit Up, Stomp (no minimize)
# Missing Fling, Natural Gift, Nature Power, Triple Kick, Weather Ball
def move_bp(atk_pkmn, def_pkmn, move):
    """Returns the move base power (base power)"""
    
    atk_hp = atk_pkmn.hp
    atk_hp_ratio = atk_pkmn.calc_hp_ratio()
    weight = def_pkmn.species.weight
    move_name = move.name
    
    if move_name == "Assurance":
        return 100
    elif move_name == "Avalanche":
        return 120
    elif move_name == "Brine":
        if def_pkmn.calc_hp_ratio() <= 50:
            return 130
        else:
            return 65
    elif move_name in {"Crush Grip", "Wring Out"}:
        return 1 + (120 * def_pkmn.hp // def_pkmn.stat[0])
    elif move_name in {"Eruption", "Water Spout"}:
        return (150 * atk_hp // atk_pkmn.stat[0])
    elif move_name == "Facade":
        if atk_pkmn.status in {"Paralyzed", "Poisoned", "Burned"}:
            return 140
        else:
            return 70
    elif move_name in {"Flail", "Reversal"}:
        cp = (atk_hp * 64 // atk_pkmn.stat[0])
        if 0 < cp <= 1:
            return 200
        if 2 < cp <= 5:
            return 150
        if 6 < cp <= 12:
            return 100
        if 13 < cp <= 21:
            return 80
        if 22 < cp <= 42:
            return 40
        if 43 < cp <= 64:
            return 20
    elif move_name == "Fling":
        raise NotImplementedError
    elif move_name == "Frustration":
        bp = 102 - (atk_pkmn.happiness * 2 // 5)
        if bp > 0:
            return bp
        else:
            return 1
    elif move_name == "Fury Cutter":
        return 160
    elif move_name in {"Grass Knot", "Low Kick"}:
        if 0 < weight <= 10:
            return 20
        elif 10 < weight <= 25:
            return 40
        elif 25 < weight <= 50:
            return 60
        elif 50 < weight <= 101:
            return 80
        elif 100 < weight <= 200:
            return 100
        else:
            return 120
    elif move_name == "Gyro Ball":
        bp = 1 + (25 * def_pkmn.stat[5] // atk_pkmn.stat[5])
        if bp > 150:
            return 150
        else:
            return bp
    elif move_name in {"Ice Ball", "Rollout"}:
        return 480
    elif move_name == "Hidden Power":
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
            move.type = type[type_num]
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
            move.type = type[type_num]
        print(move.type)
        return bp
    elif move_name == "Magnitude":
        return 150
    elif move_name == "Natural Gift":
        raise NotImplementedError
    elif move_name == "Nature Power":
        raise NotImplementedError
    elif move_name == "Payback":
        return 100
    elif move_name == "Present":
        return 120
    elif move_name == "Punishment":
        bp = 60 + (sum([x for x in atk_pkmn.stat_mod if x > 0]) * 20)
        if bp > 200:
            return 200
        else:
            return bp
    elif move_name == "Pursuit":
        return 80
    elif move_name == "Return":
        bp = atk_pkmn.happiness * 2 // 5
        if bp == 0:
            return 1
        else:
            return bp
    elif move_name == "Revenge":
        return 120
    elif move_name == "SmellingSalt":
        if atk_pkmn.status == "Paralyzed":
            atk_pkmn.status = "Normal"
            return 120
        else:
            return 60
    elif move_name == "Spit Up":
        return 300
    elif move_name == "Stomp":
        return 65
    elif move_name == "Triple Kick":
        return NotImplementedError
    elif move_name == "Trump Card":
        if move.pp - 1 >= 4:
            return 40
        elif move.pp - 1 == 3:
            return 50
        elif move.pp - 1 == 2:
            return 60
        elif move.pp - 1 == 1:
            return 80
        elif move.pp - 1 == 0:
            return 200
    elif move_name == "Wake-Up Slap":
        if def_pkmn.status == "Sleep":
            def_pkmn.status = "Normal"
            return 120
        else:
            return 60
    elif move_name == "Weather Ball":
        raise NotImplementedError
    else:
        return move.power