from math import ceil
import damage5
import formulas
import movedex
import pokemon
import speciedex

def atk_damage_range(filename, gen, name, gender, level, nature, ability, hp, atk, Def, spatk, spdef, spd):
    output_file = "DamageRange_Atk_{}_{}_{}_{}_{}_{}_{}_{}.csv".format(name, nature, hp, atk, Def, spatk, spdef, spd)
    with open(filename, "r") as f, open(output_file, "w") as i:
        f.readline()
        i.write("BATTLE,DEF_NAME,MOVE_NAME,DEF_STAGE,ATK_STAGE,DAMAGE_RANGE,DEF_HP,MIN_TURNS,MAX_TURNS,CRIT,"\
                "HP_BOOST,ITEM,SCREEN,WEATHER,EVS,ATK_STAT,DEF_STAT,TOTAL_EXP,LEVEL,POKERUS\n")
        last_battle = -1
        battle_num = 0
        atk_pkmn = pokemon.Pokemon(gen, name, gender, level, nature, ability, "", "", "", "", "", hp, atk, Def, spatk, spdef, spd)
        
        for lines in f:
            info = lines.strip().split(",")
            
            battle_num = info[0]
            battle_type = info[1].upper()
            num_poke = int(info[2])
            trainer = True if battle_type != "WILD" else False
            n = 0
            
            #Information which changes for each battle
            if last_battle != battle_num:
                last_battle = battle_num
                screens = [""]
                weathers = list(set([info[3].upper()] + update_weather(atk_pkmn, [])))
                location = info[4]
                atk_pkmn.pokerus = bool(info[33])
                #Change the user pokemon specie if it has evolved or was switched
                if atk_pkmn.species.name != info[21].upper():
                    atk_pkmn.species = speciedex.all.dex[int(gen)][info[21].upper()]
                    atk_pkmn.update_stats()
                atk_stage, def_stage, spatk_stage, spdef_stage, spd_stage = 0, 0, 0, 0, 0
                atk_pkmn.boost = [0, 0, 0, 0, 0, 0]
                max_atk, min_atk, max_def, min_def  = 0, 0, 0, 0
                name = []
            
            #Updates user pokémon item, moves, happiness value and rare candy usage
            atk_pkmn.item = info[22].upper()
            atk_pkmn.moves = [movedex.all.dex[gen][x.upper()] for x in [info[23], info[24], info[25], info[26]] if x != ""]
            for x in range(int(info[32])):
                atk_pkmn.rare_candy()
            atk_pkmn.happiness = int(info[34])
                
            #Creates defending pokemon
            def_pkmn = pokemon.Pokemon(gen, info[5], info[6], int(info[7]), info[8], info[9], info[10], info[11].upper(), info[12].upper(), info[13].upper(), info[14].upper(),
                                       int(info[15]), int(info[16]), int(info[17]), int(info[18]), int(info[19]), int(info[20]))
            
            #Updates weather and screen based on defending moves
            weathers =  update_weather(def_pkmn, weathers)
            screens = update_screen(def_pkmn, screens)
            
            #updates stages
            atk_stage += int(info[27])
            def_stage += int(info[28])
            spatk_stage += int(info[29])
            spdef_stage += int(info[30])
            spd_stage += int(info[30])
            
            #Loop to calculate damage ranges
            for move in atk_pkmn.moves:
                ability = atk_pkmn.ability
                category = move.category
                hps = [atk_pkmn.stat[0]]
                hp_boost = False
                type = move.type.name
                n += 1
                
                if def_pkmn.ability == "INTIMIDATE" and n == 1:
                    name.append(def_pkmn.species.name)
                
                if category == "STATUS":
                    continue
                elif category == "PHYSICAL":
                    max_atk = 2 if check_mod_atk(atk_pkmn, True) else atk_stage
                    min_atk = min(len(name) * -1, -2 if check_mod_atk(def_pkmn, False) else 0)
                    max_def = 0
                    min_def = -2 if check_mod_def(atk_pkmn, False) else 0
                else:
                    max_atk = spatk_stage
                    min_atk = 0
                    max_def = 0
                    min_def = 0
                if (ability == "BLAZE" and type == "FIRE") or (ability == "OVERGROW" and type == "GRASS") or (ability == "SWARM" and type == "BUG") or (ability == "TORRENT" and type == "WATER"):
                   boost = hps.append(1)
                   hp_boost = True
                   
                for crit in (False, True):
                    for hp in hps:
                        atk_pkmn.hp = hp
                        for def_mod in range(min_def, max_def + 1):
                            if category == "PHYSICAL":
                                def_pkmn.boost[2] = def_mod
                            else:
                                def_pkmn.boost[4] = def_mod
                            if crit and def_mod > 0:
                                continue
                            for atk_mod in range(min_atk, max_atk + 1):
                                if category == "PHYSICAL":
                                    atk_pkmn.boost[1] = atk_mod
                                else:
                                    atk_pkmn.boost[3] = atk_mod
                                if crit and atk_mod < 0:
                                    continue
                                for screen in screens:
                                    if screen == "LIGHT SCREEN" and (category == "PHYSICAL" or crit or move.name == "BRICK BREAK"):
                                        continue
                                    elif screen == "REFLECT" and (category == "SPECIAL" or crit or move.name == "BRICK BREAK"):
                                        continue
                                    for weather in weathers:
                                        if weather in ("SUNNY DAY", "RAIN DANCE") and type not in ("WATER", "FIRE"):
                                            continue
                                        elif weather == "SANDSTORM" and (category == "PHYSICAL" or type != "ROCK"):
                                            continue
                                        elif weather == "HAIL" and move.name != "SOLARBEAM":
                                            continue
                                        for damage_range in damage5.damage5(atk_pkmn, def_pkmn, move, battle_type, screen, crit, weather):
                                            if damage_range != [0]:
                                                dmg = "-".join([str(value) for value in damage_range])
                                                min_turns = ceil(def_pkmn.hp / max(damage_range))
                                                max_turns = ceil(def_pkmn.hp / min(damage_range))
                                                i.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"\
                                                .format(battle_num, def_pkmn.species.name, move.name, def_mod, atk_mod,
                                                        dmg, def_pkmn.hp, min_turns, max_turns, crit, True if hp == 1 else False, atk_pkmn.item, screen, weather,
                                                        "-".join([str(x) for x in atk_pkmn.ev]), 
                                                        "-".join([str(x) for x in atk_pkmn.stat]), "-".join([str(x) for x in def_pkmn.stat]), 
                                                        atk_pkmn.exp, atk_pkmn.level, atk_pkmn.pokerus))
            
            atk_pkmn.update_exp(formulas.calc_exp(gen, def_pkmn.level, def_pkmn.species.base_exp, trainer, num_poke, atk_pkmn.level, atk_pkmn.item))
            atk_pkmn.update_evs(def_pkmn.species.ev_yield)
            atk_pkmn.update_level()

def def_damage_range(filename, gen, name, gender, level, nature, ability, hp, atk, Def, spatk, spdef, spd):
    output_file = "DamageRange_Def_{}_{}_{}_{}_{}_{}_{}_{}.csv".format(name, nature, hp, atk, Def, spatk, spdef, spd)
    with open(filename, "r") as f, open(output_file, "w") as i:
        f.readline()
        i.write("BATTLE,ATK_NAME,MOVE_NAME,DEF_STAGE,ATK_STAGE,DAMAGE_RANGE,DEF_HP,MIN_TURNS,MAX_TURNS,CRIT,"\
                "HP_BOOST,ITEM,SCREEN,WEATHER,EVS,ATK_STAT,DEF_STAT,TOTAL_EXP,LEVEL,POKERUS\n")
        last_battle = -1
        battle_num = 0
        def_pkmn = pokemon.Pokemon(gen, name, gender, level, nature, ability, "", "", "", "", "", hp, atk, Def, spatk, spdef, spd)
        
        for lines in f:
            info = lines.strip().split(",")
            battle_num = info[0]
            battle_type = info[1].upper()
            num_poke = int(info[2])
            trainer = True if battle_type != "WILD" else False
            n = 0
            
            #Information which changes for each battle
            if last_battle != battle_num:
                last_battle = battle_num
                screens = [""]
                weathers = list(set([info[3].upper()] + update_weather(def_pkmn, [])))
                location = info[4]
                def_pkmn.pokerus = bool(info[33])
                #Change the user pokemon specie if it has evolved or was switched
                if def_pkmn.species.name != info[21].upper():
                    def_pkmn.species = speciedex.all.dex[int(gen)][info[21].upper()]
                    def_pkmn.update_stats()
                atk_stage, def_stage, spatk_stage, spdef_stage, spd_stage = 0, 0, 0, 0, 0
                max_atk, min_atk, max_def, min_def  = 0, 0, 0, 0
                name = []
            
            #Updates user pokémon item, moves, happiness value and rare candy usage
            def_pkmn.item = info[22].upper()
            def_pkmn.moves = [movedex.all.dex[gen][x.upper()] for x in [info[23], info[24], info[25], info[26]] if x != ""]
            for x in range(int(info[32])):
                def_pkmn.rare_candy()
            def_pkmn.happiness = int(info[34])
                
            #Creates defending pokemon
            atk_pkmn = pokemon.Pokemon(gen, info[5], info[6], int(info[7]), info[8], info[9], info[10], info[11].upper(), info[12].upper(), info[13].upper(), info[14].upper(),
                                       int(info[15]), int(info[16]), int(info[17]), int(info[18]), int(info[19]), int(info[20]))
            
            #Updates weather and screen based on defending moves
            weathers =  update_weather(atk_pkmn, weathers)
            screens = update_screen(atk_pkmn, screens)
            
            #Loop to calculate damage ranges
            for move in atk_pkmn.moves:
                ability = atk_pkmn.ability
                category = move.category
                hps = [atk_pkmn.stat[0]]
                hp_boost = False
                type = move.type.name
                n += 1
                
                if def_pkmn.ability == "INTIMIDATE" and n == 1:
                    name.append(def_pkmn.species.name)
                
                if category == "STATUS":
                    continue
                elif category == "PHYSICAL":
                    max_atk = 2 if check_mod_atk(atk_pkmn, True) else atk_stage
                    min_atk = min(len(name) * -1, -2 if check_mod_atk(def_pkmn, False) else 0)
                    max_def = 0
                    min_def = -2 if check_mod_def(atk_pkmn, False) else 0
                else:
                    max_atk = spatk_stage
                    min_atk = 0
                    max_def = 0
                    min_def = 0
                if (ability == "BLAZE" and type == "FIRE") or (ability == "OVERGROW" and type == "GRASS") or (ability == "SWARM" and type == "BUG") or (ability == "TORRENT" and type == "WATER"):
                   boost = hps.append(1)
                   hp_boost = True
                   
                for crit in (False, True):
                    for hp in hps:
                        atk_pkmn.hp = hp
                        for def_mod in range(min_def, max_def + 1):
                            if category == "PHYSICAL":
                                def_pkmn.boost[2] = def_mod
                            else:
                                def_pkmn.boost[4] = def_mod
                            if crit and def_mod > 0:
                                continue
                            for atk_mod in range(min_atk, max_atk + 1):
                                if category == "PHYSICAL":
                                    atk_pkmn.boost[1] = atk_mod
                                else:
                                    atk_pkmn.boost[3] = atk_mod
                                if crit and atk_mod < 0:
                                    continue
                                for screen in screens:
                                    if screen == "LIGHT SCREEN" and (category == "PHYSICAL" or crit or move.name == "BRICK BREAK"):
                                        continue
                                    elif screen == "REFLECT" and (category == "SPECIAL" or crit or move.name == "BRICK BREAK"):
                                        continue
                                    for weather in weathers:
                                        if weather in ("SUNNY DAY", "RAIN DANCE") and type not in ("WATER", "FIRE"):
                                            continue
                                        elif weather == "SANDSTORM" and (category == "PHYSICAL" or type != "ROCK"):
                                            continue
                                        elif weather == "HAIL" and move.name != "SOLARBEAM":
                                            continue
                                        for damage_range in damage5.damage5(atk_pkmn, def_pkmn, move, battle_type, screen, crit, weather):
                                            if damage_range != [0]:
                                                dmg = "-".join([str(value) for value in damage_range])
                                                min_turns = ceil(def_pkmn.hp / max(damage_range))
                                                max_turns = ceil(def_pkmn.hp / min(damage_range))
                                                i.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"\
                                                .format(battle_num, atk_pkmn.species.name, move.name, def_mod, atk_mod,
                                                        dmg, def_pkmn.hp, min_turns, max_turns, crit, True if hp == 1 else False, atk_pkmn.item, screen, weather,
                                                        "-".join([str(x) for x in def_pkmn.ev]), 
                                                        "-".join([str(x) for x in atk_pkmn.stat]), "-".join([str(x) for x in def_pkmn.stat]), 
                                                        def_pkmn.exp, def_pkmn.level, def_pkmn.pokerus))
            
            def_pkmn.update_exp(formulas.calc_exp(gen, atk_pkmn.level, atk_pkmn.species.base_exp, trainer, num_poke, def_pkmn.level, def_pkmn.item))
            def_pkmn.update_evs(atk_pkmn.species.ev_yield)
            def_pkmn.update_level()
            
def update_screen(pkmn, screen):
    ls = "LIGHT SCREEN"
    reflect = "REFLECT"
    
    if ls in [x.name for x in pkmn.moves]:
        screen.append(ls)
    
    if reflect in [x.name for x in pkmn.moves]:
        screen.append(reflect)
    
    return list(set(screen))

def update_weather(pkmn, weather):
    sun = "SUNNY DAY"
    rain = "RAIN DANCE"
    sandstorm = "SANDSTORM"
    hail = "HAIL"
    
    if sun in [x.name for x in pkmn.moves]:
        weather.append(sun)
    
    if rain in [x.name for x in pkmn.moves]:
        weather.append(rain)
        
    if hail in [x.name for x in pkmn.moves]:
        weather.append(hail)
        
    if sandstorm in [x.name for x in pkmn.moves]:
        weather.append(sandstorm)
    
    return list(set(weather))

#To do: Swagger boost target 
#       Superpower drops user
def check_mod_atk(pkmn, boost):
    if boost:
        info = {"ANCIENTPOWER", "ACUPRESSURE", "BELLY DRUM", "BULK UP", "CURSE",
                 "DRAGON DANCE", "HOWL", "MEDITATE", "METAL CLAW", "METEOR MASH",
                 "OMINOUS WIND", "RAGE", "SHARPEN", "SILVER WIND", "SWORDS DANCE",
                 "WORK UP"}
    else:
        info = {"AURORA BEAM", "CHARM", "FEATHERDANCE", "GROWL", "MEMENTO",
                "SECRET POWER", "SUPERPOWER", "TICKLE"}
             
    for moves in [x.name for x in pkmn.moves]:
        if moves in info:
            return True

#To do: Close Combat/Superpower drops user
def check_mod_def(pkmn, boost):
    if boost:
        info = {"ACID ARMOR", "ANCIENTPOWER", "ACUPRESSURE", "BARRIER", "BULK UP",
                "COSMIC POWER", "CURSE", "DEFEND ORDER", "DEFENSE CURL", "HARDEN",
                "IRON DEFENSE", "OMINOUS WIND", "SILVER WIND", "SKULL BASH",
                "STEEL WING", "STOCKPILE", "WITHDRAW"}
    else:
        info = {"CRUNCH", "CRUSH CLAW", "IRON TAIL", "LEER", "ROCK SMASH", 
                "SCREECH", "TAIL WHIP", "TICKLE"}
    
    for moves in [x.name for x in pkmn.moves]:
        if moves in info:
            return True

#To do: Flatter boost target
#       Draco Meteor/Leaf Storm/Overheat/Psycho Boost drops user
def check_mod_spatk(pkmn, boost):
    if boost:
        info = {"AncientPower", "Acupressure", "Calm Mind", "Charge Beam",
                "Growth", "Nasty Plot", "Ominous Wind", "Silver Wind",
                "Tail Glow"}
    else:
        info = {"Captivate", "Memento", "Mist Ball"}
    
    for moves in [x.name for x in pkmn.moves]:
        if moves in info:
            return True
            
#To do: Close Combat drops user
def check_mod_spdef(pkmn, boost):
    if boost:
        info = {"Amnesia", "AncientPower", "Acupressure", "Calm Mind", "Charge",
                "Cosmic Power", "Defend Order", "Ominous Wind", "Silver Wind",
                "Stockpile"}
    else:
        info = {"Acid", "Bug Buzz", "Earth Power", "Energy Ball", "Fake Tears",
                "Flash Cannon", "Focus Blast", "Luster Purge", "Metal Sound",
                "Psychic", "Shadow Ball", "Seed Flare"}
    
    for moves in [x.name for x in pkmn.moves]:
        if moves in info:
            return True
            
atk_damage_range("Battles_B_Tepig.csv", 5, "Tepig", "Male", 5, "Adamant", "Blaze", 30, 30, 30, 30, 30, 30)
def_damage_range("Battles_B_Tepig.csv", 5, "Tepig", "Male", 5, "Adamant", "Blaze", 30, 30, 30, 30, 30, 30)