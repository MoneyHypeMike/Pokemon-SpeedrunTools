import typedex

class Movedex():
    """Creates a movedex for generation 1 to 5."""
    
    def __init__(self):
        self.dex = {1: {}, 2: {}, 3: {}, 4:{}, 5:{}}
        
        for x in range(1, 6):
            self.files(x)
        
    def files(self, gen):
        if gen == 1:
            filename = r".\movedex_data\gen1movedex.csv"
        elif gen == 2:
            filename = r".\movedex_data\gen2movedex.csv"
        elif gen == 3:
            filename = r".\movedex_data\gen3movedex.csv"
        elif gen == 4:
            filename = r".\movedex_data\gen4movedex.csv"
        elif gen == 5:
            filename = r".\movedex_data\gen5movedex.csv"
        
        self.create_dex(gen, filename)
    
    def find_category(self, gen, type):
        categories = {"PHYSICAL": {"Normal", "Fighting", "Flying", "Ground", 
                                 "Rock", "Bug", "Ghost", "Poison", "Steel"},
                      "SPECIAL": {"Water", "Grass", "Fire", "Ice", "Electric",
                                "Psychic", "Dragon", "Dark"},
                      "OTHER": "???"}
        if gen < 4:
            for category in categories.keys():
                if type in categories[category]:
                    return category
                    break
    
    def create_dex(self, gen, filename):
        with open(filename) as f:
            f.readline()
            for lines in f:
                info = lines.split(",")
                name = info[0].strip().upper()
                type = info[1].strip()
                if gen < 4:
                    category = self.find_category(gen, type)
                else:
                    category = info[2].strip().upper()
                if gen < 3:
                    power = int(info[2].strip())
                    accuracy = round(int(info[3].strip())*100/255)
                    pp = int(info[4].strip())
                    effect_pct = round(int(info[5].strip())*100/255)
                elif gen == 3:
                    power = int(info[2].strip())
                    accuracy = int(info[3].strip())
                    pp = int(info[4].strip())
                    effect_pct = round(int(info[5].strip()))
                else:
                    power = int(info[3].strip())
                    accuracy = int(info[4].strip())
                    pp = int(info[5].strip())
                    effect_pct = int(info[6].strip())
                
                move = Moves(gen, name, category, type, power, pp, 
                             accuracy, effect_pct)
                    
                self.dex[gen].update({name: move})

class Moves():
    """
       
       Initialized variables:
       gen (int): Generation of the move
       name (str): Name of the move
       category (str): Category of the move
       type (str): Type of the move
       power (int): Power of the move
       pp (int): Maximum number of power point
       accuracy (int): Percentage to hit
       effect_pct (int): Percentage to get the effect
       
       Generated variables:
       recoil (bool): True if the move does recoil damage
       high_crit (bool): True if it's high crit ratio, false otherwise
       priority (int): Priority number
       contact (bool): Makes contact with other pokemon
       target (str): Target of the move
       charge (bool): Move has a charging turn
       recharge (bool): Move must recharge after being used
       base (str): Base of the move
       num_hit (int): Number of time the move can hit
    """

    charge_moves = {"Blast Burn", "Frenzy Plant", "Giga Impact", 
                    "Hydro Cannon", "Hyper Beam", "Roar of Time",
                    "Rock Wrecker"}

    recharge_moves = {"Bounce", "Dig", "Dive", "Fly", "Freeze Shock",
                      "Geomancy", "Ice Burn", "Phantom Force", "Razor Wind",
                      "Shadow Force", "Skull Bash", "Sky Attack", "Sky Drop",
                      "Solar Beam"}
    base_moves = {"Punch": {"Bullet Punch", "Comet Punch", "Dizzy Punch",
                            "Drain Punch", "Dynamic Punch", "Fire Punch",
                            "Focus Punch", "Hammer Arm", "Ice Punch",
                            "Mach Punch", "Mega Punch", "Meteor Mash",
                            "Power-Up Punch", "Shadow Punch", 
                            "Sky Uppercut", "Thunder Punch"},
                  "Sound": {"Boomburst", "Bug Buzz", "Chatter", "Confide",
                            "Uproar", "Disarming Voice", "Echoed Voice",
                            "Grass Whistle", "Growl", "Heal Bell", 
                            "Hyper Voice", "Metal Sound", "Noble Roar",
                            "Parting Shot", "Perish Song", "Relic Song",
                            "Roar", "Round", "Screech", "Sing", "Snarl",
                            "Snore", "Supersonic"},
                  "Jaw": {"Bite", "Crunch", "Fire Fang", "Ice Fang",
                          "Poison Fang", "Thunder Fang"},
                  "Pulse": {"Aura Sphere", "Dark Pulse", "Dragon Pulse",
                            "Heal Pulse", "Water Pulse"},
                  "Ball": {"Acid Spray", "Aura Sphere", "Barrage",
                           "Bullet Seed", "Egg Bomb", "Electro Ball",
                           "Energy Ball", "Focus Blast", "Gyro Ball",
                           "Ice Ball", "Magnet Bomb", "Mud Bomb",
                           "Octazooka", "Seed Bomb", "Shadow Ball",
                           "Sludge Bomb", "Weather Ball"}}
    
    #Dictionary of moves which heals when used
    #The second dictionary list the following:
    #pct: Percentage to heal
    #user: True if it heals the user, false if it heals target
    #dmg: True if healing based on damage, false if it based on max hp
    #To do: Healing Wish, Lunar Dance, Moonlight, Morning Sun, Swallow, Wish
    healing_moves = {"Absorb": {"pct": 0.5, "user": True, "dmg": True}, 
                    "Draining Kiss": {"pct": 0.75, "user": True, "dmg": True},
                    "Drain Punch": {"pct": 0.5, "user": True, "dmg": True},
                    "Dream Eater": {"pct": 0.5, "user": True, "dmg": True},
                    "Giga Drain": {"pct": 0.5, "user": True, "dmg": True},
                    #"Healing Wish": {"pct": -1, "user": True, "dmg": False},
                    "Heal Order": {"pct": 0.5, "user": True, "dmg": False},
                    "Heal Pulse": {"pct": 0.5, "user": False, "dmg": False},
                    "Horn Leech": {"pct": 0.5, "user": True, "dmg": True},
                    "Leech Life": {"pct": 0.5, "user": True, "dmg": True},
                    #"Lunar Dance"{"pct": -1, "user": True, "dmg": False}, 
                    "Mega Drain": {"pct": 0.5, "user": True, "dmg": True}, 
                    "Milk Drink": {"pct": 0.5, "user": True, "dmg": False}, 
                    #"Moonlight": {"pct": 0.5, "user": True, "dmg": False}, 
                    #"Morning Sun": {"pct": 0.5, "user": True, "dmg": False}, 
                    "Oblivion Wing": {"pct": 0.75, "user": True, "dmg": True}, 
                    "Parabolic Charge": {"pct": 0.5, "user": True, "dmg": True}, 
                    "Recover": {"pct": 0.5, "user": True, "dmg": False},
                    "Rest": {"pct": 1, "user": True, "dmg": False},
                    "Roost": {"pct": 0.5, "user": True, "dmg": False},
                    "Slack Off": {"pct": 0.5, "user": True, "dmg": False},
                    "Soft-Boiled": {"pct": 0.5, "user": True, "dmg": False},
                    #"Swallow": {"pct": , "user": , "dmg": },
                    "Synthesis": {"pct": 0.5, "user": True, "dmg": False}}
                    #"Wish": {"pct": 0.5, "user": True, "dmg": False}

    powder_moves = {"Cotton Spore", "Poison Power", "Powder", "Rage Powder",
                    "Sleep Powder", "Spore", "Stun Spore"}

    high_crit_moves = {"Aeroblast", "Air Cutter", "Attack Order", 
                       "Blaze Kick", "Crabhammer", "Cross Chop",
                       "Cross Poison", "Drill Run", "Frost Breath",
                       "Karate Chop", "Leaf Blade", "Night Slash",
                       "Poison Tail", "Psycho Cut", "Razor Leaf",
                       "Razor Wind", "Shadow Claw", "Sky Attack",
                       "Slash", "Spacial Rend", "Stone Edge",
                       "Storm Throw"}

    #to do: beat up
    multi_hit_moves = {5: {"Arm Trust", "Barrage", "Bone Rush", "Bullet Seed",
                           "Comet Punch", "Double Slap", "Fury Attack",
                           "Icicle Spear", "Rock Blast", "Pin Missile",
                           "Tail Slap", "Spike Cannon","Water Shuriken"},
                       3: {"Triple Kick"},
                       2: {"Bonemerang", "Double Hit", "Double Kick",
                           "Dual Chop", "Gear Grind", "Twineedle"}}

    priority_moves = {-7: {"Trick Room"},
                      -6: {"Circle Throw", "Dragon Tail", "Roar", "Whirlwind"},
                      -5: {"Counter", "Mirror Coat"},
                      -4: {"Avalanche", "Revenge"},
                      -3: {"Focus Punch"},
                      -1: {"Vital Throw"},
                      +1: {"Ally Switch", "Aqua Jet", "Baby-Doll Eyes", "Bide",
                           "Bullet Punch", "Ice Shard", "Ion Deluge", 
                           "Mach Punch", "Powder", "Quick Attack", 
                           "Shadow Punch", "Vacuum Wave", "Water Shuriken"},
                      +2: {"Extreme Speed", "Feint", "Follow Me", 
                           "Rage Powder"},
                      +3: {"Crafty Shield", "Fake Out", "Quick Guard", 
                           "Wide Guard"},
                      +4: {"Detect", "Endure", "King's Shield", "Magic Coat",
                           "Protect", "Snatch", "Spiky Shield"},
                      +5: {"Helping Hand"}}

    #This dictionary contains special moves which makes contact
    #and physical moves which doesn't make contact
    contact_moves = {"Special": {"Draining Kiss", "Grass Knot", "Infestation",
                                "Petal Dance", "Trump Card" "Wring Out"},
                     "Physical": {"Attack Order", "Barrage", "Beat Up", 
                              "Bone Club", "Bonemerang", "Bone Rush",
                              "Bulldoze", "Bullet Seed", "Diamond Storm",
                              "Earthquake", "Egg Bomb", "Explosion", "Feint",
                              "Fissure", "Fling", "Freeze Shock", 
                              "Fusion Bolt", "Gunk Shot", "Ice Shard", 
                              "Icicle Crash", "Icicle Spear", "Land's Wrath",
                              "Magnet Bomb", "Magnitude", "Metal Burst", 
                              "Natural Gift", "Pay Day", "Petal Blizzard", 
                              "Pin Missile", "Poison String", "Present", 
                              "Psycho Cut", "Razor Leaf", "Rock Blast",
                              "Rock Slide", "Rock Throw", "Rock Wrecker",
                              "Sacred Fire", "Sand Tomb", "Secret Power",
                              "Seed Bomb", "Self-Destruct", "Sky Attack",
                              "Smack Down", "Spike Cannon", "Stone Edge",
                              "Thousand Arrows", "Twineedle", 
                              "Water Shuriken"}}
    
    #only includes moves which hit all other pokemon, opponent pokemon
    target_moves = {"all": {"Boomburst", "Bulldoze", "Discharge", 
                            "Earthquake","Explosion", "Lava Plume",
                            "Magnitude", "Parabolic Charge", "Petal Blizzard",
                            "Searing Shot", "Self-Destruct", "Sludge Wave",
                            "Surf", "Synchronoise", "Teeter Dance"},
                    "all opponent": {"Acid", "Air Cutter", "Blizzard",
                                     "Bubble", "Captivate", "Cotton Spore",
                                     "Dark Void", "Dazzling Gleam", 
                                     "Diamond Storm", "Disarming Voice", 
                                     "Electroweb", "Eruption", "Glaciate", 
                                     "Growl", "Heal Block", "Heat Wave", 
                                     "Hyper Voice", "Icy Wind", "Incinerate", 
                                     "Land's Wrath", "Leer", "Muddy Water",
                                     "Poison Gas", "Powder Snow", "Razor Leaf",
                                     "Razor Wind", "Relic Song", "Rock Slide",
                                     "Snarl", "String Shot", "Struggle Bug",
                                     "Sweet Scent", "Swift", "Tail Whip",
                                     "Thousand Arrows", "Thousand Waves",
                                     "Twister", "Venom Drench", "Water Spout"},
                    "random": {"Outrage", "Petal Dance", "Struggle", "Trash",
                               "Uproar"}}
    
    #dictionary which contains the different status aliments
    #second dictionary indicates the percentage to get the status (if needed)
    status_moves = {"PRZ": {"BODY SLAM": 0.3, "BOLT STRIKE": 0.2,
                                  "BOUNCE": 0.3, "DISCHARGE": 0.3,
                                  "DRAGON BREATH": 0.3, "FORCE PALM": 0.3,
                                  "FREEZE SHOCK": 0.3, "GLARE": 1,
                                  "LICK": 0.3, "NUZZLE": 1, "SPARK": 0.3,
                                  "STUN SPORE": 1, "THUNDER": 0.3,
                                  "THUNDERBOLT": 0.1, "THUNDER FANG": 10,
                                  "THUNDER PUNCH": 0.1, "THUNDER SHOCK": 0.1,
                                  "THUNDER WAVE": 1, "VOLT TACKLE": 0.1,
                                  "ZAP CANNON": 1},
                    "SLP": {"DARK VOID": 1, "GRASS WHISTLE": 1,
                              "HYPNOSIS": 1, "LOVELY KISS": 1,
                              "RELIC SONG": 0.1, "SING": 1,
                              "SLEEP POWDER": 1, "SPORE": 1},
                    "FRZ": {"BLIZZARD": 0.1, "FREEZE-DRY": 0.1,
                               "ICE BEAM": 0.1, "ICE FANG": 0.1,
                               "ICE PUNCH": 0.1, "POWDER SNOW": 0.1},
                    "BRN": {"BLAZE KICK": 0.1, "BLUE FLARE": 0.2,
                               "EMBER": 0.1, "FIRE BLAST": 0.1,
                               "FIRE FANG": 0.1, "FIRE PUNCH": 0.1,
                               "FLAMETHROWER": 0.1, "FLAME WHEEL": 0.1,
                               "FLARE BLITZ": 0.1, "HEAT WAVE": 0.1,
                               "ICE BURN": 0.3, "INFERNO": 1,
                               "LAVA PLUME": 0.3, "SACRED FIRE": 0.5,
                               "SCALD": 0.3, "SEARING SHOT": 0.3,
                               "STEAM ERUPTION": 0.3, "WILL-O-WISP": 1},
                    "PSN": {"CROSS POISON": 0.1, "GUNK SHOT": 0.3,
                               "POISON GAS": 1, "POISON FANG": 0.5,
                               "POISON JAB": 0.3, "POISON POWDER": 1, 
                               "POISON STING": 0.3, "POISON TAIL": 0.1, 
                               "SLUDGE": 30, "SLUDGE BOMB": 0.3, 
                               "SLUDGE WAVE": 0.1, "SMOG": 0.4, 
                               "TOXIC": 1, "TWINEEDLE": 0.2}}
                     #"CONFUSED": {"CHATTER": 1, "CONFUSE RAY": 1, 
                     #            "CONFUSION": 0.1, "DIZZY PUNCH": 0.2,
                     #            "DYNAMIC PUNCH": 1, "FLATTER": 1,
                     #            "HURRICANE": 0.3, "PSYBEAM": 0.1,
                     #            "ROCK CLIMB": 0.2, "SIGNAL BEAM": 0.1,
                     #            "SUPERSONIC": 1, "SWAGGER": 1,
                     #            "SWEET KISS": 1, "TEETER DANCE": 1,
                     #            "WATER PULSE": 0.2},
                     #"INFATUATED": {"ATTRACT": 0.5},
                     #"TRAP": {"BIND", "CLAMP", "FIRE SPIN", "INFESTATION",
                     #         "MAGMA STORM", "SAND TOMB", "WHIRLPOOL", "WRAP"},
                     #"NIGHTMARE": {"NIGHTMARE"},
                     #"TORMENT": {"TORMENT"},
                     #"DISABLE": {"DISABLE"},
                     #"YAWN": {"YAWN"},
                     #"HEAL BLOCK": {"HEAL BLOCK"},
                     #"NO_IMMUNITY": {"FORESIGHT", "MIRACLE EYE",
                     #                "ODOR SLEUTH"},
                     #"SEEDED": {"LEECH SEED"},
                     #"EMBARGO": {"EMBARGO"},
                     #"PERISH_SONG": {"PERISH SONG"},
                     #"INGRAIN": {"INGRAIN"},
                     #"CURSE": {"CURSE"},
                     #"ENCORE": {"ENCORE"},
                     #"FLINCH": {"AIR SLASH": 0.3, "ASTONISH": 0.3, "BITE": 0.3,
                     #           "BONE CLUB": 0.1, "DARK PULSE": 0.2, 
                     #           "DRAGON RUSH": 0.2, "EXTRASENSORY": 0.1,
                     #           "FAKE OUT": 1, "FIRE FANG": 0.1, 
                     #           "HEADBUTT": 0.3, "HEART STAMP": 0.3,
                     #           "HYPER FANG": 0.1, "ICE FANG": 0.1,
                     #           "ICICLE CRASH": 0.3, "IRON HEAD": 0.3,
                     #           "NEEDLE ARM": 0.3, "ROCK SLIDE": 0.3,
                     #           "ROLLING KICK": 0.3, "SKY ATTACK": 0.3,
                     #           "SNORE": 0.3, "STEAMROLLER": 0.3, "STOMP": 0.3,
                     #           "THUNDER FANG": 0.1, "TWISTER": 0.2,
                     #           "WATERFALL": 0.2, "ZEN HEADBUTT": 0.2}}
    
    ko_moves = {"Fissure", "Guillotine", "Horn Drill", "Sheer Cold"}
    
    recoil_moves = {"Brave Bird", "Double-Edge", "Flare Blitz", "Head Charge",
              "Head Smash", "Submission", "Take Down", "Volt Tackle",
              "Wild Charge", "Wood Hammer"}
    
    def __init__(self, gen, name, category, type, power, pp, accuracy, effect_pct):
        self.gen = gen
        self.name = name.upper()
        self.category = category
        self.type = typedex.all.dex[gen][type]
        self.power = power
        self.pp = pp
        self.accuracy = accuracy
        self.effect_pct = effect_pct
        
        self.check_recoil()
        self.check_high_crit()
        self.check_priority()
        self.check_contact()
        self.check_target()
        self.check_charge()
        self.check_recharge()
        self.check_base()
        self.check_num_hit()
        self.check_status()
        
    #def __str__(self):
    #    return "{} is a {} {} move with a power of {}, {} PP and {}% accuracy"\
    #           .format(self)
    
    #def __repr__(self):
    #    return "moves.Moves({0.name}, {0.category}, {0.type}, {0.power}, {0.pp}, " \
    #            "{0.accuracy})".format(self)
    
    def check_status(self):
        for keys in self.status_moves.keys():
            if self.name in self.status_moves[keys]:
                self.status = keys
                break
        else:
            self.status = None
    
    def check_recoil(self):
        self.recoil = True if self.name in self.recoil_moves else False
        
    def check_high_crit(self):
        self.high_crit = True if self.name in self.high_crit_moves else False
    
    def check_priority(self):
        for number in self.priority_moves.keys():
            if self.name in self.priority_moves[number]:
                self.priority = number
                break
        else:
            self.priority = 0
    
    def check_contact(self):
        if self.category == "Physical":
            if self.name in self.contact_moves[self.category]:
                self.contact = False
            else:
                self.contact = True
        elif self.category == "Special" :
            if self.name in self.contact_moves[self.category]:
                self.contact = True
            else:
                self.contact = False
    
    def check_target(self):
        for keys in self.target_moves.keys():
            if self.name in self.target_moves[keys]:
                self.target = keys
                break
        else:
            self.target = "single opponent"
    
    def check_charge(self):
        self.charge = True if self.name in self.charge_moves else False
   
    def check_recharge(self):
        self.recharge = True if self.name in self.recharge_moves else False
        
    def check_base(self):
        for keys in self.base_moves:
            if self.name in self.base_moves[keys]:
                self.base = keys
                break
        else:
            self.base = False
    
    def check_num_hit(self):
        for keys in self.multi_hit_moves:
            if self.name in self.multi_hit_moves[keys]:
                self.num_hit = keys
                break
        else:
            self.num_hit = 1

all = Movedex()