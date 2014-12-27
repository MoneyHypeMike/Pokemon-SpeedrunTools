import pokemon
from math import floor

#http://www.smogon.com/bw/articles/bw_complete_damage_formula
def damage5(atk_pkmn, def_pkmn, move, battle_type="SINGLE", screen=[""], crit=False, weather="NORMAL"):
    
    name = move.name
    total_damage = []
    modifiers = []
    final_mods = []
    stab_mod = 0x1000
    burn = False
    
    #Moves which don't follow the damage formula.
    if name == "PSYWAVE":
        #return "Damage is between {} and {}.".format(50 * atk_pkmn.level // 100, 150 * atk_pkmn.level // 100)
        return [[0]]
    elif name == "NIGHT SHADE":
        #return "Damage is the level of the user Pokémon ({}).".format(atk_pkmn.level)
        return [[0]]
    elif name == "SONICBOOM":
        #return "Damage is always 40."
        return [[0]]
    elif name == "SUPER FANG":
        #return "Damage is the maximum between 1 and half the target HP."
        return [[0]]
    elif name == "DRAGON RAGE":
        #return "Damage is always 40."
        return [[0]]
    elif name == "ENDEAVOR":
        #return "Damage is target current HP - user current HP."
        return [[0]]
    elif name == "FINAL GAMBIT":
        #return "Damage is the user HP."
        return [[0]]
    elif name == "BRICK BREAK":
        screen = [""]
    elif name == "COUNTER":
        #return "Damage is double the amount taken on the last turn if the move was physical."
        return [[0]]
    elif name == "MIRROR COAT":
        #return "Damage is double the amount taken on the last turn if the move was special."
        return [[0]]
    elif name == "METAL BURST":
        #return "Damage is 1.5x the amount taken on this turn if you are slower than the target Pokémon."
        return [[0]]
    elif name == "BIDE":
        #return "Damage is double the amount taken on the last 2 turns."
        return [[0]]
       
    #6. Type Effectiveness
    type1, type2 = move.type.type_multi(def_pkmn.species.types)
    type_multi = type1 * type2
    
    #Moves that inflict no damage.
    if move.category == "STATUS" or type_multi == 0:
        return [[0]]
    
    #Physical or special move (missing wonder room, thing that swap defenses)
    if move.category == "PHYSICAL":
        attack = def_pkmn.stat[1] if move.name == "FOUL PLAY" else atk_pkmn.stat[1]
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
    bp = base_power(atk_pkmn, def_pkmn, move, battle_type)
    mod_bp = bp_mod(atk_pkmn, def_pkmn, move, weather)
    bp = [rounding(x * mod_bp / 0x1000) for x in bp]
    
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
    if def_pkmn.ability == "UNAWARE" or name == "CHIP AWAY":
        dividend, divisor = (2, 2)
    else:
        dividend, divisor = stat_boost(def_boost)
    if crit: dividend = 2
    defense = defense * dividend // divisor
    if (weather == "SANDSTORM" and "ROCK" in def_pkmn.types) and move.category == "SPECIAL":
        defense = rounding(defense * 0x1800 / 0x1000)
    mod_def = def_mod(def_pkmn, move)
    defense = rounding(defense * mod_def / 0x1000)
    
    #Initial Damage Formula
    base_damage = [((((2 * atk_pkmn.level) // 5 + 2) * x * attack) // defense) // 50 + 2 for x in bp]
    
    #1. Multi Target Modifier
    if battle_type != "SINGLE" and move.target in ("ALL", "ALL OPPONENT"):
        base_damage = [rounding(x * 0xC00 / 0x1000) for x in base_damage]
    
    #2. Weather Modifier
    if (weather == "RAIN DANCE" and move.type.name == "WATER") or (weather == "SUNNY DAY" and move.type.name == "FIRE"):
        base_damage = [rounding(x * 0x1800 / 0x1000) for x in base_damage]
    elif (weather == "RAIN DANCE" and move.type.name == "FIRE") or (weather == "SUNNY DAY" and move.type.name == "WATER"):
        base_damage = [rounding(x * 0x800 / 0x1000) for x in base_damage]
    
    #3. Critical Hit
    if crit and def_pkmn.ability not in ("BATTLE ARMOR", "SHELL ARMOR"):
        base_damage = [floor(x * 2) for x in base_damage]
    
    #5. Stab Modifier
    if move.type.name in [x.name for x in atk_pkmn.species.types]:
        stab_mod = 0x2000 if atk_pkmn.ability == "ADAPTABILITY" else 0x1800
    
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
    
    if berries(def_pkmn.item, move.type.name, type_multi):
        final_mods.append(0x800)
    
    if (move.name in ("STOMP", "STEAMROLLER") and "MINIMIZE" in [x.name for x in def_pkmn.moves]) or \
       (move.name == "EARTHQUAKE" and "DIG" in [x.name for x in def_pkmn.moves]) or \
       (move.name == "SURF" and "DIVE" in [x.name for x in def_pkmn.moves]):
        final_mods.append(0x2000)
        
    #4. Random Factor
    for y in base_damage:
        damage_range = []
        for x in range(85, 101):
            damage = y * x // 100
            damage = rounding(damage * stab_mod / 0x1000)
            damage = floor(damage * type_multi)
            if burn == True: damage = damage // 2
            damage = max(1, damage)
            damage_range.append(rounding(damage * chain_mod(final_mods) / 0x1000))
        total_damage.append(damage_range)
    
    return total_damage
    
def base_power(atk_pkmn, def_pkmn, move, battle_type):
    name = move.name
    
    if name == "FRUSTRATION":
        return [((255 - atk_pkmn.happiness) * 10) // 25]
    elif name in ("ASSURANCE", "HEX", "PAYBACK"):
        return [50, 100]
    elif name == "RETURN":
        return [(atk_pkmn.happiness * 10) // 25]
    elif name == "ELECTRO BALL":
        s = atk_pkmn.stat[5] // def_pkmn.stat[5]
        if s >= 4:
            return [150]
        elif s >= 3:
            return [120]
        elif s >= 2:
            return [80]
        elif s >= 1:
            return [60]
        else:
            return [40]
    elif name in ("AVALANCHE", "SMELLING SALT", "WAKE-UP SLAP"):
        return [60, 120]
    elif name == "GYRO BALL":
        return [min(150, 25 * atk_pkmn.stat[5] // def_pkmn.stat[5])]
    elif name in ("ERUPTION", "WATER SPOUT"):
        return [150 * atk_pkmn.hp // atk_pkmn.stat[0]]
    elif name == "PUNISHMENT":
        return [min(120, 60 + 20 * sum(def_pkmn.boost))]
    elif name == "FURY CUTTER":
        return [20, 40, 60, 80, 100, 120]
    elif name in ("LOW KICK", "GRASS KNOT"):
        w = def_pkmn.species.weight
        if w >= 200:
            return [120]
        elif w >= 100:
            return [100]
        elif w >= 50:
            return [80]
        elif w >= 25:
            return [60]
        elif w >= 10:
            return [40]
        else:
            return [20]
    elif name == "ECHOED VOICE":
        return [40, 80, 120, 160, 200]
    elif name in ("WRING OUT", "CRUSH GRIP"):
        return [120]
    elif name in ("HEAT CRASH", "HEAVY SLAM"):
        w = atk_pkmn.species.weight // def_pkmn.species.weight
        if w >= 5:
            return [120]
        elif w >= 4:
            return [100]
        elif w >= 3:
            return [80]
        elif w >=2:
            return [60]
        elif w < 2:
            return [40]
    elif name == "STORED POWER":
        return [20 + 20 * sum(atk_pkmn.boost)]
    elif name == "ACROBATICS":
        if atk_pkmn.item == "":
            return [110]
        else:
            return [55]
    elif name in ("FLAIL", "REVERSAL"):
        return [20, 40, 80, 100, 150, 200]
    elif name == "TRUMP CARD":
        return [40, 50, 60, 80, 200]
    elif name == "ROUND":
        if battle_type == "SINGLE":
            return [60]
        else:
            return [60, 120]
    elif name == "TRIPLE KICK":
        return [10, 20, 30]
    elif name == "WEATHER BALL":
        if weather == "NORMAL":
            return [50]
        else:
            return [100]
    elif name in ("GUST", "TWISTER"):
        return [40, 80]
    elif name == "SPIT UP":
        if "STOCKPILE" in [x.name for x in def_pkmn.moves]:
            return [100, 200, 300]
        else:
            return [0]
    elif name == "PURSUIT":
        return [40, 80]
    elif name == "PRESENT":
        return [40, 80, 120]
    elif name == "MAGNITUDE":
        return [10, 30, 50, 70, 90, 110, 130, 150]
    elif name == "REVENGE":
        return [60, 120]
    elif name == "ROLLOUT":
        if "DEFENSE CURL" in [x.name for x in atk_pkmn.moves]:
            return [60, 120, 240, 480, 960]
        else:
            return [30, 60, 120, 240, 480]
    elif name in ("BEAT UP", "FLING", "FIRE PLEDGE", "GRASS PLEDGE", "NATURAL GIFT", "WATER PLEDGE", "WONDER ROOM"):
        raise NotImplementedError
    else:
        return [move.power]

#Base Power Modifiers
def bp_mod(atk_pkmn, def_pkmn, move, weather, field=None):
    ability = atk_pkmn.ability
    name = move.name
    item = atk_pkmn.item
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
    elif ability == "SAND FORCE" and move.type.name in ("ROCK", "GROUND", "STEEL") and weather == "SANDSTORM":
        modifiers.append(0x14CD)
    #elif ability == "SHEER FORCE":
    #    raise NotImplementedError
    
    if def_pkmn.ability == "HEATPROOF" and move.type.name == "FIRE":
        modifiers.append(0x800)
    elif def_pkmn.ability == "DRY SKIN" and move.type.name == "FIRE":
        modifiers.append(0x1400)
    
    if item == "MUSCLE BAND" and move.category == "PHYSICAL":
        modifiers.append(0x1199)
    elif item == "WISE GLASS" and move.category == "SPECIAL":
        modifiers.append(0x1199)
    elif item == "LUSTROUS ORB" and atk_pkmn.species.name == "PALKIA" and move.type.name in ("DRAGON", "WATER"):
        modifiers.append(0x1333)
    elif item == "GRISEOUS ORB" and atk_pkmn.species.name == "GIRATINA" and move.type.name in ("GHOST", "DRAGON"):
        modifiers.append(0x1333)
    elif item == "ADAMANT ORB" and atk_pkmn.species.name == "DIALGA" and move.type.name in ("STEEL", "DRAGON"):
        modifiers.append(0x1333)
    elif gems(item, move.type.name):
        modifiers.append(0x1800)
    elif item_boost(item, move.type.name):
        modifiers.append(0x1333)
        
    if name == "FACADE" and atk_pkmn.status in ("PRZ", "PSN", "BRN"):
        modifiers.append(0x2000)
    elif name == "BRINE" and atk_pkmn.calc_hp_ratio() <= 50:
        modifiers.append(0x2000)
    elif name == "VENOSHOCK" and atk_pkmn.status == "POISON":
        modifiers.append(0x2000)
    elif name == "RETALIATE":
        modifiers.append(0x2000)
    elif name in ("FUSION BOLT", "FUSION FLARE"):
        modifiers.append(0x2000)
    elif name == "SOLARBEAM" and weather not in ("NORMAL", "SUNNY DAY"):
        modifiers.append(0x800)
    elif move.type.name == "ELECTRIC" and "CHARGE" in [x.name for x in atk_pkmn.moves]:
        modifiers.append(0x2000)
    elif name in ("ME FIRST", "HELPING HAND"):
        raise NotImplementedError
        
    if move.type.name == "FIRE" and field == "WATER SPORT":
        modifiers.append(0x548)
    elif move.type.name == "ELECTRIC" and field == "MUD SPORT":
        modifiers.append(0x548)
        
    return chain_mod(modifiers)

#Attack Modifiers
def atk_mod(atk_pkmn, def_pkmn, move, battle_type="SINGLE", weather="NORMAL"):
    ability = atk_pkmn.ability
    category = move.category
    hp_ratio = atk_pkmn.calc_hp_ratio()
    item = atk_pkmn.item
    name = atk_pkmn.species.name
    type = move.type.name
    modifiers = []
    
    if def_pkmn.ability == "THICK FAT" and move.type.name in ("FIRE", "ICE"):
        modifiers.append(0x800)
    
    if ability == "TORRENT" and hp_ratio <= 33 and type == "WATER":
        modifiers.append(0x1800)
    elif ability == "BLAZE" and hp_ratio <= 33 and type == "FIRE":
        modifiers.append(0x1800)
    elif ability == "OVERGROW" and hp_ratio <= 33 and type == "GRASS":
        modifiers.append(0x1800)
    elif ability == "SWARM" and hp_ratio <= 33 and type == "BUG":
        modifiers.append(0x1800)
    elif ability == "GUTS" and atk_pkmn.status in ("BRN", "PSN", "PRZ") and category == "PHYSICAL":
        modifiers.append(0x1800)
    elif ability == "DEFEATIST" and hp_ratio <= 50:
        modifiers.append(0x800)
    elif ability in ("PURE POWER", "HUGE POWER") and category == "PHYSICAL":
        modifiers.append(0x2000)
    elif ability == "SOLAR POWER" and weather == "SUNNY DAY" and category == "SPECIAL":
        modifiers.append(0x1800)
    elif ability in ("PLUS", "MINUS") and battle_type != "SINGLE" and category == "SPECIAL":
        modifiers.append(0x1800)
    elif ability in ("FLASH FIRE", "FLOWER GIFT", "SLOW START"):
        raise NotImplementedError
    
    if name in ("CUBONE", "MAROWAK") and item == "THICK CLUB" and category == "PHYSICAL":
        modifiers.append(0x2000)
    elif name == "CLAMPERL" and item == "DEEPSEATOOTH" and category == "SPECIAL":
        modifiers.append(0x2000)
    elif name == "PIKACHU" and item == "LIGHT BALL":
        modifiers.append(0x2000)
    elif name in ("LATIOS", "LATIAS") and item == "SOUL DEW" and category == "SPECIAL":
        modifiers.append(0x1800)
    elif item == "CHOICE BAND" and category == "PHYSICAL":
        modifiers.append(0x1800)
    elif item == "CHOICE SPECS" and category == "SPECIAL":
        modifiers.append(0x1800)
    
    return chain_mod(modifiers)

#Defense Modifiers
#Missing Flower Gift, Eviolite
def def_mod(def_pkmn, move):
    category = move.category
    item = def_pkmn.item
    name = def_pkmn.species.name
    modifiers = []
    
    if def_pkmn.ability == "MARVEL SCALE" and atk_pkmn.status in ("BRN", "PRZ", "FRZ", "PSN") and category == "PHYSICAL":
        modifiers.append(0x1800)
    elif name == "CLAMPERL" and item == "DEEPSEASCALE" and category == "SPECIAL":
        modifiers.append(0x1800)
    elif name == "DITTO" and item == "METAL POWDER" and category == "PHYSICAL":
        modifiers.append(0x2000)
    elif name in ("LATIOS", "LATIAS") and item == "SOUL DEW" and category == "SPECIAL":
        modifiers.append(0x1800)
    elif def_pkmn.ability == "FLOWER GIFT" or item == "EVIOLITE":
        raise NotImplementedError
        
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

def berries(item, type, multiplier):
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
        
def item_boost(item, type):
    if item in ("BLACK BELT", "FIST PLATE") and type == "FIGHTING":
        return True
    elif item in ("BLACK GLASSES", "DREAD PLATE") and type == "DARK":
        return True
    elif item in ("CHARCOAL", "FLAME PLATE") and type == "FIRE":
        return True
    elif item in ("DRAGON FANG", "DRACO PLATE") and type == "DRAGON":
        return True
    elif item in ("HARD STONE", "STONE PLATE", "ROCK INCENSE") and type == "ROCK":
        return True
    elif item in ("MAGNET", "ZAP PLATE") and type == "ELECTRIC":
        return True
    elif item in ("METAL COAT", "IRON PLATE") and type == "STEEL":
        return True
    elif item in ("MIRACLE SEED", "MEADOW PLATE", "ROSE INCENSE") and type == "GRASS":
        return True
    elif item in ("MYSTIC WATER", "SPLASH PLATE", "SEA INCENSE", "WAVE INCENSE") and type == "WATER":
        return True
    elif item in ("NEVER-MELT ICE", "ICICLE PLATE") and type == "ICE":
        return True
    elif item in ("POISON BARB", "TOXIC PLATE") and type == "POISON":
        return True
    elif item in ("SHARP BEAK", "SKY PLATE") and type == "FLYING":
        return True
    elif item in ("SILK SCARF",) and type == "NORMAL":
        return True
    elif item in ("SILVER POWDER", "INSECT PLATE") and type == "BUG":
        return True
    elif item in ("SOFT SAND", "EARTH PLATE") and type == "GROUND":
        return True
    elif item in ("SPELL TAG", "SPOOKY PLATE") and type == "GHOST":
        return True
    elif item in ("TWISTED SPOON", "MIND PLATE", "ODD INCENSE") and type == "PSYCHIC":
        return True
    else:
        return False
        
def gems(item, type):   
    if item == "BUG GEM" and type == "BUG":
        return True
    elif item == "DARK GEM" and type == "DARK":
        return True
    elif item == "DRAGON GEM" and type == "DRAGON":
        return True
    elif item == "ELECTRIC GEM" and type == "ELECTRIC":
        return True
    elif item == "FIGHTING GEM" and type == "FIGHTING":
        return True
    elif item == "FIRE GEM" and type == "FIRE":
        return True
    elif item == "FLYING GEM" and type == "FLYING":
        return True
    elif item == "GHOST GEM" and type == "GHOST":
        return True
    elif item == "GRASS GEM" and type == "GRASS":
        return True
    elif item == "GROUND GEM" and type == "GROUND":
        return True
    elif item == "ICE GEM" and type == "ICE":
        return True
    elif item == "NORMAL GEM" and type == "NORMAL":
        return True
    elif item == "POISON GEM" and type == "POISON":
        return True
    elif item == "PSYCHIC GEM" and type == "PSYCHIC":
        return True
    elif item == "ROCK GEM" and type == "ROCK":
        return True
    elif item == "STEEL GEM" and type == "STEEL":
        return True
    elif item == "WATER GEM" and type == "WATER":
        return True
    else:
        return False
        
#tepig = pokemon.Pokemon(5, "tEPIG", "MaLe", 9, "aDamant", "Blaze", "", "tAckle", "eMBeR", "", "", 30, 30, 30, 30, 30, 30)
#snivy = pokemon.Pokemon(5, "SNIVY", "MALE", 7, "bashful", "OVERGROW", "", "TACKLE", "", "", "", 3, 3, 3, 3, 3, 3)
#print(damage5(tepig, snivy, tepig.moves[0]))
#print(damage5(tepig, snivy, tepig.moves[1]))
#print(damage5(tepig, snivy, tepig.moves[2]))
#print(damage5(tepig, snivy, tepig.moves[3]))