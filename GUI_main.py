import pygame
import sprites
from gameinfo import Game
import random


#create game instance
campaign = Game()
game_objects_import = campaign.get_game_objects()
display_objects = []
bg_color = (0, 150, 0)
clock = pygame.time.Clock()
sprite_objects = []

pygame.init()
screen = pygame.display.set_mode((950, 800))
screen.fill(bg_color)
done = False

ss = sprites.SpriteSheet("./images/iconpack1/transp_1.png")

playlist = ["./music/GroovyTower.wav","./music/gloriousmorning.wav","./music/timemachine.wav","./music/finalbattle.wav"]

pygame.mixer.music.load(random.choice(playlist))
pygame.mixer.music.play(-1)


hud = pygame.Surface((150,800))
hud.fill((0,0,0))


def translate_location(loc):
    new_loc = (loc[0]*40, loc[1]*40)
    return new_loc

def load_images():
    for o in game_objects_import:
        item = o.get_icon()
        if item == "QU":
            display_objects.append([translate_location(o.get_location()),ss.get_image(4,387,25,25,bg_color)])
        elif item == "TR":
            display_objects.append([translate_location(o.get_location()),ss.get_image(163,387,25,25,bg_color)])
        elif item == "BB":
            display_objects.append([translate_location(o.get_location()),ss.get_image(99,133,25,25,(0,0,255))])
        elif item == "BS":
            display_objects.append([translate_location(o.get_location()),ss.get_image(35,227,25,25,(0,0,255))])
        elif item == "BW":
            display_objects.append([translate_location(o.get_location()),ss.get_image(227,196,25,25,(0,0,255))])
        elif item == "BM":
            display_objects.append([translate_location(o.get_location()),ss.get_image(69,322,25,25,(0,0,255))])
        elif item == "RB":
            display_objects.append([translate_location(o.get_location()),ss.get_image(99,133,25,25,(255,0,0))])
        elif item == "RS":
            display_objects.append([translate_location(o.get_location()),ss.get_image(35,227,25,25,(255,0,0))])
        elif item == "RW":
            display_objects.append([translate_location(o.get_location()),ss.get_image(227,196,25,25,(255,0,0))])
        elif item == "RM":
            display_objects.append([translate_location(o.get_location()),ss.get_image(69,322,25,25,(255,0,0))])

def place_images():
    for i in display_objects:
        #Paramters: image, position
        screen.blit(i[1],i[0])
    #screen.blit(hud,(800,0))


def update_hud():
    hud.fill((0,0,0))
    start_row = 10
    start_col = 10
    inc_row = 35
    statlist = campaign.get_game_stats()
    names = campaign.get_player_names()

    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    hudfont = pygame.font.SysFont('', 30)
    #screen.blit(hud,(800,0))
    title = hudfont.render('DataStrike', False, white)
    div = hudfont.render("----------", False, white)
    hud.blit(title,(start_row,start_col))
    start_col += inc_row

    hud.blit(div,(start_row,start_col))
    start_col += inc_row

    gen_round_txt = "Round: " + str(statlist["round"])
    gen_round = hudfont.render(gen_round_txt, False, white)
    hud.blit(gen_round,(start_row,start_col))
    start_col += inc_row

    hud.blit(div,(start_row,start_col))
    start_col += inc_row

    #RED

    rname = hudfont.render(names[0], False, red)
    hud.blit(rname,(start_row,start_col))
    start_col += inc_row

    rbot_txt = "Bots: " + str(statlist["r_bots"])
    rbots = hudfont.render(rbot_txt, False, red)
    hud.blit(rbots,(start_row,start_col))
    start_col += inc_row

    rres_txt = "Res: " + str(statlist["red_res"])
    rres = hudfont.render(rres_txt, False, red)
    hud.blit(rres,(start_row,start_col))
    start_col += inc_row

    hud.blit(div,(start_row,start_col))
    start_col += inc_row

    #BLUE
    bname = hudfont.render(names[1], False, blue)
    hud.blit(bname,(start_row,start_col))
    start_col += inc_row

    bbot_txt = "Bots: " + str(statlist["b_bots"])
    bbots = hudfont.render(bbot_txt, False, blue)
    hud.blit(bbots,(start_row,start_col))
    start_col += inc_row

    bres_txt = "Res: " + str(statlist["blue_res"])
    bres = hudfont.render(bres_txt, False, blue)
    hud.blit(bres,(start_row,start_col))
    start_col += inc_row

    hud.blit(div,(start_row,start_col))
    start_col += inc_row

    winner = "None"
    if winner == "None":
        winner = campaign.determine_winner()
    if winner == "R":
        winner = "RED"
    elif winner == "B":
        winner = "BLUE"  
    win_txt1 = "WINNER: "
    win1 = hudfont.render(win_txt1, False, white)
    hud.blit(win1,(start_row,start_col))
    start_col += inc_row

    win2 = hudfont.render(winner, False, white)
    hud.blit(win2,(start_row,start_col))
    start_col += inc_row
    screen.blit(hud,(800,0))


round_count = 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if round_count < 300:
        campaign.run_round()
        screen.fill(bg_color)
        game_objects_import = campaign.get_game_objects()
        display_objects = []
        load_images()
        place_images()
        update_hud()
        #campaign.run_round()
        #screen.blit(image_list[0],(0, y_test))
        #y_test += 40
        if campaign.player_killed():
            round_count = 300
        else:
            round_count += 1
        
    pygame.display.flip()  

    clock.tick(5)

