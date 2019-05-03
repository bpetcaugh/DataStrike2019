import pygame
import sprites
from gameinfo import Game


#create game instance
campaign = Game()
game_objects_import = campaign.get_game_objects()
display_objects = []
bg_color = (0, 170, 0)
clock = pygame.time.Clock()
sprite_objects = []

pygame.init()
screen = pygame.display.set_mode((800, 800))
screen.fill(bg_color)
done = False

ss = sprites.SpriteSheet("./images/iconpack1/transp_1.png")

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

round_count = 1
myfont1 = pygame.font.SysFont('Comic Sans MS', 80)
textsurface1 = myfont1.render('RED WINS!', False, (255, 0, 0))
myfont2 = pygame.font.SysFont('Comic Sans MS', 30)
textsurface2 = myfont2.render('BLUE WINS!', False, (0, 0, 255))
winner = "None"

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if round_count <= 300:
        campaign.run_round()
        screen.fill(bg_color)
        game_objects_import = campaign.get_game_objects()
        display_objects = []
        load_images()
        place_images()
        #campaign.run_round()
        #screen.blit(image_list[0],(0, y_test))
        #y_test += 40
        round_count += 1
        
    pygame.display.flip()
    if winner == "None":
        winner = campaign.determine_winner()
    if winner == "R":
        screen.blit(textsurface1,(0,0))
    elif winner == "B":
        screen.blit(textsurface2,(0,0))        

    clock.tick(4)

