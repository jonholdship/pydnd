from monstersdictionary import *

# Monster class
class Monster:
    """Class used to rename values in the lists.monst_dic dictionary."""
    def __init__(self, name, challenge_rating, creature_size,creature_type, environment,hitdie,init): 
        self.name             = name
        self.challenge_rating = str(challenge_rating)
        self.size    = creature_size
        self.type    = creature_type
        self.environment      = environment
        self.xp               = 0
        self.hitdie       	  = hitdie
        self.init        = init

    def getinfo(self):
        print "hi"
        return [self.name,self.challenge_rating,self.size,self.type,self.environment,self.hitdie,self.init]

class globaldat:
	def __init__(self):
		self.players=[]
		self.selected=[]
		self.monsters_dict={}
		for key in monst_dict:
			self.monsters_dict[key] = Monster(key, *monst_dict[key])	

