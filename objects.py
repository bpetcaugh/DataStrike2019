import random

class GameObject():
    #Type: Base, Soldier, Wizard, Miner, Rock, Tree
    #Location: (x,y)
    #Team: "R", "B", or None
    def __init__(self, t, loc, color, i):
        self.id = random.randint(100, 1000)
        self.type = t
        self.location = loc
        self.team = color
        self.icon = i

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

    def get_location(self):
        return self.location

    def get_team(self):
        return self.team

    def get_icon(self):
        return self.icon

    def set_icon(self, i):
        self.icon = i
    
    def get_location_string(self):
        return "(" + str(self.location[0]) + "," + str(self.location[1]) + ")"

class Unit(GameObject):
    def __init__(self, t, loc, color, i):
        super(Unit, self).__init__(t, loc, color, i)
    
class Soldier(Unit):
    def __init__(self, t, loc, color, i):
        self.hp = 130
        self.ap = 30
        self.mp = 0
        self.move_max = 1
        self.attack_max = 1
        self.vision = 5
        self.alive = True
        super(Soldier, self).__init__(t, loc, color, i)

    def get_hp(self):
        return self.hp  

    def modify_hp(self, mod):
        self.hp += mod
        if self.hp <= 0:
            self.alive = False
        if self.hp < 0:
            self.hp = 0

    def move(self, loc, objects):
        #Checks if various conditions are met
        #Returns True if the move was successful, otherwise returns False
        canMove = True
        for o in objects:
            if o.get_location() == loc:
                canMove = False

        if canMove:
            if (0 <= loc[0] < 20) and (0 <= loc[1] < 20):
                if (int(loc[0]) == loc[0]) and (int(loc[1]) == loc[1]):
                    if (abs(loc[0] - self.location[0]) <= self.move_max) and (abs(loc[1] - self.location[1]) <= self.move_max):
                        self.location = loc
                        return True
        return False

    def strike(self, loc, objects):
        #Checks for valid location
        validLoc = False
        if (0 <= loc[0] < 20) and (0 <= loc[1] < 20):
            if (int(loc[0]) == loc[0]) and (int(loc[1]) == loc[1]):
                if (abs(loc[0] - self.location[0]) <= self.attack_max) and (abs(loc[1] - self.location[1]) <= self.attack_max):
                    validLoc = True

        #Checks if object can be attacked
        canStrike = False
        if validLoc:
            for o in objects:
                if o.get_location() == loc:
                    if o.get_type() in ["Soldier","Wizard","Miner","Base"]:
                        o.modify_hp(-self.ap)
                        canStrike = True

        return canStrike

    def take_action(self, list, objects, color, player):
        if self.alive:
            if 'move' in list[0]:
                self.move(list[0]['move'], objects)
            elif 'strike' in list[0]:
                self.strike(list[0]['strike'], objects)

class Base(Unit):
    def __init__(self, t, loc, color, i):
        self.hp = 300
        self.ap = 0
        self.mp = 0
        self.move_max = 0
        self.build_max = 1
        self.alive = True
        super(Base, self).__init__(t, loc, color, i)

    def get_hp(self):
        return self.hp  

    def modify_hp(self, mod):
        self.hp += mod
        if self.hp <= 0:
            self.alive = False
        if self.hp < 0:
            self.hp = 0

    def build(self, type, color, loc, objects):
        canBuild = True
        for o in objects:
            if o.get_location() == loc:
                canBuild = False

        if canBuild:
            if (0 <= int(loc[0]) < 20) and (0 <= int(loc[1]) < 20):
                if (int(loc[0]) == loc[0]) and (int(loc[1]) == loc[1]):
                    if (abs(loc[0] - self.location[0]) <= self.build_max) and (abs(loc[1] - self.location[1]) <= self.build_max):
                        if type == "Soldier" and color == "B":
                            objects.append(Soldier("Soldier",loc,color,"BS"))
                        elif type == "Soldier" and color == "R":
                            objects.append(Soldier("Soldier",loc,color,"RS"))
                        elif type == "Wizard" and color == "B":
                            objects.append(Wizard("Wizard",loc,color,"BW"))
                        elif type == "Wizard" and color == "R":
                            objects.append(Wizard("Wizard",loc,color,"RW"))
                        elif type == "Miner" and color == "B":
                            objects.append(Miner("Miner",loc,color,"BM"))
                        elif type == "Miner" and color == "R":
                            objects.append(Miner("Miner",loc,color,"RM"))

                        return objects

    def take_action(self, list, objects, color, player):
        if self.alive:
            if 'build' in list[0]:
                self.build(list[0]['build'][0], color ,list[0]['build'][1] ,objects)

class Wizard(Unit):
    def __init__(self, t, loc, color, i):
        self.hp = 70
        self.ap = 0
        self.mp = 60
        self.move_max = 3
        self.attack_max = 3
        self.vision = 8
        self.alive = True
        super(Wizard, self).__init__(t, loc, color, i)

    def get_hp(self):
        return self.hp  

    def modify_hp(self, mod):
        self.hp += mod
        if self.hp <= 0:
            self.alive = False
        if self.hp < 0:
            self.hp = 0

    def move(self, loc, objects):
        #Checks if various conditions are met
        #Returns True if the move was successful, otherwise returns False
        canMove = True
        for o in objects:
            if o.get_location() == loc:
                canMove = False

        if canMove:
            if (0 <= loc[0] < 20) and (0 <= loc[1] < 20):
                if (int(loc[0]) == loc[0]) and (int(loc[1]) == loc[1]):
                    if (abs(loc[0] - self.location[0]) <= self.move_max) and (abs(loc[1] - self.location[1]) <= self.move_max):
                        self.location = loc
                        return True
        return False

    def cast(self, loc, objects):
        #Checks for valid location
        validLoc = False
        if (0 <= loc[0] < 20) and (0 <= loc[1] < 20):
            if (int(loc[0]) == loc[0]) and (int(loc[1]) == loc[1]):
                if (abs(loc[0] - self.location[0]) <= self.attack_max) and (abs(loc[1] - self.location[1]) <= self.attack_max):
                    validLoc = True

        #Checks if object can be attacked
        canCast = False
        if validLoc:
            for o in objects:
                if o.get_location() == loc:
                    if o.get_type() in ["Soldier","Wizard","Miner","Base"]:
                        o.modify_hp(-self.mp)
                        canCast = True

        return canCast

    def take_action(self, list, objects, color, player):
        if self.alive:
            if 'move' in list[0]:
                self.move(list[0]['move'], objects)
            elif 'cast' in list[0]:
                self.cast(list[0]['cast'], objects)


class Miner(Unit):
    def __init__(self, t, loc, color, i):
        self.hp = 40
        self.ap = 0
        self.mp = 0
        self.move_max = 1
        self.alive = True
        super(Miner, self).__init__(t, loc, color, i)

    def get_hp(self):
        return self.hp  

    def modify_hp(self, mod):
        self.hp += mod
        if self.hp <= 0:
            self.alive = False
        if self.hp < 0:
            self.hp = 0

    def move(self, loc, objects):
        #Checks if various conditions are met
        #Returns True if the move was successful, otherwise returns False
        canMove = True
        for o in objects:
            if o.get_location() == loc:
                canMove = False

        if canMove:
            if (0 <= loc[0] < 20) and (0 <= loc[1] < 20):
                if (int(loc[0]) == loc[0]) and (int(loc[1]) == loc[1]):
                    if (abs(loc[0] - self.location[0]) <= self.move_max) and (abs(loc[1] - self.location[1]) <= self.move_max):
                        self.location = loc
                        return True
        return False

    def gather(self, loc, objects, player):
        for o in objects:
            if o.get_location() == loc:
                if o.get_type() == "Rock" or o.get_type() == "Tree":
                    o.harvest(20, player)

    def take_action(self, list, objects, color, player):
        if self.alive:
            if 'move' in list[0]:
                self.move(list[0]['move'], objects)
            if 'gather' in list[0]:
                self.gather(list[0]['gather'], objects, player)

    
class Resource(GameObject):
    def __init__(self, t, loc, color, i):
        super(Resource, self).__init__(t, loc, color, i)

class Rock(Resource):
    def __init__(self, t, loc, color, i):
        self.minerals = 400
        super(Rock, self).__init__(t, loc, color, i)

    def harvest(self, amount, player):
        if self.minerals >= 20:
            self.minerals -= amount
            player.mod_resources(amount)
        elif 0 < self.minerals < 20:
            player.mod_resources(self.minerals)
            self.minerals = 0
    
    def get_minerals(self):
        return self.minerals
    
class Tree(Resource):
    def __init__(self, t, loc, color, i):
        self.minerals = 200
        super(Tree, self).__init__(t, loc, color, i)

    def harvest(self, amount, player):
        if self.minerals >= 20:
            self.minerals -= amount
            player.mod_resources(amount)
        elif 0 < self.minerals < 20:
            player.mod_resources(self.minerals)
            self.minerals = 0

    def get_minerals(self):
        return self.minerals

        




