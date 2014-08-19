"""Contains the necessary information to define a move.

   Information taken from veekun pokedex http://veekun.com/dex/moves
"""

class Moves():
    """Defines a move
       
       Variables needed for initialization:
       name (str): Name of the move
       category (str): Category of the move
       type (str): Type of the move
       power (int): Power of the move
       pp (int): Maximum number of power point
       accuracy (int): Percentage to hit
       
       Variables created based on initial variables:
       high_crit (bool): True if it's high crit ratio, false otherwise
       priority (int): Priority number
       contact (bool): Makes contact with other pokemon
       target (str): Target of the move
       charge (bool): Move has a charging turn
       recharge (bool): Move must recharge after being used
       base (str): Base of the move
       num_hit (int): Number of time the move can hit
       effect_target (str): Status aliment, foe stats reduction, etc.
       effect_chance (int): Percentage to get the effect
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
    status_moves = {"paralyzed": {"Body Slam": 0.3, "Bolt Strike": 0.2,
                                  "Bounce": 0.3, "Discharge": 0.3,
                                  "Dragon Breath": 0.3, "Force Palm": 0.3,
                                  "Freeze Shock": 0.3, "Glare": 1,
                                  "Lick": 0.3, "Nuzzle": 1, "Spark": 0.3,
                                  "Stun Spore": 1, "Thunder": 0.3,
                                  "Thunderbolt": 0.1, "Thunder Fang": 10,
                                  "Thunder Punch": 0.1, "Thunder Shock": 0.1,
                                  "Thunder Wave": 1, "Volt Tackle": 0.1,
                                  "Zap Cannon": 1},
                    "sleep": {"Dark Void": 1, "Grass Whistle": 1,
                              "Hypnosis": 1, "Lovely Kiss": 1,
                              "Relic Song": 0.1, "Sing": 1,
                              "Sleep Powder": 1, "Spore": 1},
                    "freeze": {"Blizzard": 0.1, "Freeze-Dry": 0.1,
                               "Ice Beam": 0.1, "Ice Fang": 0.1,
                               "Ice Punch": 0.1, "Powder Snow": 0.1},
                    "burned": {"Blaze Kick": 0.1, "Blue Flare": 0.2,
                               "Ember": 0.1, "Fire Blast": 0.1,
                               "Fire Fang": 0.1, "Fire Punch": 0.1,
                               "Flamethrower": 0.1, "Flame Wheel": 0.1,
                               "Flare Blitz": 0.1, "Heat Wave": 0.1,
                               "Ice Burn": 0.3, "Inferno": 1,
                               "Lava Plume": 0.3, "Sacred Fire": 0.5,
                               "Scald": 0.3, "Searing Shot": 0.3,
                               "Steam Eruption": 0.3, "Will-O-Wisp": 1},
                    "poison": {"Cross Poison": 0.1, "Gunk Shot": 0.3,
                               "Poison Gas": 1, "Poison Jab": 0.3,
                               "Poison Powder": 1, "Poison Sting": 0.3,
                               "Poison Tail": 0.1, "Sludge": 30,
                               "Sludge Bomb": 0.3, "Sludge Wave": 0.1,
                               "Smog": 0.4, "Twineedle": 0.2},
                    "badly_poison": {"Poison Fang": 0.5, "Toxic": 1},
                    "confused": {"Chatter": 1, "Confuse Ray": 1, 
                                 "Confusion": 0.1, "Dizzy Punch": 0.2,
                                 "Dynamic Punch": 1, "Flatter": 1,
                                 "Hurricane": 0.3, "Psybeam": 0.1,
                                 "Rock Climb": 0.2, "Signal Beam": 0.1,
                                 "Supersonic": 1, "Swagger": 1,
                                 "Sweet Kiss": 1, "Teeter Dance": 1,
                                 "Water Pulse": 0.2},
                     "infatuated": {"Attract": 0.5},
                     "trap": {"Bind", "Clamp", "Fire Spin", "Infestation",
                              "Magma Storm", "Sand Tomb", "Whirlpool", "Wrap"},
                     "nightmare": {"Nightmare"},
                     "torment": {"Torment"},
                     "disable": {"Disable"},
                     "yawn": {"Yawn"},
                     "heal block": {"Heal Block"},
                     "no_immunity": {"Foresight", "Miracle Eye",
                                     "Odor Sleuth"},
                     "seeded": {"Leech Seed"},
                     "embargo": {"Embargo"},
                     "perish_song": {"Perish Song"},
                     "ingrain": {"Ingrain"},
                     "curse": {"Curse"},
                     "encore": {"Encore"},
                     "flinch": {"Air Slash": 0.3, "Astonish": 0.3, "Bite": 0.3,
                                "Bone Club": 0.1, "Dark Pulse": 0.2, 
                                "Dragon Rush": 0.2, "Extrasensory": 0.1,
                                "Fake Out": 1, "Fire Fang": 0.1, 
                                "Headbutt": 0.3, "Heart Stamp": 0.3,
                                "Hyper Fang": 0.1, "Ice Fang": 0.1,
                                "Icicle Crash": 0.3, "Iron Head": 0.3,
                                "Needle Arm": 0.3, "Rock Slide": 0.3,
                                "Rolling Kick": 0.3, "Sky Attack": 0.3,
                                "Snore": 0.3, "Steamroller": 0.3, "Stomp": 0.3,
                                "Thunder Fang": 0.1, "Twister": 0.2,
                                "Waterfall": 0.2, "Zen Headbutt": 0.2}}
    
    ko_moves = {"Fissure", "Guillotine", "Horn Drill", "Sheer Cold"}
    
    def __init__(self, name, category, type, power, pp, accuracy):
        self.name = name
        self.category = category
        self.type = type
        self.power = power
        self.pp = pp
        self.accuracy = accuracy
        
        self.check_high_crit()
        self.check_priority()
        self.check_contact()
        self.check_target()
        self.check_charge()
        self.check_recharge()
        self.check_base()
        self.check_num_hit()
    
    def __str__(self):
        return "{} is a {} {} move with a power of {}, {} PP and {}% accuracy"\
               .format(self)
    
    def __repr__(self):
        return "moves.Moves({0.name}, {0.category}, {0.type}, {0.power}, {0.pp}, " \
                "{0.accuracy})".format(self)
    
    def check_high_crit(self):
        """Checks if the move has a high critical hit ratio"""
        
        self.high_crit = True if self.name in self.high_crit_moves else False
    
    def check_priority(self):
        """Sets the priority number of the move"""
        
        for number in self.priority_moves.keys():
            if self.name in self.priority_moves[number]:
                self.priority = number
                break
        else:
            self.priority = 0
    
    def check_contact(self):
        """Checks if the move makes contact"""
        
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
        """Sets the move target"""
        
        for keys in self.target_moves.keys():
            if self.name in self.target_moves[keys]:
                self.target = keys
                break
        else:
            self.target = "single opponent"
    
    def check_charge(self):
        """Checks if the move needs a charging turn"""
        
        self.charge = True if self.name in self.charge_moves else False
   
    def check_recharge(self):
        """Checks if the moves must recharge"""
        
        self.recharge = True if self.name in self.recharge_moves else False
        
    def check_base(self):
        """Sets the base of the move"""
        
        for keys in self.base_moves:
            if self.name in self.base_moves[keys]:
                self.base = keys
                break
        else:
            self.base = False
    
    def check_num_hit(self):
        """Sets the number of time a move can hit"""
        
        for keys in self.multi_hit_moves:
            if self.name in self.multi_hit_moves[keys]:
                self.num_hit = keys
                break
        else:
            self.num_hit = 1

#used for testing
m = Moves("Double Slap", "Physical", "Normal", 20, 20, 100)