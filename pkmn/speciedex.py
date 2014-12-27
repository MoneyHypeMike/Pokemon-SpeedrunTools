import typedex
import expgroupdex

class Speciedex():
    """Creates a pokedex for generation 1 to 5."""
    
    def __init__(self):
        self.dex = {1: {}, 2: {}, 3: {}, 4:{}, 5:{}, 5.5:{}}
        
        for x in [1, 2, 3, 4, 5, 5.5]:
            self.files(x)
        
    def files(self, gen):
        if gen == 1:
            filename = r".\speciedex_data\gen1speciedex.csv"
        elif gen == 2:
            filename = r".\speciedex_data\gen2speciedex.csv"
        elif gen == 3:
            filename = r".\speciedex_data\gen3speciedex.csv"
        elif gen == 4:
            filename = r".\speciedex_data\gen4speciedex.csv"
        elif gen == 5:
            filename = r".\speciedex_data\gen5bwspeciedex.csv"
        elif gen == 5.5:
            filename = r".\speciedex_data\gen5b2w2speciedex.csv"
        
        self.create_dex(gen, filename)
    
    def create_dex(self, gen, filename):
        with open(filename) as f:
            dex = typedex.Typedex()
            f.readline()
            for lines in f:
                info = lines.split(",")
                dex_num = int(info[0].strip())
                name = info[1].strip()
                types = [info[2].strip(), info[3].strip()]
                abilities = [info[4].strip(), info[5].strip(), info[6].strip()]
                weight = float(info[7].strip())
                catch_rate = int(info[8].strip())
                happiness = int(info[9].strip())
                base_stats = [int(info[10].strip()), int(info[11].strip()), 
                              int(info[12].strip()), int(info[13].strip()), 
                              int(info[14].strip()), int(info[15].strip())]
                exp_curve = info[16].strip()
                base_exp = int(info[17].strip())
                ev_yield = [int(info[18].strip()), int(info[19].strip()), 
                            int(info[20].strip()), int(info[21].strip()), 
                            int(info[22].strip()), int(info[23].strip())]
                
                specie = Species(gen, dex_num, name, types, abilities,
                                 weight, catch_rate, happiness, base_stats,
                                 exp_curve, base_exp, ev_yield)
                
                self.dex[gen].update({name: specie})

class Species:
    """
       
       gen (int): Generation of the specie
       dex_num (int): National pokedex number
       name (str): Name of the specie
       types (list of str): Types of the species [type1, type2]
       abilities (list of str): Possible abilities [abi1l, abil2, h_abil]
       weight (float): Weight (kg) of the specie
       catch_rate (int): Catch rate of the specie
       base_happiness (int): Base happiness of the specie
       base_stats (list of int): Base stats [HP, atk, def, spatk, spdef, spd]
       exp_group (str): Experience group name of the specie
       base_exp (int): Experience yield. For gen 5 --> [bw_value, b2w2_value]
       ev_yield (list of int): EV gained [HP, atk, def, spatk, spdef, spd]
    """
    
    def __init__(self, gen, dex_num, name, types, abilities, weight, 
                 catch_rate, base_happiness, base_stats, exp_group, 
                 base_exp, ev_yield):
        self.gen = gen
        self.dex_num = dex_num
        self.name = name.upper()
        self.types = [typedex.all.dex[int(gen)][x] for x in types if x !=""]
        self.abilities = [x for x in abilities if x != ""]
        self.weight = weight
        self.catch_rate = catch_rate
        self.base_happiness = base_happiness
        self.base_stats = base_stats
        self.exp_group = expgroupdex.all.dex[exp_group]
        self.base_exp = base_exp
        self.ev_yield = ev_yield
    
    def __str__(self):
        if self.types[0].name in ["ICE", "ELECTRIC"]:
            type = "an {}".format("/".join([x.name.lower() for x in self.types]))
        else:
            type = "a {}".format("/".join([x.name.lower() for x in self.types]))
        
        name = self.name.capitalize()
        group = " ".join(self.exp_group.name.split("_")).lower()
        
        if self.gen < 3:
            return "In generation {0.gen}, {1} (#{0.dex_num}) is {2} pokémon with "\
                   "the following base stats: {0.base_stats[0]} hp, {0.base_stats[1]} atk, {0.base_stats[2]} "\
                   "def, {0.base_stats[3]} spatk, {0.base_stats[4]} spdef and {0.base_stats[5]} speed. It "\
                   "has a catch rate of {0.catch_rate}, a base happiness of {0.base_happiness} and "\
                   "a base experience of {0.base_exp}. It weights {0.weight} kg and is part "\
                   "of the {3} experience group. When it faints, it yields "\
                   "the following stat exp: {0.ev_yield[0]} hp, {0.ev_yield[1]} atk, {0.ev_yield[2]} "\
                   "def, {0.ev_yield[3]} spatk, {0.ev_yield[4]} spdef and {0.ev_yield[5]} speed."\
                   .format(self, name, type, group)
        else:
            if len(self.abilities) == 1:
                ability = "ability is {0}".format(self.abilities[0].capitalize())
            else:
                ability = "abilities are {0}".format("/".join([x.capitalize() for x in self.abilities]))
            
            return "In generation {0.gen}, {1} (#{0.dex_num}) is {2} pokémon with "\
                   "the following base stats: {0.base_stats[0]} hp, {0.base_stats[1]} atk, "\
                   "{0.base_stats[2]} def, {0.base_stats[3]} spatk, {0.base_stats[4]} spdef and {0.base_stats[5]} speed. "\
                   "It {3} and has a catch rate of {0.catch_rate}, a base happiness of "\
                   "{0.base_happiness} with a base experience of {0.base_exp}. It weights {0.weight} kg and "\
                   "is part of the {4} experience group. When it faints, it "\
                   "yields the following evs: {0.ev_yield[0]} hp, {0.ev_yield[1]} atk, "\
                   "{0.ev_yield[2]} def, {0.ev_yield[3]} spatk, {0.ev_yield[4]} spdef and {0.ev_yield[5]} "\
                   "speed".format(self, name, type, ability, group)

all = Speciedex()