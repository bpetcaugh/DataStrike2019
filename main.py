#Current Step:
#Creating game objects and seeing if they are set with the correct properties

#import classes
from gameinfo import Game


#create game instance
campaign = Game()
#campaign.print_game_map()
#print(campaign.get_game_objects())
#print(campaign.get_game_stats())
#campaign.get_all_object_info()

for x in range(len(campaign.world_objects)):
    print(campaign.world_objects[x])

'''
round_count = 2

while round_count > 0:
    #Do a thing
    campaign.run_round()
    campaign.print_game_map()
    round_count -= 1
'''
