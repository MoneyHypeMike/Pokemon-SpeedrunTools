import pokemon
from math import floor

#http://www.smogon.com/bw/articles/bw_complete_damage_formula
def damage5(atk_pkmn, def_pkmn, move, battle_type="SINGLE", screen=[], crit=False, weather="NORMAL"):
    
    name = move.name
    damage_range = []
    modifiers = []
    final_mods = []
    stab_mod = 0x1000
    burn = False
    
    #Special Cases
    if name == "PSYWAVE":
        return "Damage is between {} and {}.".format(50 * atk_pkmn.level // 100, 150 * atk_pkmn.level // 100)
    elif name == "NIGHT SHADE":
        return "Damage is the level of the user Pokémon ({}).".format(atk_pkmn.level)
    elif name == "SONICBOOM":
        return "Damage is always 40."
    elif name == "SUPER FANG":
        return "Damage is the maximum between 1 and half the target HP."
    elif name == "DRAGON RAGE":
        return "Damage is always 40."
    elif name == "ENDEAVOR":
        return "Damage is target current HP - user current HP."
    elif name == "FINAL GAMBIT":
        return "Damage is the user HP."
    elif name == "BRICK BREAK":
        screen = []
    elif name == "COUNTER":
        return "Damage is double the amount taken on the last turn if the move was physical."
    elif name == "MIRROR COAT":
        return "Damage is double the amount taken on the last turn if the move was special."
    elif name == "METAL BURST":
        return "Damage is 1.5x the amount taken on this turn if you are slower than the target Pokémon."
    elif name == "BIDE":
        return "Damage is double the amount taken on the last 2 turns."
    
    #Physical or special move (missing wonder room, thing that swap defenses)
    if move.name == "Foul Play":
        attack = def_pkmn.stat[1]
        atk_boost = def_pkmn.boost[1]
    else:
        if move.category == "PHYSICAL":
            attack = atk_pkmn.stat[1]
            if atk_pkmn.ability == "HUSTLE":
                attack = attack * 0x1800 // 0x1000 
            atk_boost = atk_pkmn.boost[1]
            defense = def_pkmn.stat[2]
            def_boost = def_pkmn.boost[2]
        elif move.category == "SPECIAL":
            attack = atk_pkmn.stat[3]
            atk_boost = atk_pkmn.boost[3]
            defense = def_pkmn.stat[4]
            def_boost = def_pkmn.boost[4]
    
    #Base Power
    bp = base_power(atk_pkmn, def_pkmn, move)
    mod_bp = bp_mod(atk_pkmn, def_pkmn, move)
    bp = rounding(bp * mod_bp / 0x1000)
    
    #Attack
    if def_pkmn.ability == "UNAWARE":
        dividend, divisor = (2, 2)
    else:
        dividend, divisor = stat_boost(atk_boost)
    if crit: divisor = 2
    attack = attack * dividend // divisor
    mod_atk = atk_mod(atk_pkmn, def_pkmn, move, battle_type, weather)
    attack = rounding(attack * mod_atk / 0x1000)
    
    #Defense
    if def_pkmn.ability == "UNAWARE" or move.name == "CHIP AWAY":
        dividend, divisor = (2, 2)
    else:
        dividend, divisor = stat_boost(def_boost)
    defense = defense * dividend // divisor
    if weather == "SANDSTORM" and "ROCK" in def_pkmn.types and move.category == "SPECIAL":
        defense = rounding(defense * 0x1800 / 0x1000)
    mod_def = def_mod(def_pkmn, move)
    defense = rounding(defense * mod_def / 0x1000)
    
    #Initial Damage Formula
    base_damage = ((((2 * atk_pkmn.level) // 5 + 2) * bp * attack) // defense) // 50 + 2
    
    #1. Multi Target Modifier
    if battle_type != "SINGLE" and move.target in ("ALL", "ALL OPPONENT"):
        base_damage = rounding(base_damage * 0xC00 / 0x1000)
    
    #2. Weather Modifier
    if (weather == "RAIN DANCE" and move.type.name == "WATER") or (weather == "SUNNY DAY" and move.type.name == "FIRE"):
        base_damage = rounding(base_damage * 0x1800 / 0x1000)
    elif (weather == "RAIN DANCE" and move.type.name == "FIRE") or (weather == "SUNNY DAY" and move.type.name == "WATER"):
        base_damage = rounding(base_damage * 0x800 / 0x1000)
    
    #3. Critical Hit
    if crit and def_pkmn.ability not in ("BATTLE ARMOR", "SHELL ARMOR"): base_damage = floor(base_damage * 2)
    
    #5. Stab Modifier
    if move.type.name in [x.name for x in atk_pkmn.species.types]:
        stab_mod = 0x2000 if atk_pkmn.ability == "ADAPTABILITY" else 0x1800
    
    #6. Type Effectiveness
    type1, type2 = move.type.type_multi(def_pkmn.species.types)
    type_multi = type1 * type2
    
    #7. Burn Effect
    if move.category == "PHYSICAL" and atk_pkmn.status == "BRN" and atk_pkmn.ability != "GUTS": burn = True
    
    #9. Final Modifier (need to add metronome, type resist berries, friend guard)
    if ((move.category == "PHYSICAL" and "REFLECT" in screen) or (move.category == "SPECIAL" and "LIGHT SCREEN" in screen)) and atk_pkmn.ability != "INFILTRATOR" and not crit:
        if battle_type == "SINGLE":
            final_mods.append(0x800)
        else:
            final_mods.append(0xA8F)
    
    if def_pkmn.ability == "MULTISCALE" and def_pkmn.calc_hp_ratio() == 100:
        final_mods.append(0x800)
    elif def_pkmn.ability in ("FILTER", "SOLID ROCK") and type_multi > 1:
        final_mods.append(0xC00)
    
    if atk_pkmn.ability == "TINTED LENS" and type_multi < 0:
        final_mods.append(0x2000)
    elif atk_pkmn.ability == "SNIPER" and crit:
        final_mods.append(0x1800)
    
    if atk_pkmn.item == "EXPERT BELT" and type_multi > 1:
        final_mods.append(0x1333)
    elif atk_pkmn.item == "LIFE ORB":
        final_mods.append(0x14CC)
    
    if (move.name in ("STOMP", "STEAMROLLER") and "MINIMIZE" in [x.name for x in def_pkmn.moves]) or \
       (move.name == "EARTHQUAKE" and "DIG" in [x.name for x in def_pkmn.moves]) or \
       (move.name == "SURF" and "DIVE" in [x.name for x in def_pkmn.moves]):
        final_mods.append(0x2000)
        
    #4. Random Factor
    for x in range(0, 16):
        damage = base_damage * (85 + x) // 100
        damage = rounding(damage * stab_mod / 0x1000)
        damage = floor(damage * type_multi)
        if burn == True: damage = damage // 2
        damage = max(1, damage)
        damage_range.append(rounding(damage * chain_mod(final_mods) / 0x1000))
        
    return damage_range

#Missing beat up, hidden power, natural gift, fling, pledge moves
def base_power(atk_pkmn, def_pkmn, move):
    name = move.name
    
    if name == "FRUSTRATION":
        return 102 #[((255 - atk_pkmn.happiness) * 10) // 25]
    elif name == "PAYBACK":
        if atk_pkmn.stat[5] < def_pkmn.stat[5]:
            return 50 #[50]
        else:
            return 100 #[100]
    elif name in ("ASSURANCE", "HEX"):
        return 50 #[50, 100]
    elif name == "RETURN":
        return 102 #[(atk_pkmn.happiness * 10) // 25]
    elif name == "ELECTRO BALL":
        s = atk_pkmn.stat[5] // def_pkmn.stat[5]
        if s >= 4:
            return 150 #[150]
        elif s >= 3:
            return 120 #[120]
        elif s >= 2:
            return 80 #[80]
        elif s >= 1:
            return 60 #[60]
        else:
            return 40 #[40]
    elif name in ("AVALANCHE", "SMELLING SALT", "WAKE-UP SLAP"):
        return 60 #[60, 120]
    elif name == "GYRO BALL":
        return 25 #[min(125, 25 * atk_pkmn.stat[5] // def_pkmn.stat[5])]
    elif name in ("ERUPTION", "WATER SPOUT"):
        return 150 #[150]
    elif name == "PUNISHMENT":
        return 60 #[min(120, 60 + 20 * sum(def_pkmn.boost))]
    elif name in ("ECHOED VOICE", "FURY CUTTER"):
        return 20 #[20, 40, 60, 80, 100, 120]
    elif name in ("LOW KICK", "GRASS KNOT"):
        w = def_pkmn.weight
        if w >= 200:
            return 120 #[120]
        elif w >= 100:
            return 100 #[100]
        elif w >= 50:
            return 80 #[80]
        elif w >= 25:
            return 60 #[60]
        elif w >= 10:
            return 40 #[40]
        else:
            return 20 #[20]
    elif name in ("WRING OUT", "CRUSH GRIP"):
        return 120 #[120]
    elif name in ("HEAT CRASH", "HEAVY SLAM"):
        w = atk_pkmn.weight // def_pkmn.weight
        if w >= 5:
            return 120 #[120]
        elif w >= 4:
            return 100 #[100]
        elif w >= 3:
            return 80 #[80]
        elif w >=2:
            return 60 #[60]
        elif w < 2:
            return 40 #[40]
    elif name == "STORED POWER":
        return 20 #[20 + 20 * sum(atk_pkmn.boost)]
    elif name == "ACROBATICS":
        if atk_pkmn.item == "":
            return 110 #[110]
        else:
            return 55 #[55]
    elif name in ("FLAIL", "REVERSAL"):
        return 20 #[20, 40, 80, 100, 150, 200]
    elif name == "TRUMP CARD":
        return 40 #[40, 50, 60, 80, 200]
    elif name == "ROUND":
        if battle_type == "SINGLE":
            return 60 #[60]
        else:
            return 120 #[120]
    elif name == "DOUBLE KICK":
        return 10 #[10, 20, 30]
    elif name == "WEATHER BALL":
        if weather == "NORMAL":
            return 50 #[50]
        else:
            return 100 #[100]
    elif name in ("GUST", "TWISTER"):
        return 40 #[40, 80]
    elif name == "SPIT UP":
        if "Stockpile" in [x.name for x in def_pkmn.moves]:
            return 100 #[100, 200, 300]
        else:
            return 0 #[0]
    elif name == "PURSUIT":
        return 40 #[40, 80]
    elif name == "PRESENT":
        return 40 #[40, 80, 120]
    elif name == "MAGNITUDE":
        return 10 #[10, 30, 50, 70, 90, 110, 130, 150]
    elif name == "ROLLOUT":
        return 30 #[30, 60, 120, 240, 480, 960]
    else:
        return move.power

#Base Power Modifiers
#Missing Sheer Force, missing type boosting items, plates, incense, gem, missing me first, helping hand
def bp_mod(atk_pkmn, def_pkmn, move, field=None):
    ability = atk_pkmn.ability
    name = move.name
    modifiers = []
    
    if ability == "TECHNICIAN" and move.power <= 60:
        modifiers.append(0x1800)
    elif ability == "FLARE BOOST" and atk_pkmn.status == "BRN" and move.category == "SPECIAL":
        modifiers.append(0x1800)
    elif ability == "ANALYTIC" and (atk_pkmn.stat[5] < def_pkmn.stat[5]):
        modifiers.append(0x14CD)
    elif ability == "RECKLESS" and (move.recoil or move.name in ("JUMP KICK", "HI JUMP KICK")):
        modifiers.append(0x1333)
    elif ability == "IRON FIST" and move.punch:
        modifiers.append(0x1333)
    elif ability == "TOXIC BOOST" and atk_pkmn.status == "POISON" and move.category == "PHYSICAL":
        modifiers.append(0x1800)
    elif ability == "RIVALRY":
        if "GENDERLESS" in (atk_pkmn.gender, def_pkmn.gender):
            modifiers.append(0x1000)
        elif atk_pkmn.gender == def_pkmn.gender:
            modifiers.append(0x1400)
        else:
            modifiers.append(0xC00)
    elif ability == "SAND FORCE" and move.type.name in ("ROCK", "GROUND", "STEEL"):
        modifiers.append(0x14CD)
    elif ability == "HEATPROOF" and move.type.name == "FIRE":
        modifiers.append(0x800)
    elif ability == "DRY SKIN" and move.type.name == "FIRE":
        modifiers.append(0x1400)
    
    if atk_pkmn.item == "MUSCLE BAND" and move.category == "PHYSICAL":
        modifiers.append(0x1199)
    elif atk_pkmn.item == "WISE GLASS" and move.category == "SPECIAL":
        modifiers.append(0x1199)
    elif atk_pkmn.species.name == "PALKIA" and atk_pkmn.item == "LUSTROUS ORB" and move.type.name in ("DRAGON", "WATER"):
        modifiers.append(0x1333)
    elif atk_pkmn.species.name == "GIRATINA" and atk_pkmn.item == "GRISEOUS ORB" and move.type.name in ("GHOST", "DRAGON"):
        modifiers.append(0x1333)
    elif atk_pkmn.species.name == "DIALGA" and atk_pkmn.item == "ADAMANT ORB" and move.type.name in ("STEEL", "DRAGON"):
        modifiers.append(0x1333)
    
    if name == "FACADE" and atk_pkmn.status in ("BURN", "POISON", "BURN"):
        modifiers.append(0x2000)
    elif name == "BRINE" and atk_pkmn.calc_hp_ratio <= 50:
        modifiers.append(0x2000)
    elif name == "VENOSHOCK" and atk_pkmn.status == "POISON":
        modifiers.append(0x2000)
    elif name == "RETALIATE":
        modifiers.append(0x2000)
    elif name in ("FUSION BOLT", "FUSION FLARE"):
        modifiers.append(0x2000)
    elif name == "SOLARBEAM" and weather not in ("NORMAL", "SUNNY DAY"):
        modifiers.append(0x800)
    elif name == "CHARGE" and "ELECTRIC" in [x.type.name in atk_pkmn.moves]:
        modifiers.append(0x2000)
    elif move.type.name == "FIRE" and field == "WATER SPORT":
        modifiers.append(0x548)
    elif move.type.name == "ELECTRIC" and field == "MUD SPORT":
        modifiers.append(0x548)
        
    return chain_mod(modifiers)

#Attack Modifiers
#Missing Plus/Minus, slow start, flower gift
def atk_mod(atk_pkmn, def_pkmn, move, battle_type="SINGLE", weather="NORMAL"):
    ability = atk_pkmn.ability
    item = atk_pkmn.item
    modifiers = []
    
    if def_pkmn.ability == "THICK FAT" and move.type.name in ("FIRE", "ICE"):
        modifiers.append(0x800)
    
    if ability == "TORRENT" and atk_pkmn.calc_hp_ratio() <= 33 and move.type.name == "WATER":
        modifiers.append(0x1800)
    elif ability == "BLAZE" and atk_pkmn.calc_hp_ratio() <= 33 and move.type.name == "FIRE":
        modifiers.append(0x1800)
    elif ability == "OVERGROW" and atk_pkmn.calc_hp_ratio() <= 33 and move.type.name == "GRASS":
        modifiers.append(0x1800)
    elif ability == "SWARM" and atk_pkmn.calc_hp_ratio() <= 33 and move.type.name == "BUG":
        modifiers.append(0x1800)
    elif ability == "GUTS" and atk_pkmn.status in ("BRN", "PSN", "PRZ") and move.category == "PHYSICAL":
        modifiers.append(0x1800)
    elif ability == "DEFEATIST" and atk_pkmn.calc_hp_ratio <= 50:
        modifiers.append(0x800)
    elif ability in ("PURE POWER", "HUGE POWER") and move.category == "PHYSICAL":
        modifiers.append(0x2000)
    elif ability == "SOLAR POWER" and weather == "SUNNY DAY" and move.category == "SPECIAL":
        modifiers.append(0x1800)
    elif ability == "FLASH FIRE" and move.type == "FIRE":
        modifiers.append(0x1800)
    elif atk_pkmn.species.name in ("CUBONE", "MAROWAK") and atk_pkmn.item == "THICK CLUB" and move.category == "PHYSICAL":
        modifiers.append(0x2000)
    elif atk_pkmn.species.name == "CLAMPERL" and atk_pkmn.item == "DEEPSEATOOTH" and move.category == "Special":
        modifiers.append(0x2000)
    elif atk_pkmn.species.name == "PIKACHU" and atk_pkmn.item == "LIGHT BALL":
        modifiers.append(0x2000)
    elif atk_pkmn.species.name in ("LATIOS", "LATIAS") and atk_pkmn.item == "SOUL DEW" and move.category == "SPECIAL":
        modifiers.append(0x1800)
    
    if item == "CHOICE BAND" and move.category == "PHYSICAL":
        modifiers.append(0x1800)
    elif item == "CHOICE SPECS" and move.category == "SPECIAL":
        modifiers.append(0x1800)
        
    return chain_mod(modifiers)

#Defense Modifiers
#Missing Flower Gift, Eviolite
def def_mod(def_pkmn, move):
    modifiers = []
    if def_pkmn.ability == "MARVEL SCALE" and atk_pkmn.status in ("BRN", "PRZ", "FRZ", "PSN") and move.category == "PHYSICAL":
        modifiers.append(0x1800)
    elif def_pkmn.species.name == "CLAMPERL" and def_pkmn.item == "DEEPSEASCALE" and move.category == "SPECIAL":
        modifiers.append(0x1800)
    elif def_pkmn.species.name == "DITTO" and def_pkmn.item == "METAL POWDER" and move.category == "PHYSICAL":
        modifiers.append(0x2000)
    elif def_pkmn.species.name in ("LATIOS", "LATIAS") and def_pkmn.item == "SOUL DEW" and move.category == "SPECIAL":
        modifiers.append(0x1800)
        
    return chain_mod(modifiers)

def chain_mod(mods):
    m = 0x1000
    for x in mods:
        m = ((m * x) + 0x800) >> 12
        
    return m

def rounding(value):
    from math import modf, floor, ceil
    if modf(value)[0] <= 0.5:
        return floor(value)
    else:
        return ceil(value)

def stat_boost(number):
    if number == 0:
        return (2, 2)
    elif number < 0:
        return (2, 2 - number)
    else:
        return (2 + number, 2)

tepig = pokemon.Pokemon(5, "TEPIG", "MALE", 5, "ADAMANT", "BLAZE", "", "TACKLE", "EMBER", "FLAME CHARGE", "AQUA JET", 30, 30, 30, 30, 30, 30)
snivy = pokemon.Pokemon(5, "SNIVY", "MALE", 5, "BOLD", "OVERGROW", "", "TACKLE", "", "", "", 0, 0, 0, 0, 0, 0)
tepig.hp = 3
tepig.item = "CHOICE BAND"
print(damage5(tepig, snivy, tepig.moves[0]))
print(damage5(tepig, snivy, tepig.moves[1]))
print(damage5(tepig, snivy, tepig.moves[2]))
print(damage5(tepig, snivy, tepig.moves[3]))