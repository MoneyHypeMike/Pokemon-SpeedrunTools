from math import ceil
import formulas
import movedex
import pokemon
import speciedex

def atk_damage_range(filename, gen, name, level, nature, ability, hp, atk, Def, spatk, spdef, spd):
    output_file = "DamageRange_Atk_{}_{}_{}_{}_{}_{}_{}_{}.csv".format(name, nature, hp, atk, Def, spatk, spdef, spd)
    with open(filename, "r") as f, open(output_file, "w") as i:
        f.readline()
        i.write("Battle,Def_Name,Move Used,Def_Modifier,"\
                "Atk_Modifier,Damage_Range,HP,Min_Turns,"\
                "Max_Turns,Crit,Torrent,Item,Screen,Weather,"\
                "EVs,Atk_Stat,Def_Stat,Total_Exp,Level,Pokerus\n")
        last_battle = "0"
        
        atk_pkmn = pokemon.Pokemon(gen, name.upper(), "Male", level, nature,
                                   ability, "None", "None", "None", "None",
                                   "None", hp, atk, Def, spatk, spdef, spd)
        
        for lines in f:
            info = lines.strip().split(",")
            
            #Stores file information into variables
            battle_num = info[0]
            battle_type = info[1].split("\\")[0]
            location = info[3]
            
            #Reset the weather, screen and stat modifiers for a new battle
            if last_battle != battle_num:
                last_battle = battle_num
                weathers = [info[2]]
                screens = ["None"]
                min_mod_atk = 0
                max_mod_atk = int(info[32])
                min_mod_spatk = 0
                max_mod_spatk = int(info[33])
                min_mod_def = 0
                max_mod_def = 0
                min_mod_spdef = 0
                max_mod_spdef = 0
                min_def = 0
                max_def = 0
                max_atk = 0
                min_atk = 0
                poke_num = 0
                trainer = True
                
            #Change the pokemon specie if it evolved or was switched
            if atk_pkmn.species.name != info[26].upper():
                if atk_pkmn.species.dex_num + 1 == speciedex.all.dex[gen][info[26].upper()].dex_num:
                    atk_pkmn.species = speciedex.all.dex[int(gen)][info[26].upper()]
                    atk_pkmn.update_stats()
                else:
                    atk_pkmn = pokemon.Pokemon(gen, info[26].upper(), "Male", 40, "Rash",
                                   "Pressure", "None", "None", "None", "None",
                                   "None", 19, 24, 29, 26, 22, 27)
            
            #Use Rare Candy
            if info[34] != "0":
                for x in range(int(info[34])):
                    atk_pkmn.rare_candy()
            
            if info[37] == "TRUE":
                atk_pkmn.pokerus = True
            else:
                atk_pkmn.pokerus = False
            
            #Stores file information into variables
            def_specie = info[4].upper()
            def_gender = info[5]
            def_level = int(info[6])
            def_nature = info[7]
            def_ability = info[8]
            def_item = info[9]
            def_move1 = info[10]
            def_move2 = info[11]
            def_move3 = info[12]
            def_move4 = info[13]
            def_hp_iv = int(info[14])
            def_atk_iv = int(info[15])
            def_def_iv = int(info[16])
            def_spatk_iv = int(info[17])
            def_spdef_iv = int(info[18])
            def_spd_iv = int(info[19])
            def_hp_ev = int(info[20])
            def_atk_ev = int(info[21])
            def_def_ev = int(info[22])
            def_spatk_ev = int(info[23])
            def_spdef_ev = int(info[24])
            def_spd_ev = int(info[25])
            atk_pkmn.moves = [movedex.all.dex[gen][x] for x in [info[28], info[29], info[30], info[31]] if x != "None"]
            atk_pkmn.update_item(info[27])
            
            #Creates defending pokemon
            def_pkmn = pokemon.Pokemon(gen, def_specie, def_gender,
                                       def_level, def_nature, def_ability,
                                       def_item, def_move1, def_move2,
                                       def_move3, def_move4, def_hp_iv,
                                       def_atk_iv, def_def_iv, def_spatk_iv,
                                       def_spdef_iv, def_spd_iv)
            
            #Updates weather and screen based on defending moves
            weathers =  list(set(weathers + update_weather(def_pkmn) + update_weather(atk_pkmn)))
            screens = list(set(screens + update_screen(def_pkmn)))
            
            #Checks if the attacking pokemon has an hp boosting ability for the loop
            if atk_pkmn.ability in {"Blaze", "Torrent", "Overgrow", "Swarm"}:
                hp = (atk_pkmn.stat[0], 1)
                hp_boost = True
            else:
                hp = (1,)
                hp_boost = False
            
            #Updates item and stat modifiers variables for the loop
            if atk_pkmn.item == "None":
                items = ("None",)
            else:
                items = ("None", atk_pkmn.item)
            
            if int(info[32]) > max_mod_atk:
                max_mod_atk += int(info[32])
            
            if int(info[33]) > max_mod_spatk:
                max_mod_spatk += int(info[33])
            
            if check_mod_def(def_pkmn, True):
                max_mod_def = 6
            else:
                max_mod_def = 0
            
            if check_mod_def(atk_pkmn, False):
                min_mod_def = -6
            else:
                min_mod_def = 0
            
            if check_mod_spdef(def_pkmn, True):
                max_mod_spdef = 6
            else:
                max_mod_spdef = 0
                
            if check_mod_atk(def_pkmn, False) and min_mod_atk != -6:
                min_mod_atk = -6
                
            if check_mod_spatk(def_pkmn, False) and min_mod_spatk != -6:
                min_mod_spatk = -6
            
            #Loop to calculate damage ranges
            for move in atk_pkmn.moves:
                if move.category == "Status":
                    continue
                elif move.category == "Special":
                    max_atk = max_mod_spatk
                    min_atk = min_mod_spatk
                    max_def = max_mod_spdef
                    min_def = min_mod_spdef
                elif move.category == "Physical":
                    max_atk = max_mod_atk
                    min_atk = min_mod_atk
                    max_def = max_mod_def
                    min_def = min_mod_def
                for crit in (False, True):
                    for hp_value in hp:
                        if hp_boost:
                            atk_pkmn.hp = hp_value
                            torrent = True if atk_pkmn.calc_hp_ratio() <= 33 else False
                            if torrent and atk_pkmn.ability == "Blaze" and move.type.name != "FIRE":
                                continue
                            elif torrent and atk_pkmn.ability == "Torrent" and move.type.name != "WATER":
                                continue
                            elif torrent and atk_pkmn.ability == "Overgrow" and move.type.name != "GRASS":
                                continue
                            elif torrent and atk_pkmn.ability == "Swarm" and move.type.name != "BUG":
                                continue
                            else:
                                torrent = False
                        for item in items:
                            atk_pkmn.item = item
                            if item == "Choice Specs" and move.category != "Special":
                                continue
                            elif item == "Fist Plate" and move.type.name != "FIGHTING":
                                continue
                            for def_mod in range(min_def, max_def + 1):
                                if crit and def_mod > 0:
                                    continue
                                for atk_mod in range(min_atk, max_atk + 1):
                                    if crit and atk_mod < 0:
                                        continue
                                    for screen in screens:
                                        if screen == "Light Screen" and move.category == "Physical":
                                            continue
                                        elif screen == "Reflect" and move.category == "Special":
                                            continue
                                        for weather in weathers:
                                            if weather == "Sunny Day" and move.type.name not in {"WATER", "FIRE"} and weather != "Normal" and len(weathers) > 1:
                                                continue
                                            elif weather == "Rain Dance" and move.type.name not in {"WATER", "FIRE"} and weather != "Normal" and len(weathers) > 1:
                                                continue
                                            elif weather == "Hail" and move.name != "SolarBeam":
                                                continue
                                            elif weather == "Sandstorm" and move.category == "Physical" and move.name != "SolarBeam":
                                                continue
                                            elif weather == "Sandstorm" and "ROCK" not in [x.name for x in def_pkmn.species.types] and weather != "Normal" and len(weathers) > 1:
                                                continue
                                            for damage_range in formulas.calc_damage(atk_pkmn, def_pkmn, move, atk_mod, def_mod, crit, weather, screen, battle_type, location):
                                                if max(damage_range) != 0:
                                                    dmg = "-".join([str(value) for value in damage_range])
                                                    min_turns = ceil(def_pkmn.hp / max(damage_range))
                                                    max_turns = ceil(def_pkmn.hp / min(damage_range))
                                                    i.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"\
                                                    .format(battle_num, def_specie, move.name, def_mod, atk_mod,
                                                            dmg, def_pkmn.hp, min_turns, max_turns, 
                                                            crit, torrent, item, screen, weather,"-".join([str(x) for x in atk_pkmn.ev]), 
                                                            "-".join([str(x) for x in atk_pkmn.stat]), "-".join([str(x) for x in def_pkmn.stat]), 
                                                            atk_pkmn.exp, atk_pkmn.level, atk_pkmn.pokerus))
            if battle_type == "Single":
                poke_num = 1
                trainer = True
            elif battle_type == "Double":
                poke_num = int(info[1].split("\\")[1])
                trainer = True
            else:
                poke_num = 1
                trainer = False
            
            atk_pkmn.update_exp(formulas.calc_exp(gen, def_level, def_pkmn.species.base_exp, trainer, poke_num))
            atk_pkmn.update_evs(def_pkmn.species.ev_yield)
            atk_pkmn.update_level()

def def_damage_range(filename, gen, name, level, nature, ability, hp, atk, Def, spatk, spdef, spd):
    output_file = "DamageRange_Def_{}_{}_{}_{}_{}_{}_{}_{}.csv".format(name, nature, hp, atk, Def, spatk, spdef, spd)
    with open(filename, "r") as f, open(output_file, "w") as i:
        f.readline()
        i.write("Battle,Def_Name,Move Used,Def_Modifier,"\
                "Atk_Modifier,Damage_Range,HP,Min_Turns,"\
                "Max_Turns,Crit,Torrent,Item,Screen,Weather,"\
                "EVs,Atk_Stat,Def_Stat,Total_Exp,Level,Pokerus\n")
        last_battle = "0"
        
        atk_pkmn = pokemon.Pokemon(gen, name.upper(), "Male", level, nature,
                                   ability, "None", "None", "None", "None",
                                   "None", hp, atk, Def, spatk, spdef, spd)
        
        for lines in f:
            info = lines.strip().split(",")
            
            #Stores file information into variables
            battle_num = info[0]
            battle_type = info[1].split("\\")[0]
            location = info[3]
            
            #Reset the weather, screen and stat modifiers for a new battle
            if last_battle != battle_num:
                last_battle = battle_num
                weathers = [info[2]]
                screens = ["None"]
                min_mod_atk = 0
                max_mod_atk = int(info[32])
                min_mod_spatk = 0
                max_mod_spatk = int(info[33])
                min_mod_def = 0
                max_mod_def = 0
                min_mod_spdef = 0
                max_mod_spdef = 0
                min_def = 0
                max_def = 0
                max_atk = 0
                min_atk = 0
                poke_num = 0
                trainer = True
            
            #Change the pokemon specie if it evolved or was switched
            if atk_pkmn.species.name != info[26].upper():
                atk_pkmn.species = speciedex.all.dex[int(gen)][info[26].upper()]
                atk_pkmn.update_stats()
            
            #Use Rare Candy
            if info[34] != "0":
                for x in range(int(info[34])):
                    atk_pkmn.rare_candy()
            
            if info[37] == "TRUE":
                atk_pkmn.pokerus = True
            else:
                atk_pkmn.pokerus = False
            
            #Stores file information into variables
            def_specie = info[4].upper()
            def_gender = info[5]
            def_level = int(info[6])
            def_nature = info[7]
            def_ability = info[8]
            def_item = info[9]
            def_move1 = info[10]
            def_move2 = info[11]
            def_move3 = info[12]
            def_move4 = info[13]
            def_hp_iv = int(info[14])
            def_atk_iv = int(info[15])
            def_def_iv = int(info[16])
            def_spatk_iv = int(info[17])
            def_spdef_iv = int(info[18])
            def_spd_iv = int(info[19])
            def_hp_ev = int(info[20])
            def_atk_ev = int(info[21])
            def_def_ev = int(info[22])
            def_spatk_ev = int(info[23])
            def_spdef_ev = int(info[24])
            def_spd_ev = int(info[25])
            atk_pkmn.moves = [movedex.all.dex[gen][x] for x in [info[28], info[29], info[30], info[31]] if x != "None"]
            atk_pkmn.update_item(info[27])
            
            #Creates defending pokemon
            def_pkmn = pokemon.Pokemon(gen, def_specie, def_gender,
                                       def_level, def_nature, def_ability,
                                       def_item, def_move1, def_move2,
                                       def_move3, def_move4, def_hp_iv,
                                       def_atk_iv, def_def_iv, def_spatk_iv,
                                       def_spdef_iv, def_spd_iv)
            
            #Updates weather and screen based on defending moves
            weathers =  list(set(weathers + update_weather(def_pkmn) + update_weather(atk_pkmn)))
            screens = list(set(screens + update_screen(atk_pkmn)))
            
            #Checks if the attacking pokemon has an hp boosting ability for the loop
            if def_pkmn.ability in {"Blaze", "Torrent", "Overgrow", "Swarm"}:
                hp = (def_pkmn.stat[0], 1)
                hp_boost = True
            else:
                hp = (1,)
                hp_boost = False
            
            #Updates item and stat modifiers variables for the loop
            if def_pkmn.item == "None":
                items = ("None",)
            else:
                items = ("None", def_pkmn.item)
            
            if int(info[35]) > max_mod_def:
                max_mod_def = int(info[35])
            
            if int(info[36]) > max_mod_spdef:
                max_mod_spdef += int(info[36])
            
            if check_mod_atk(def_pkmn, True):
                max_mod_atk = 6
            else:
                max_mod_atk = 0
            
            if check_mod_spatk(def_pkmn, True):
                max_mod_spatk = 6
            else: 
                max_mod_spatk = 0
            
            if check_mod_atk(atk_pkmn, False):
                min_mod_atk = -6
            else:
                min_mod_atk = 0
            
            if check_mod_spatk(atk_pkmn, False):
                min_mod_spatk = -6
            else:
                mind_mod_spatk = 0
            
            if check_mod_def(atk_pkmn, True) and max_mod_def != 6:
                max_mod_def = 6
                
            #if check_mod_def(atk_pkmn, False) and min_mod_def !=-6:
            #    min_mod_def = -6
            
            if check_mod_spdef(atk_pkmn, True) and max_mod_spdef != 6:
                max_mod_spdef = 6
                
            #if check_mod_spdef(atk_pkmn, False) and min_mod_spdef != -6:
            #    min_mod_spdef = -6
            
            #Loop to calculate damage ranges
            for move in def_pkmn.moves:
                if move.category == "Status":
                    continue
                elif move.category == "Special":
                    max_atk = max_mod_spatk
                    min_atk = min_mod_spatk
                    max_def = max_mod_spdef
                    min_def = min_mod_spdef
                elif move.category == "Physical":
                    max_atk = max_mod_atk
                    min_atk = min_mod_atk
                    max_def = max_mod_def
                    min_def = min_mod_def
                for crit in (False, True):
                    for hp_value in hp:
                        if hp_boost:
                            def_pkmn.hp = hp_value
                            torrent = True if def_pkmn.calc_hp_ratio() <= 33 else False
                            if torrent and def_pkmn.ability == "Blaze" and move.type.name != "FIRE":
                                continue
                            elif torrent and def_pkmn.ability == "Torrent" and move.type.name != "WATER":
                                continue
                            elif torrent and def_pkmn.ability == "Overgrow" and move.type.name != "GRASS":
                                continue
                            elif torrent and def_pkmn.ability == "Swarm" and move.type.name != "BUG":
                                continue
                        else:
                            torrent = False
                        for item in items:
                            def_pkmn.item = item
                            if item in {"Sitrus Berry", "Oran Berry"}:
                                continue
                            for def_mod in range(min_def, max_def + 1):
                                if crit and def_mod > 0:
                                    continue
                                for atk_mod in range(min_atk, max_atk + 1):
                                    if crit and atk_mod < 0:
                                        continue
                                    for screen in screens:
                                        if screen == "Light Screen" and move.category == "Physical":
                                            continue
                                        elif screen == "Reflect" and move.category == "Special":
                                            continue
                                        for weather in weathers:
                                            if weather == "Sunny Day" and move.type.name not in {"WATER", "FIRE"} and weather != "Normal" and len(weathers) > 1:
                                                continue
                                            elif weather == "Rain Dance" and move.type.name not in {"WATER", "FIRE"} and weather != "Normal" and len(weathers) > 1:
                                                continue
                                            elif weather == "Hail" and move.name != "SolarBeam":
                                                continue
                                            elif weather == "Sandstorm" and move.category == "Physical" and move.name != "SolarBeam":
                                                continue
                                            elif weather == "Sandstorm" and "ROCK" not in [x.name for x in def_pkmn.species.types] and weather != "Normal" and len(weathers) > 1:
                                                continue
                                            for damage_range in formulas.calc_damage(def_pkmn, atk_pkmn, move, atk_mod, def_mod, crit, weather, screen, battle_type, location):
                                                if max(damage_range) != 0:
                                                    dmg = "-".join([str(value) for value in damage_range])
                                                    min_turns = ceil(def_pkmn.hp / max(damage_range))
                                                    max_turns = ceil(def_pkmn.hp / min(damage_range))
                                                    i.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n"\
                                                    .format(battle_num, def_specie, move.name, def_mod, atk_mod,
                                                            dmg, atk_pkmn.stat[0], min_turns, max_turns,
                                                            crit, torrent, item, screen, weather,"-".join([str(x) for x in atk_pkmn.ev]), 
                                                            "-".join([str(x) for x in atk_pkmn.stat]), "-".join([str(x) for x in def_pkmn.stat]),
                                                            atk_pkmn.exp, atk_pkmn.level, atk_pkmn.pokerus))
            
            if battle_type == "Single":
                poke_num = 1
                trainer = True
            elif battle_type == "Double":
                poke_num = int(info[1].split("\\")[1])
                trainer = True
            else:
                poke_num = 1
                trainer = False
            atk_pkmn.update_exp(formulas.calc_exp(gen, def_level, def_pkmn.species.base_exp, trainer, poke_num))
            atk_pkmn.update_evs(def_pkmn.species.ev_yield)
            atk_pkmn.update_level()
            
def update_screen(pkmn):
    screen = []

    if "Light Screen" in [x.name for x in pkmn.moves]:
        screen.append("Light Screen")
    
    if "Reflect" in [x.name for x in pkmn.moves]:
        screen.append("Reflect")
    
    return screen

def update_weather(pkmn):
    weather = []
    sun = "Sunny Day"
    rain = "Rain Dance"
    sandstorm = "Sandstorm"
    hail = "Hail"
    
    if sun in [x.name for x in pkmn.moves]:
        weather.append(sun)
    
    if rain in [x.name for x in pkmn.moves]:
        weather.append(rain)
        
    if hail in [x.name for x in pkmn.moves]:
        weather.append(hail)
        
    if sandstorm in [x.name for x in pkmn.moves]:
        weather.append(sandstorm)
    
    return weather

#To do: Swagger boost target 
#       Superpower drops user
def check_mod_atk(pkmn, boost):
    if boost:
        info = {"AncientPower", "Acupressure", "Belly Drum", "Bulk Up", "Curse",
                 "Dragon Dance", "Howl", "Meditate", "Metal Claw", "Meteor Mash",
                 "Ominous Wind", "Rage", "Sharpen", "Silver Wind", "Swords Dance"}
    else:
        info = {"Aurora Beam", "Charm", "FeatherDance", "Growl", "Memento",
                "Secret Power", "Superpower", "Tickle"}
             
    for moves in [x.name for x in pkmn.moves]:
        if moves in info:
            return True

#To do: Close Combat/Superpower drops user
def check_mod_def(pkmn, boost):
    if boost:
        info = {"Acid Armor", "AncientPower", "Acupressure", "Barrier", "Bulk Up",
                "Cosmic Power", "Curse", "Defend Order", "Defense Curl", "Harden",
                "Iron Defense", "Ominous Wind", "Silver Wind", "Skull Bash",
                "Steel Wing", "Stockpile", "Withdraw"}
    else:
        info = {"Crunch", "Crush Claw", "Iron Tail", "Leer", "Rock Smash", 
                "Screech", "Tail Whip", "Tickle"}
    
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
            
atk_damage_range("Battles_HG_Cyndaquil.csv", 4, "Cyndaquil", 5, "Naive", "Blaze", 28, 29, 28, 30, 25, 31)
#def_damage_range("Battles_HG_Cyndaquil_Any.csv", 4, "Cyndaquil", 5, "Naive", "Blaze", 28, 29, 28, 30, 25, 31)