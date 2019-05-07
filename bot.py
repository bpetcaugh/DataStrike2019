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
        self.shouldILog = True

    def my_turn(self, stats, team, loc, hp, type, data, world):
        '''
        Type your player code here for each turn
        '''

        
        if type == "Base":
            self.logfile.add_to_file("I am " + team + " and I at " + str(loc[0]))
            return [{"build":("Soldier",(loc[0]+1,loc[1]))}, data]


        #Random Movement
        x = loc[0] + random.choice([-1,0,1])
        y = loc[1] + random.choice([-1,0,1])
        return [{"move":(x,y)},data]



class Robot2():
    def __init__(self):
        self.name = "Petcaugh"
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
        

class Robot3():

    def __init__(self):
        self.name = "Bot slayer"
        self.logfile = l.Log(self.name+".txt")
        self.shouldILog = True

    def my_turn(self, stats, team, loc, hp, type, data, world):
        '''
        Type your player code here for each turn
        '''

        '''
        if type == "Base":
            return [{"build":("Soldier",(loc[0]+1,loc[1]))}, data]

        #Random Movement
        x = loc[0] + random.choice([-1,0,1])
        y = loc[1] + random.choice([-1,0,1])
        return [{"move":(x,y)},data]
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


class Robot4():
    def __init__(self):
        self.name = "Miguel"
        self.logfile = l.Log(self.name+".txt")
        self.shouldILog = False
        self.print = True  # Testing

    def my_turn(self, stats, team, loc, hp, type, data, world):
        '''
        Type your player code here for each turn
        '''

        if self.shouldILog:
            self.logfile.add_to_file(
                str(stats["round"]) + ": I am a " + type + "\n")

        info = []

        for i in range(9):
            info.append(0)
        info[0] = []
        info[4] = []

        for obj in world:
            # -----> INFORMATION SECTION <----- #
            # ENEMY INFO
            if obj.get_type() == "Base" and obj.get_team() != team:
                info[0].append(obj.get_location())  # Returns as tuple

            if obj.get_type() == "Soldier" and obj.get_team() != team:
                info[1] += 1

            if obj.get_type() == "Miner" and obj.get_team() != team:
                info[2] += 1

            if obj.get_type() == "Wizard" and obj.get_team() != team:
                info[3] += 1

            # MY INFO
            if obj.get_type() == "Base" and obj.get_team() == team:
                info[4].append(obj.get_location())

            if obj.get_type() == "Soldier" and obj.get_team() == team:
                info[5] += 1

            if obj.get_type() == "Miner" and obj.get_team() == team:
                info[6] += 1

            if obj.get_type() == "Wizard" and obj.get_team() == team:
                info[7] += 1

        # -----> STRATEGY SECTION <----- #

        # TESTS
        # global print_data
        # if stats["round"] == 5 and print_data:
        #     print(data)
        #     print_data = False

        # BASE
        if type == "Base":
            # Send out sos on data[8] array
            if hp < 150 and self.close_to_me(loc, team, world) < 5:
                data.append(["SOS", loc])
            else:
                data.append(["GOOD", loc])
            # Can you take oponents resources??????
            # or not(stats["b_res"] < 1 and stats["r_res"] < 1):
            if stats["round"] < 50:
                # Build Miners
                return [{"build": ("Miner", (loc[0]+1, loc[1]))}, data]
            if info[1] > info[5]:  # Build soldier so that I always have more
                return [{"build": ("Soldier", (loc[0]+1, loc[1]))}, data]
            if stats["round"] > 150 and self.my_resources(team, stats) > 180:
                return [{"build": ("Wizard", (loc[0]+1, loc[1]))}, data]
            if stats["round"] < 100:
                return [{"build": ("Soldier", (loc[0]+1, loc[1]))}, data]
            else:  # Build Soldiers
                return [{"build": ("Wizard", (loc[0]+1, loc[1]))}, data]

        # MINER
        if type == "Miner":
            # Go for rocks until the rocks are finished
            # amount_trees_rocks = 0  # TRYING TO ACCOUNT FOR NO MORE OBJECTS, Just roam around
            # for obj in world:
            #     if obj.get_type() == "Rock" or obj.get_type() == "Tree":
            #         amount_trees_rocks += 1
            # if amount_trees_rocks == 0:
            #     x = loc[0] + random.choice([-1, 0, 1])
            #     y = loc[1] + random.choice([-1, 0, 1])
            #     return [{"move": (x, y)}, data]

            # # Go for the rocks first
            # rockLoc = []
            # nearestRock = ()
            # for obj in world:
            #     if obj.get_type() == "Rock":
            #         rockLoc.append(obj.get_location())
            # for rock in rockLoc:
            #     shortest = 100
            #     distanceRock = abs(rock[0] - loc[0]) + abs(rock[1] - loc[1])
            #     if distanceRock < shortest:
            #         nearestRock = rock
            # if abs(nearestRock[0] - loc[0]) <= 2 and abs(nearestRock[1] - loc[1]) <= 2:
            #     return [{"gather": nearestRock}, data]
            # else:
            #     myMoveLoc = self.move_toward(world, loc, nearestRock)
            #     return [{"move": myMoveLoc}, data]

            # Find nearest rock (or tree) and go towards it
            mineralLocs = []
            nearestMineralLoc = ()
            for obj in world:
                if obj.get_type() == "Rock" or obj.get_type() == "Tree":
                    mineralLocs.append(obj.get_location())
            for mineralloc in mineralLocs:
                shortest = 100
                mineralDistance = abs(
                    mineralloc[0] - loc[0]) + abs(mineralloc[1] - loc[1])
                if mineralDistance < shortest:
                    nearestMineralLoc = mineralloc

            # index out of range if resources run out

            if abs(nearestMineralLoc[0] - loc[0]) <= 2 and abs(nearestMineralLoc[1] - loc[1]) <= 2:
                # GATHER!
                return [{"gather": nearestMineralLoc}, data]
            else:
                # MOVE TOWARDS MINERAL
                myMoveLoc = self.move_toward(world, loc, nearestMineralLoc)
                return [{"move": myMoveLoc}, data]

        # SOLDIER
        if type == "Soldier":
            if data[0][0] == "SOS":
                return [{"move": data[0][1]}, data]
            # Find nearby enemies
            myEnemies = []
            for obj in world:
                if obj.get_team() != team:
                    if obj.get_type() in ["Base", "Soldier", "Wizard", "Miner"]:
                        myEnemies.append(obj.get_location())
            # ATTACK!
            for e in myEnemies:
                if abs(e[0] - loc[0]) <= 2 and abs(e[1] - loc[1]) <= 2:
                    return [{"strike": e}, data]

            # Move towards the enemy strategy needs to be added
            if info[5] > (info[1] + 5):
                # Move towards enemy base and attack
                # attack first if anyone closeby, then move
                if len(info) > 0:
                    myMoveTo = self.move_toward(world, loc, info[0][0])  # Fix this to account for more than one base!
                    return [{"move": myMoveTo}, data]

        # WIZARD
        if type == "Wizard":
            # Find nearby enemies
            myEnemies = []
            nearestEnemy = ()
            for obj in world:
                if obj.get_team() != team:
                    if obj.get_type() in ["Base", "Soldier", "Wizard", "Miner"]:
                        myEnemies.append(obj.get_location())
            # ATTACK!
            for e in myEnemies:
                if abs(e[0] - loc[0]) <= 3 and abs(e[1] - loc[1]) <= 3:
                    return [{"cast": e}, data]

            for enemy in myEnemies:
                shortest = 100
                distanceTo = abs(enemy[0] - loc[0]) + abs(enemy[1] - loc[1])

                if distanceTo < shortest:
                    nearestEnemy = enemy

            myMoveTo = self.move_toward(world, loc, nearestEnemy)
            return [{"move": myMoveTo}, data]

        # MID-GAME
        '''
        Send all wizards and warriors to attack
        '''
        # ENDGAME
        if type == "Soldier" and 200 >= stats["round"] >= 150:
            # MOVE TOWARDS BASES
            if len(info[0]) > 1:
                myMoveLoc = self.move_toward(world, loc, info[0][1])
                return [{"move": myMoveLoc}, data]
        if type == "Soldier" and stats["round"] >= 200:
            # MOVE TOWARDS BASES
            if len(info[0]) > 0:
                myMoveLoc = self.move_toward(world, loc, info[0][0])
                return [{"move": myMoveLoc}, data]

        # -----> EXTRA SECTION <----- #
        # RANDOM MOVEMENT
        x = loc[0] + random.choice([-1, 0, 1])
        y = loc[1] + random.choice([-1, 0, 1])
        return [{"move": (x, y)}, data]

    # -----> ADDED METHODS SECTION <----- #
    def canImove(self, newloc, w):
        '''Method to determine if there is something in the spot
        where I am trying to move.'''
        for obj in w:
            if obj.get_location() == newloc:
                return False
        return True

    def move_toward(self, w, myloc, newloc):
        '''Method to move toward a specific location. Returns
        a location to move.'''  # w is world
        # My current location
        x1 = myloc[0]
        y1 = myloc[1]
        # Location bot is trying to move
        x2 = newloc[0]
        y2 = newloc[1]
        # Locations I can move, if nothing is in my way (clockwise, starting at North)
        # This may or may not be used yet
        locs_to_move = [(x1, y1-1), (x1+1, y1-1), (x1+1, y1), (x1+1, y1+1),
                        (x1, y1+1), (x1-1, y1+1), (x1-1, y1), (x1-1, y1-1)]

        # Travel SE
        if x1 < x2 and y1 < y2:
            try:
                if self.canImove(locs_to_move[3], w):
                    return locs_to_move[3]
                else:
                    for dir in locs_to_move:
                        if self.canImove(dir, w):
                            return dir
            except TypeError:
                print(x1)
                print(y1)
                print(x2)
                print(y2)
                if type == "Base":
                    print("Base")
                elif type == "Miner":
                    print("Miner")
                elif type == "Wizard":
                    print("Wizard")
                else:
                    print("Soldier")

        # Travel NW
        if x1 > x2 and y1 > y2:
            if self.canImove(locs_to_move[7], w):
                return locs_to_move[7]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        # Travel NE
        if x1 < x2 and y1 > y2:
            if self.canImove(locs_to_move[1], w):
                return locs_to_move[1]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        # Travel SW
        if x1 > x2 and y1 < y2:
            if self.canImove(locs_to_move[5], w):
                return locs_to_move[5]
            else:
                for dir in locs_to_move:
                    if self.canImove(dir, w):
                        return dir

        # Return random move if nothing else works
        x = myloc[0] + random.choice([-1, 0, 1])
        y = myloc[1] + random.choice([-1, 0, 1])
        return (x, y)

    def my_resources(self, team, stats):
        if team is "R":
            return stats["r_res"]
        else:
            return stats["b_res"]

    def close_to_me(self, loc, team, world):  # Finish this
        # Needs to return integer
        base_x = loc[0]
        base_y = loc[1]

        soldier_wizard_loc = []
        for o in world:
            if o.get_team() != team:
                if o.get_type() in ["Soldier", "Wizard"]:
                    soldier_wizard_loc.append(o.get_location())

        for e_loc in soldier_wizard_loc:
            # distance  # abs()
            # other things
            pass
        return 1


class Robot5():

    def __init__(self):
        self.name = "Chris Bot"
        self.logfile = l.Log(self.name+".txt")
        self.shouldILog = True
        
    def my_turn(self, stats, team, loc, hp, type, data, world):
        

        if self.shouldILog:
            self.logfile.add_to_file(str(stats["round"]) + ": I am a " + type + "\n")

        #Get enemy info
        eBases = []
        for obj in world:
            if obj.get_type() == "Base" and obj.get_team() != team:
                eBases.append(obj.get_location())
        eMiner = []
        for obj in world:
            if obj.get_type() == "Base" and obj.get_team() != team:
                eBases.append(obj.get_location())

        #Base Strategy
        if type == "Base":
            if stats["round"] < 75:
                #build miners
                return [{"build":("Miner",(loc[0]+1,loc[1]))}, data]
            else:
                #Build Soldiers
                return [{"build":("Soldier",(loc[0]+1,loc[1]))}, data]
            if stats["round"] == 50:
                return [{"build":("Soldier",(loc[0]+1,loc[1]))}, data]
                
       
        if type == "Miner":
           
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
               
                return [{"gather":nearestMineralLoc},data]  
            else:
                
                myMoveLoc = self.move_toward(world, loc, nearestMineralLoc)
                return [{"move":myMoveLoc},data] 

        if type == "Soldier":
           
            myEnemies = []
            nearestEnemyLoc = ()
            for obj in world:
                if obj.get_team() != team:
                    if obj.get_type() in ["Base","Soldier","Wizard","Miner"]:
                        myEnemies.append(obj.get_location())
            for myEnemies in nearestEnemyLoc:
                shortest = 100
                enemyDistance = abs(myEnemies[0] - loc [0]) + abs(myEnemies[1]- loc[1]) <=2;
                if enemyDistance < shortest:
                    nearestEnemyLoc = myEnemies
            #attack miners in the first 50 rounds
            if type == "Soldier" and stats["round"] < 300:
            #MOVE TOWARDS miners
                if len(eBases) > 1:
                    if len(eMiner) > 0:
                        myMoveLoc = self.move_toward(world, loc, eMiner[1])
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

   




