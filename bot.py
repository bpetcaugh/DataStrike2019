#import statements here
import random
import log as l

'''
This robot has access to the data explained in the README, and also
the following methods for all objects in world:

for o in world:
    o.get_id()          #Returns a unique number for each robot
    o.get_type()        #Return "Rock", "Soldier", etc
    o.get_location()    #Returns location in tuple (x,y)
    o.get_team()        #Returns "R" or "B"


DEBUGGING: You can add to the LOG file by putting this line anywhere:

self.logfile.add_to_file("Sample String to Add")
'''

class Robot1():

    def __init__(self):
        self.name = "Standard"
        self.logfile = l.Log(self.name+".txt")
        self.shouldILog = False

    def my_turn(self, stats, team, loc, hp, type, data, world):
        '''
        Type your player code here for each turn
        '''

        
        if type == "Base":
            return [{"build":("Soldier",(loc[0]+1,loc[1]))}, data]

        #Random Movement
        x = loc[0] + random.choice([-1,0,1])
        y = loc[1] + random.choice([-1,0,1])
        return [{"move":(x,y)},data]



class Robot2():
    def __init__(self):
        self.name = "Spicy"
        self.logfile = l.Log(self.name+".txt")
        self.shouldILog = True

    def my_turn(self, stats, team, loc, hp, type, data, world):
        '''
        Type your player code here for each turn
        '''

        if self.shouldILog:
            self.logfile.add_to_file(str(stats["round"]) + ": I am a " + type + "\n")

        #Get enemy base locations
        eBases = []
        for obj in world:
            if obj.get_type() == "Base" and obj.get_team() != team:
                eBases.append(obj.get_location())

        #Get other locations that may be useful in the future

        #Base Strategy
        if type == "Base":
            if stats["round"] < 50:
                #Build Miners
                return [{"build":("Miner",(loc[0]+1,loc[1]))}, data]
            else:
                #Build Soldiers
                return [{"build":("Soldier",(loc[0]+1,loc[1]))}, data]

        #Miner Strategy
        if type == "Miner":
            #Find nearest rock (or tree) and go towards it
            mineralLocs = []
            nearestMineralLoc = ()
            for obj in world:
                if obj.get_type() == "Rock" or obj.get_type() == "Tree":
                    mineralLocs.append(obj.get_location())
            for mineralloc in mineralLocs:
                shortest = 100
                mineralDistance = abs(mineralloc[0] - loc[0]) + abs(mineralloc[1] - loc[1])
                if mineralDistance < shortest:
                    nearestMineralLoc = mineralloc
            
            if abs(nearestMineralLoc[0] - loc[0]) <= 2 and abs(nearestMineralLoc[1] - loc[1]) <= 2:
                #GATHER!
                return [{"gather":nearestMineralLoc},data]  
            else:
                #MOVE TOWARDS MINERAL
                myMoveLoc = self.move_toward(world, loc, nearestMineralLoc)
                return [{"move":myMoveLoc},data] 

        if type == "Soldier":
            #Find nearby enemies
            myEnemies = []
            for obj in world:
                if obj.get_team() != team:
                    if obj.get_type() in ["Base","Soldier","Wizard","Miner"]:
                        myEnemies.append(obj.get_location())
            #ATTACK!
            for e in myEnemies:
                if abs(e[0] - loc[0]) <= 2 and abs(e[1] - loc[1]) <= 2:
                    return [{"strike":e},data]  



        #Mid-Game Strategy
        if type == "Wizard":
            return [{"cast":(loc[0]+2,loc[1])}, data]


        #EndGame....
        if type == "Soldier" and 200 >= stats["round"] >= 150:
            #MOVE TOWARDS BASES
            if len(eBases) > 1:
                myMoveLoc = self.move_toward(world, loc, eBases[1])
                return [{"move":myMoveLoc},data]         
        if type == "Soldier" and stats["round"]>=200:
            #MOVE TOWARDS BASES
            if len(eBases) > 0:
                myMoveLoc = self.move_toward(world, loc, eBases[0])
                return [{"move":myMoveLoc},data]      
        
        #Random Movement
        x = loc[0] + random.choice([-1,0,1])
        y = loc[1] + random.choice([-1,0,1])
        return [{"move":(x,y)},data]


    def canImove(self, newloc, w):
        '''Method to determine if there is something in the spot
        where I am trying to move.'''
        for obj in w:
            if obj.get_location() == newloc:
                return False
        return True
    
    def move_toward(self, w, myloc, newloc):
        '''Method to move toward a specific location. Returns
        a location to move.'''
        #My current location
        x1 = myloc[0]
        y1 = myloc[1]
        #Location bot is trying to move
        x2 = newloc[0]
        y2 = newloc[1]
        #Locations I can move, if nothing is in my way (clockwise, starting at North)
        #This may or may not be used yet
        locs_to_move = [(x1,y1-1),(x1+1,y1-1),(x1+1,y1),(x1+1,y1+1),(x1,y1+1),(x1-1,y1+1),(x1-1,y1),(x1-1,y1-1)]

        #Travel SE
        if x1 < x2 and y1 < y2:
            if self.canImove(locs_to_move[3], w):
                return locs_to_move[3]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        #Travel NW
        if x1 > x2 and y1 > y2:
            if self.canImove(locs_to_move[7], w):
                return locs_to_move[7]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        #Travel NE
        if x1 < x2 and y1 > y2:
            if self.canImove(locs_to_move[1], w):
                return locs_to_move[1]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        #Travel SW
        if x1 > x2 and y1 < y2:
            if self.canImove(locs_to_move[5], w):
                return locs_to_move[5]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        #Return random move if nothing else works
        x = myloc[0] + random.choice([-1,0,1])
        y = myloc[1] + random.choice([-1,0,1])
        return (x,y)    
        


