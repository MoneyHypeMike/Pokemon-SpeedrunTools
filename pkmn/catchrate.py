from math import floor, sqrt
import pokemon

#Formulas are taken from www.dragonflycave.com
#Gen1: http://www.dragonflycave.com/rbycapture.aspx
#Gen2: http://www.dragonflycave.com/gen2capture.aspx
#Gen3-4: http://www.dragonflycave.com/capture.aspx
#Gen 5: http://www.dragonflycave.com/gen5capture.aspx#formula

def calc_catchrate(ball_name, atk_pkmn, def_pkmn, status="Normal", location="None", owned=False, turn=1, time="Night", power=0, caught=1):
    if ball_name in ("Master Ball", "Park Ball", "Dream Ball"):
        return 1
    
    pct = []
    hps = []
    gen = def_pkmn.species.gen
    c = capture_rate(ball_name, atk_pkmn, def_pkmn, location)
    b = ball_bonus(gen, ball_name, def_pkmn, location, turn, time, owned)
    s = status_multi(gen, status)
    ratio = 100
    
    if gen == 1:
        g = 8 if ball_name == "Great Ball" else 12
        for x in range(0, 16):
            def_pkmn.update_iv(0, x)
            m = def_pkmn.stat[0]
            h = floor(def_pkmn.stat[0] * ratio / 100)
            f = min(255, (m * 255 // g) // max(1, h // 4))
            chance = (s / b) + (min(c + 1, b - s) / b) * ((f + 1) / 256)
            hps.append(m)
            pct.append(round(chance, 5))
    elif gen == 2:
        for x in range(0, 16):
            def_pkmn.update_iv(0, x)
            m = def_pkmn.stat[0]
            h = floor(def_pkmn.stat[0] * ratio / 100)
            x = max(1, floor((3 * m - 2 * h) * c) // (3 * m)) + s
            hps.append(m)
            pct.append(min(1, round((x + 1) / 256, 5)))
    elif gen == 3 or gen == 4:
        for x in range(0, 32):
            def_pkmn.update_iv(0, x)
            m = def_pkmn.stat[0]
            h = floor(def_pkmn.stat[0] * ratio / 100)
            x = max(1, floor(floor(((3 * m - 2 * h) * floor(c * b)) // (3 * m)) * s))
            y = 1048560 // floor(sqrt(floor(sqrt(16711680 // x))))
            hps.append(m)
            pct.append(min(1, round((y / 65536) ** 4, 5)))
    elif gen == 5:
        ccs = []
        g, p = grass(location, caught)
        e = entralink(power)
        for x in range(0, 32):
            def_pkmn.update_iv(0, x)
            m = def_pkmn.stat[0]
            h = floor(def_pkmn.stat[0] * ratio / 100)
            x = max(1, down5(round5(down5(round5(round5((3 * m - 2 * h) * g) * c * b) / (3 * m)) * s) * e / 100))
            y = floor(round5(65536 / round5(sqrt(round5(sqrt(round5(255 / x)))))))
            hps.append(m)
            pct.append(min(1, round((y / 65536) ** 3, 5)))
            if caught > 30:
                cc = floor(min(255, x * p) / 6) / 256
                ccs.append(round(cc, 5))
    
    if caught > 30:
        values = {key: [value, c] for (key, value, c) in zip(hps, pct, ccs)}
    else:
        values = {key: value for (key, value) in zip(hps, pct)}
    
    return values

def balls(gen):
    if gen == 1:
        return ("Poké Ball", "Great Ball", "Ultra Ball", "Master Ball", "Safari Ball")
    elif gen == 2:
        return ("Poké Ball", "Great Ball", "Ultra Ball", "Master Ball", "Safari Ball",
                "Level Ball", "Lure Ball", "Moon Ball", "Friend Ball", "Love Ball",
                "Heavy Ball", "Fast Ball", "Sport Ball")
    
def down5(x):
    return floor(x * 4096) / 4096

def round5(x):
    return round(x * 4096) / 4096

def entralink(power):
    if power == 0:
        return 100
    elif power == 1:
        return 110
    elif power == 2:
        return 120
    elif power == 3:
        return 130

def grass(location, caught):   
    if caught > 600:
        if location == "Thick Grass":
            return (1, 2.5)
        else:
            return (1, 2.5)
    elif caught > 450:
        if location == "Thick Grass":
            return (3686/4096, 2)
        else:
            return (1, 2)
    elif caught > 300:
        if location == "Thick Grass":
            return (3277/4096, 1.5)
        else:
            return (1, 1.5)
    elif caught > 150:
        if location == "Thick Grass":
            return (2867/4096, 1)
        else:
            return (1, 1)
    elif caught > 30:
        if location == "Thick Grass":
            return (0.5, 0.5)
        else:
            return (1, 0.5)
    else:
        if location == "Thick Grass":
            return (1229/4096, 0)
        else:
            return (1, 0)

def status_multi(gen, name):
    if name in ("Asleep", "Frozen"):
        if gen == 1:
            return 25
        elif gen == 2:
            return 10
        elif gen == 3 or gen == 4:
            return 2
        elif gen == 5:
            return 2.5
    elif name in ("Poisoned", "Paralyzed", "Burned"):
        if gen == 1:
            return 12
        elif gen == 2:
            return 0
        elif gen < 6:
            return  1.5
    else:
        if gen < 3:
            return 0
        elif gen < 6:
            return 1

def capture_rate(ball_name, atk_pkmn, def_pkmn, location):
    catch_rate = def_pkmn.species.catch_rate
    if gen == 1 or gen == 5:
        return catch_rate
    
    if ball_name in ("Great Ball", "Park Ball"):
        if gen == 2:
            exp = catch_rate * 1.5
        else:
            exp = catch_rate
    elif ball_name == "Ultra Ball":
        if gen == 2:
            exp = catch_rate * 2
        else:
            exp = catch_rate
    elif ball_name == "Fast Ball":
        if gen == 2:
            if def_pkmn.species.name in ("GRIMER", "TANGELA", "MAGNEMITE"):
                exp = catch_rate * 4
            else:
                exp = catch_rate
        else:
            if def_pkmn.species.base_stats[5] > 100:
                exp = catch_rate * 4
            else:
                exp = catch_rate
    elif ball_name == "Heavy Ball":
        weight = def_pkmn.species.weight
        if gen == 2:
            if weight > 307.2:
                exp = catch_rate + 30
            elif weight > 204.8:
                exp = catch_rate + 20
            elif weight > 102.4:
                exp = catch_rate
            else:
                exp = catch_rate - 20
        else:
            if weight > 409.6:
                exp = catch_rate + 40
            elif weight > 307.2:
                exp = catch_rate + 30
            elif weight > 204.8:
                exp = catch_rate + 20
            else:
                exp = catch_rate - 20
    elif ball_name == "Level Ball":
        atk_level = atk_pkmn.level
        def_level = def_pkmn.level
        if atk_level // 4 > def_level:
            exp = catch_rate * 8
        elif atk_level // 2 > def_level:
            exp = catch_rate * 4
        elif atk_level > def_level:
            exp = catch_rate * 2
        else:
            exp = catch_rate
    elif ball_name == "Love Ball":
        if atk_pkmn.species.name == def_pkmn.species.name and \
           "Genderless" not in (atk_pkmn.gender, def_pkmn.gender):
           if gen == 2 and atk_pkmn.gender == def_pkmn.gender:
               exp = catch_rate * 8
           elif 2 < gen < 6 and atk_pkmn.gender != def_pkmn.gender:
               exp = catch_rate * 8
           else:
               exp = catch_rate
        else:
            exp = catch_rate
    elif ball_name == "Lure Ball":
        if location == "Fishing":
            exp = catch_rate * 3
        else:
            exp = catch_rate
    elif ball_name == "Moon Ball":
        pokes = ("NIDORINO", "NIDORINA", "CLEFAIRY", "JIGGLYPUFF", "SKITTY")
        if def_pkmn.species.name in pokes:
            if gen == 2:
                exp = catch_rate
            elif gen < 6:
                exp = catch_rate * 4
        else:
            exp = catch_rate
    else:
        exp = catch_rate
    
    if exp < 0:
        return 1
    elif exp > 255:
        return 255
    else:
        return exp
        
def ball_bonus(gen, ball_name, def_pkmn, location, turn, time, owned):
    if gen == 1:
        if ball_name == "Poké Ball":
            return 256
        elif ball_name == "Great Ball":
            return 201
        elif ball_name in {"Ultra Ball", "Safari Ball"}:
            return 151
    
    if ball_name in ("Great Ball", "Safari Ball", "Sport Ball"):
        return 1.5
    elif ball_name == "Ultra Ball":
        return 2
    elif ball_name == "Net Ball":
        types = [x.name for x in def_pkmn.species.types]
        if "BUG" in types or "WATER" in types:
            return 3
        else:
            return 1
    elif ball_name == "Nest Ball":
        if gen == 3 or gen == 4:
            return max(1, (40 - def_pkmn.level) / 10)
        elif gen == 5:
            return max(1, (41 - def_pkmn.level) / 10)
    elif ball_name == "Dive Ball":
        if gen == 3 and location == "Underwater":
            return 3.5
        elif gen > 3 and location == "Water":
            return 3.5
        else:
            return 1
    elif ball_name == "Repeat Ball":
        if owned:
            return 3
        else:
            return 1
    elif ball_name == "Timer Ball":
        if gen == 3 or gen == 4:
            return min(4, (turn + 10) / 10)
        elif gen == 5:
            return min(4, 1 + (turn * 1229 / 4096))
    elif ball_name == "Quick Ball":
        if turn == 1:
            if gen == 3 or gen == 4:
                return 4
            elif gen == 5:
                return 5
        else:
            return 1
    elif ball_name == "Dusk Ball":
        if location == "Cave" or time == "Night":
            return 3.5
        else:
            return 1
    else:
        return 1
        
gen = 4
piplup = pokemon.Pokemon(gen, "TENTACOOL", "Male", 17, "Mild","Torrent", "None", "None", "None", "None",
                         "None", 25, 31, 31, 31, 30, 31)
abra = pokemon.Pokemon(gen, "TENTACRUEL", "Female", 6, "Modest", "Synchronize", "None", "None", "None", "None",
                       "None", 12, 10, 15, 20, 25, 30)

print(calc_catchrate("Net Ball", piplup, abra, "Normal", "Thick Grass"))
print(calc_catchrate("Net Ball", abra, piplup, "Normal", "Thick Grass"))
#print(calc_catchrate("Poké Ball", piplup, abra, "Frozen", "Thick Grass"))

#print(calc_catchrate("Great Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Great Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Great Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Ultra Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Ultra Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Ultra Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Safari Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Safari Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Safari Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Master Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Master Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Master Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Premier Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Premier Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Premier Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Net Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Net Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Net Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Nest Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Nest Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Nest Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Dive Ball", piplup, abra, "Normal", "Water"))
#print(calc_catchrate("Dive Ball", piplup, abra, "Poisoned", "Water"))
#print(calc_catchrate("Dive Ball", piplup, abra, "Frozen", "Water"))

#print(calc_catchrate("Dive Ball", piplup, abra, "Normal", "Underwater"))
#print(calc_catchrate("Dive Ball", piplup, abra, "Poisoned", "Underwater"))
#print(calc_catchrate("Dive Ball", piplup, abra, "Frozen", "Underwater"))

#print(calc_catchrate("Repeat Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Repeat Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Repeat Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Repeat Ball", piplup, abra, "Normal", "", True))
#print(calc_catchrate("Repeat Ball", piplup, abra, "Poisoned", "", True))
#print(calc_catchrate("Repeat Ball", piplup, abra, "Frozen", "", True))

#print(calc_catchrate("Timer Ball", piplup, abra, "Normal", "", False, 10))
#print(calc_catchrate("Timer Ball", piplup, abra, "Poisoned", "", False, 10))
#print(calc_catchrate("Timer Ball", piplup, abra, "Frozen", "", False, 10))

#print(calc_catchrate("Timer Ball", piplup, abra, "Normal", "", False))
#print(calc_catchrate("Timer Ball", piplup, abra, "Poisoned", "", False))
#print(calc_catchrate("Timer Ball", piplup, abra, "Frozen", "", False))

#print(calc_catchrate("Luxury Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Luxury Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Luxury Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Heal Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Heal Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Heal Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Quick Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Quick Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Quick Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Quick Ball", piplup, abra, "Normal", "", False, 10))
#print(calc_catchrate("Quick Ball", piplup, abra, "Poisoned", "", False, 10))
#print(calc_catchrate("Quick Ball", piplup, abra, "Frozen", "", False, 10))

#print(calc_catchrate("Dusk Ball", piplup, abra, "Normal", "Cave", False, 10, "Day"))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Poisoned", "Cave", False, 10, "Day"))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Frozen", "Cave", False, 10, "Day"))

#print(calc_catchrate("Dusk Ball", piplup, abra, "Normal", "Thick Grass", False, 10, "Day", 2, 31))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Poisoned", "Thick Grass", False, 10, "Day", 2, 31))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Frozen", "Thick Grass", False, 10, "Day", 2, 31))

#print(calc_catchrate("Dusk Ball", piplup, abra, "Normal", "Cave", False, 10, "Night"))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Poisoned", "Cave", False, 10, "Night"))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Frozen", "Cave", False, 10, "Night"))

#print(calc_catchrate("Dusk Ball", piplup, abra, "Normal", "", False, 10, "Night", 3))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Poisoned", "", False, 10, "Night", 3))
#print(calc_catchrate("Dusk Ball", piplup, abra, "Frozen", "", False, 10, "Night", 3))

#print(calc_catchrate("Park Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Park Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Park Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Cherish Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Cherish Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Cherish Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Sport Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Sport Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Sport Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Friend Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Friend Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Friend Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Fast Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Fast Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Fast Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Heavy Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Heavy Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Heavy Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Level Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Level Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Level Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Love Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Love Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Love Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Lure Ball", piplup, abra, "Normal", "Fishing"))
#print(calc_catchrate("Lure Ball", piplup, abra, "Poisoned", "Fishing"))
#print(calc_catchrate("Lure Ball", piplup, abra, "Frozen", "Fishing"))

#print(calc_catchrate("Lure Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Lure Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Lure Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Moon Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Moon Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Moon Ball", piplup, abra, "Frozen"))

#print(calc_catchrate("Dream Ball", piplup, abra, "Normal"))
#print(calc_catchrate("Dream Ball", piplup, abra, "Poisoned"))
#print(calc_catchrate("Dream Ball", piplup, abra, "Frozen"))