import species as s

class Pokedex():
    """Creates a pokedex for generation 1 to 5"""
    def __init__(self):
        self.dex = {1: {}, 2: {}, 3: {}, 4:{}, 5:{}}
        
        for x in range(1, 6):
            self.files(x)
        
    def files(self, gen):
        """Selects the correct file to generate the pokedex"""
        if gen == 1:
            filename = ".\pokedex_data\gen1dex.csv"
        elif gen == 2:
            filename = ".\pokedex_data\gen2dex.csv"
        elif gen == 3:
            filename = ".\pokedex_data\gen3dex.csv"
        elif gen == 4:
            filename = ".\pokedex_data\gen4dex.csv"
        elif gen == 5:
            filename = ".\pokedex_data\gen5dex.csv"
        
        self.create_dex(gen, filename)
    
    def create_dex(self, gen, filename):
        """Generates the pokedex for the specified generation"""
        with open(filename) as f:
            f.readline()
            for lines in f:
                info = lines.split(",")
                dex_num = info[0].strip()
                name = info[1].strip()
                type = [info[2].strip(), info[3].strip()]
                types = [x for x in type if x != "" and x != "\n"]
                ability = [info[4].strip(), info[5].strip(), info[6].strip()]
                abilities = [x for x in ability if x != "" and x != "\n"]
                weight = info[7].strip()
                catch_rate = info[8].strip()
                happiness = info[9].strip()
                base_stats = [info[10].strip(), info[11].strip(), 
                              info[12].strip(), info[13].strip(), 
                              info[14].strip(), info[15].strip()]
                exp_curve = info[16].strip()
                base_exp = info[17].strip()
                ev_yield = [info[18].strip(), info[19].strip(), 
                            info[20].strip(), info[21].strip(), 
                            info[22].strip(), info[23].strip()]
                
                specie = s.Species(dex_num, name, types, abilities, weight,
                                   catch_rate, happiness, base_stats, 
                                   exp_curve, base_exp, ev_yield)
                                   
                self.dex[gen].update({name: specie})

if __name__ != "__main__":
    dex = Pokedex()