import worldinfo as world
from playerinfo import Player
import bot
import log as l
import random

class Game():
    def __init__(self):
        self.game_map = world.Map(20, "./maps/standard.txt")
        self.world_objects = self.game_map.get_init_objects()
        #Red is first, blue is second
        #Randomize bots
        self.bot_list = self.determine_colors()
        self.players = [Player(150, "R", self.bot_list[0].name), Player(150, "B", self.bot_list[1].name)]
        self.game_stats = {}
        self.reset_stats()
        self.update_game_stats(self.world_objects,self.players[1],self.players[0])
        self.team_data = [[],[]]
        self.logfile = l.Log("gamelog.txt")
        self.shouldIlog = False

    
    def determine_colors(self):
        num = random.randint(0,2)
        if num == 0:
            bots = [bot.Robot1(), bot.Robot2()]
            return bots
        else:
            bots = [bot.Robot2(), bot.Robot1()]
            return bots

    def get_player_names(self):
        return (self.bot_list[0].name,self.bot_list[1].name)
    

    def run_round(self):
        #Red Turns
        for o in self.world_objects:
            gs = self.game_stats.copy()
            wo = self.world_objects.copy()
            if o.get_team() == "R":
                #Run player code to determine action
                my_action = self.bot_list[0].my_turn(gs, o.get_team(),o.get_location(),o.get_hp(), o.get_type(), self.team_data[0], wo)
                o.take_action(my_action, self.world_objects, "R", self.players[0])
                #Update game elements if action is successful (not needed for movement)
                #self.handle_action(my_action, o.take_action(my_action, self.world_objects, "R", self.players[0]))
                self.team_data[0] = my_action[1]

        #Blue Turns
        for o in self.world_objects:
            gs = self.game_stats.copy()
            if o.get_team() == "B":
                my_action = self.bot_list[1].my_turn(gs, o.get_team(),o.get_location(),o.get_hp(), o.get_type(), self.team_data[1], wo)
                o.take_action(my_action, self.world_objects, "B", self.players[1])
                #self.handle_action(my_action, o.take_action(my_action, self.world_objects, "B", self.players[0]))
                self.team_data[1] = my_action[1]

        self.players[0].mod_resources(1)
        self.players[1].mod_resources(1)

        #Discard dead robots
        self.remove_the_dead()

        self.update_game_stats(self.world_objects, self.bot_list[0], self.bot_list[1])
        if self.shouldIlog:
            self.log_round()

    def remove_the_dead(self):
        round_kill_count = 0
        for x in range(len(self.world_objects)):
            if self.world_objects[x].get_type() in ["Soldier","Wizard","Miner","Base"]:
                if self.world_objects[x].get_hp() == 0:
                    round_kill_count += 1

        while(round_kill_count > 0):
            for x in range(len(self.world_objects)):
                if self.world_objects[x].get_type() in ["Soldier","Wizard","Miner","Base"]:
                    if self.world_objects[x].get_hp() == 0:
                        self.world_objects.pop(x)
                        break
            round_kill_count -= 1

        mineral_kill_count = 0
        for x in range(len(self.world_objects)):
            if self.world_objects[x].get_type() in ["Rock", "Tree"]:
                if self.world_objects[x].get_minerals() == 0:
                    mineral_kill_count += 1

        while(mineral_kill_count > 0):
            for x in range(len(self.world_objects)):
                if self.world_objects[x].get_type() in ["Rock", "Tree"]:
                    if self.world_objects[x].get_minerals() == 0:
                        self.world_objects.pop(x)
                        break
            mineral_kill_count -= 1

    def determine_winner(self):
        if self.game_stats["r_bots"] == 0:
            return "B"
        if self.game_stats["b_bots"] == 0:
            return "R"        
        if self.game_stats["round"] >= 300:
            if self.game_stats["b_bots"] > self.game_stats["r_bots"]:
                return "B"
            if self.game_stats["r_bots"] > self.game_stats["b_bots"]:
                return "R"
            if self.game_stats["b_res"] > self.game_stats["r_res"]:
                return "B"
            if self.game_stats["r_res"] > self.game_stats["b_res"]:
                return "R"     
            num = random.randint(0,2)
            if num == 0:
                return "R"
            else:
                return "B"    
        return "None"

    def player_killed(self):
        if self.game_stats["r_bots"] == 0 or self.game_stats["b_bots"] == 0:
            return True
        return False


    def log_round(self):
        file_string = ""
        file_string += "ROUND " + str(self.game_stats["round"]) + "\n"
        for o in self.world_objects:
            if o.get_type() in ["Soldier","Wizard","Miner","Base"]:
                file_string += "ID:" + str(o.get_id()) + "\n"
                file_string += "TYPE:" + o.get_type() + "\n"
                file_string += "LOC:" + o.get_location_string() + "\n"
                file_string += "TEAM:" + o.get_team() + "\n"
                file_string += "ICON:" + o.get_icon() + "\n"
                file_string += "HP:" + str(o.get_hp()) + "\n"
                file_string += "---------------" + "\n"

        self.logfile.add_to_file(file_string)

            


    def handle_action(self, player_action, itRan):
        if itRan:
            if "strike" in player_action[0]:
                for o in self.world_objects:
                    if o.get_location() == player_action[0]["strike"]:
                        o.o.modify_hp(-30)

    def create_new_world_object(self, object_icon, location):
        pass

    def playerTurn(self, player):
        return player.my_turn()

    def print_game_map(self):
        return self.game_map.print_map()

    def get_game_objects(self):
        return self.world_objects

    def get_game_stats(self):
        return self.game_stats

    def reset_stats(self):
        self.game_stats["r_bots"] = 0
        self.game_stats["b_bots"] = 0
        self.game_stats["b_res"] = 0
        self.game_stats["r_res"] = 0
        self.game_stats["rocks"] = 0
        self.game_stats["trees"] = 0
        self.game_stats["round"] = 1

    #Run after each round
    def update_game_stats(self, wo, red_p, blue_p):
        self.game_stats["r_bots"] = 0
        self.game_stats["b_bots"] = 0
        self.game_stats["b_res"] = 0
        self.game_stats["r_res"] = 0
        self.game_stats["rocks"] = 0
        self.game_stats["trees"] = 0

        for o in wo:
            if o.get_team() == "R":
                self.game_stats["r_bots"] += 1
            elif o.get_team() == "B":
                self.game_stats["b_bots"] += 1
            elif o.get_type() == "Rock":
                self.game_stats["rocks"] += 1
            elif o.get_type() == "Tree":
                self.game_stats["trees"] += 1
        self.game_stats["red_res"] = self.players[0].get_resources()
        self.game_stats["blue_res"] = self.players[1].get_resources()
        if self.game_stats["round"] < 1000:
            self.game_stats["round"] += 1

        


