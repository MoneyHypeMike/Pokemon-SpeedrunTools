import formulas
import pokemon

gen = 4
battle_type = "Single"
weather = "None"
location = "Building"
            
            
atk_pkmn = pokemon.Pokemon(gen, "Empoleon", "Male",
                                       65, "Mild", "Torrent",
                                       "Choice Specs", "Surf", "Strength",
                                       "Waterfall", "Rock Climb", 25,
                                       31, 31, 31,
                                       30, 31, 40,
                                       107, 57, 74,
                                       17, 111)
            
def_pkmn = pokemon.Pokemon(gen, "Milotic", "Male",
                                       58, "Docile", "Marvel Scale",
                                       "None", "Surf", "Ice Beam",
                                       "Mirror Coat", "Dragon Pulse", 30,
                                       30, 30, 30,
                                       30, 30, 0,
                                       0, 0, 0,
                                       0, 0)

move = atk_pkmn.moves[0]
crit = False
screen = "None"
#print(atk_pkmn.stat)
#print(atk_pkmn.ev)
print(formulas.calc_damage(atk_pkmn, def_pkmn, move))
print(formulas.base_power(atk_pkmn, def_pkmn, move))
print(formulas.atk_stat(atk_pkmn, move, crit, weather))
print(formulas.def_stat(def_pkmn, move, crit, weather))
print(formulas.mod1(atk_pkmn, move, weather, crit, screen, battle_type))
print(formulas.mod2(atk_pkmn, move))
type1, type2 = formulas.effectiveness(move.type, def_pkmn.species.types)
print(formulas.mod3(atk_pkmn, def_pkmn, move, type1 * type2))