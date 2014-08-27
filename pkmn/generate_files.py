import formulas
import pokemon

def calc_user_info(gen, name, filename):
    dex = pokedex.Pokedex()
    group = exp_group.ExpGroup()
    with open(filename, "r") as route, open("info.csv", "w") as user_info:
        route.readline()
        user_info.write("Battle,Name,Level,Exp,HP EV,Atk EV,Def EV,"
                        "Sp.Atk EV,Sp.Def EV,Spd EV,HP,Atk,Def,Sp.Atk,"
                        "Sp.Def,Spd\n")
        user_specie = dex.dex[int(gen)][name.upper()]
        user_group = user_specie.exp_group
        user_level = 5
        exp = group.group[user_group][user_level - 1]
        user = pokemon.Pokemon(user_specie, "Male", user_level, "Mild", "", "",
                               "", "", "", "", 25, 31, 31, 31, 30, 31, 0, 0, 0,
                               0, 0, 0)
        for lines in route:
            info = lines.strip().split(",")
            
            if user.species.name != info[3]:
                user.species = dex.dex[int(gen)][info[3]]
                user.update_stats()
            try:
                battle_num = info[0]
                foe_name = info[1]
                foe_level = int(info[2])
                foe = dex.dex[gen][foe_name]
                
                stuff = [battle_num,foe_name,str(user.level),str(user.exp)] +\
                        [str(x) for x in user.ev] + [str(x) for x in user.stat]
                
                user.update_exp(formulas.calc_exp(foe.gen, foe_level, 
                                                  foe.base_exp))
                user_level = exp_group.calc_level(user_group, user.exp, 
                                                  user_level)
                user.update_evs(foe.ev_yield)
                
                if user_level != user.level:
                    for x in range(user_level - user.level):
                        user.update_level()
                
                user_info.write(",".join(stuff)+"\n")
            except ValueError:
                if info[0] == "Rare Candy":
                    user.update_level()
                    user.exp = group.group[user.species.exp_group][user.level - 1]
                    
def damage_range(gen, filename):
    with open(filename, "r") as f, open("dmg_rng.csv", "w") as i:
        f.readline()
        for lines in f:
            info = lines.strip().split(",")
            
            battle_num = info[0]
            battle_type = info[1]
            weather = info[2]
            location = info[3]
            
            def_specie, atk_specie = info[4].upper(), info[26].upper()
            def_gender, atk_gender = info[5], info[27]
            def_level, atk_level = int(info[6]), int(info[28])
            def_nature, atk_nature = info[7], info[29]
            def_ability, atk_ability = info[8], info[30]
            def_item, atk_item = info[9], info[31]
            def_move1, atk_move1 = info[10], info[32]
            def_move2, atk_move2 = info[11], info[33]
            def_move3, atk_move3 = info[12], info[34]
            def_move4, atk_move4 = info[13], info[35]
            def_hp_iv, atk_hp_iv = int(info[14]), int(info[36])
            def_atk_iv, atk_atk_iv = int(info[15]), int(info[37])
            def_def_iv, atk_def_iv = int(info[16]), int(info[38])
            def_spatk_iv, atk_spatk_iv = int(info[17]), int(info[39])
            def_spdef_iv, atk_spdef_iv = int(info[18]), int(info[40])
            def_spd_iv, atk_spd_iv = int(info[19]), int(info[41])
            def_hp_ev, atk_hp_ev = int(info[20]), int(info[42])
            def_atk_ev, atk_atk_ev = int(info[21]), int(info[43])
            def_def_ev, atk_def_ev = int(info[22]), int(info[44])
            def_spatk_ev, atk_spatk_ev = int(info[23]), int(info[45])
            def_spdef_ev, atk_spdef_ev = int(info[24]), int(info[46])
            def_spd_ev, atk_spd_ev = int(info[25]), int(info[47])
            
            atk_pkmn = pokemon.Pokemon(gen, atk_specie, atk_gender,
                                       atk_level, atk_nature, atk_ability,
                                       atk_item, atk_move1, atk_move2,
                                       atk_move3, atk_move4, atk_hp_iv,
                                       atk_atk_iv, atk_def_iv, atk_spatk_iv,
                                       atk_spdef_iv, atk_spd_iv, atk_hp_ev,
                                       atk_atk_ev, atk_def_ev, atk_spatk_ev,
                                       atk_spdef_ev, atk_spd_ev)
            
            def_pkmn = pokemon.Pokemon(gen, def_specie, def_gender,
                                       def_level, def_nature, def_ability,
                                       def_item, def_move1, def_move2,
                                       def_move3, def_move4, def_hp_iv,
                                       def_atk_iv, def_def_iv, def_spatk_iv,
                                       def_spdef_iv, def_spd_iv)
            
            for x in range(len(atk_pkmn.moves)):
                dmg1 = formulas.calc_damage(atk_pkmn, def_pkmn, atk_pkmn.moves[x], False,
                                           weather, set(), battle_type, location)
                dmg2 = "-".join([str(x) for x in dmg1])
                i.write("{},{},{},{},{},{}\n".format(battle_num, def_specie, atk_pkmn.moves[x].name, atk_pkmn.item, weather, dmg2))

damage_range(4, "battles.csv")