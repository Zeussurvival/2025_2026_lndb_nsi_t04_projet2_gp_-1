# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os 
import classe_dialogue as C_D
import numpy
import random
import time
import math
import Test_def as D
import Test_classe_tile as CT
import Test_classe_humain as CH
import Test_classe_objets as CO
import winreg

def audio_device_available():
    # Retourne True si Windows a AU MOINS un périphérique audio fonctionnel.
    # On lit le registre Windows : s'il n'y a aucun endpoint audio actif,
    # pygame.mixer ne doit PAS être initialisé.
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render")
        pygame.mixer.init()
        audio = True
        return audio
    except: 
        audio = False
        pygame.mixer.init()
        return audio
audio = audio_device_available()
pygame.display.init()
pygame.font.init()







###-------------------------------------------------------
### ------------- CODE EUDOCIE
###-------------------------------------------------------

# Chemins
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")
police_dir = os.path.join(assets_dir,"polices")
police_dialogue_path = os.path.join(police_dir, "police_dialogue.ttf")
if audio:
    dialogue_sounds_path = os.path.join(sounds_dir, "typewriter.mp3")
    text_sound = pygame.mixer.Sound(dialogue_sounds_path)
    text_sound.set_volume(0.5)

# pygame setup
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
fps = 120

# Variables fade
FADE_BLACK = 0
FADE_TO_EARTH = 1  
SHOW_EARTH = 2      
FADE_TO_DIALOGUE = 3 
SHOW_DIALOGUE = 4   
GAME_PLAY = 5     
current_state = FADE_BLACK
earth_timer = fps *2
fade_alpha = 255 
fade_speed = 60/fps
fade_active = True
timer = fps * 0.5 # 7/6
fade2_active = False
earth_active = False

# Variables dialogue
counter = 0
speed = round(4 * 60/fps)
done = False
active_message = 0
dialogue_box = True
current_frame = 0
animation_speed = 0.3 * 60/fps

# Chargement des assets  ### pour le dialogue
liste_dialoges = C_D.objets
dialogue_image = pygame.image.load(os.path.join(assets_dir, "dialogue_box.png"))
dialogue_box_width = 400
dialogue_box_height = 200
dialogue_box_x = (screen.get_width() - dialogue_box_width) // 2
dialogue_box_y = (screen.get_height() - dialogue_box_height) // 2
dialogue_box = True
dialogue_1 = C_D.Dialogue(640, 600, 894, 200, dialogue_image, police_dialogue_path, 
                          ["Initialisation…", "Unité de nettoyage autonome : R-0.", 
                           "Statut de la planète : inhabitable.", 
                           "Mission prioritaire : nettoyer."], next)
message = dialogue_1.dialogue_text[active_message]

# Frames pour planète
frames = []
for i in range(30):
    img = pygame.image.load(f"assets/earth/sprite_{i:02d}.png")
    img = pygame.transform.scale(img,(256,256))
    frames.append(img)


see_animations = False
cooldown_dialogue = True
###-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------
W,H = (1280, 720)
W_2,H_2 = W/2,H/2
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
LEN_SQUARE = 64
dt = 0

Taille_map = 200
Actual_map = D.creation_map_rectangle(Taille_map,Taille_map,0)
Actual_map_pollution = D.set_pollution_map_rectangle(Taille_map,Taille_map,Actual_map,5)
Actual_map_objects_layer = D.creation_map_rectangle(Taille_map,Taille_map,-1)
pollution_initiale = numpy.sum(Actual_map_pollution)
pollution_max_possible = pollution_initiale


Nom_image_list_tiles = ["background_1.png","background_2.png","Bush_tile.png","pollution_texture.png","transparent.png"]
List_tiles = [CT.Tile(Nom_image_list_tiles[0],None,0),CT.Tile(Nom_image_list_tiles[0],None,90),CT.Tile(Nom_image_list_tiles[0],None,180),CT.Tile(Nom_image_list_tiles[0],None,270),\
              CT.Tile(Nom_image_list_tiles[1],None,0),CT.Tile(Nom_image_list_tiles[1],None,90),CT.Tile(Nom_image_list_tiles[1],None,180),CT.Tile(Nom_image_list_tiles[1],None,270),\
              CT.Tile(Nom_image_list_tiles[2],None,0),
              CT.Tile(Nom_image_list_tiles[3],None,0),
              CT.Tile(Nom_image_list_tiles[4],None,0)]

for y in range(Actual_map.shape[0]):
    for x in range(Actual_map.shape[1]):
        Actual_map[x,y] = random.randint(0,7)
# print(Actual_map_pollution)

List_ground_objets = []
pomme = CO.Consumable("apple.png","Pomme","Une pomme bien délicieuse")
List_ground_objets.append((pomme,(300,200)))
bush = CO.Plant("bush.png","Buisson","Ce buisson permet de cultiver des pommes",List_tiles[2],8)


Arial_font = pygame.font.SysFont('Arial', 30)
Surface_text_pickup = Arial_font.render('Press [E] to pick it up !', False, (255,255,255))
can_pickup = True
can_see_pollution = True
cd_see_pollution = True


hotbar = [bush,None,None,None,None]
Robot = CH.Humanoid((15*LEN_SQUARE,15*LEN_SQUARE),100,5,5,"robot_front_wait.png",["robot_front_walking.png"],LEN_SQUARE,hotbar)
print("running now")



###-------------------------------------------------------
### ------------- CODE EUDOCIE + START UN PEU EMIL
###-------------------------------------------------------
while running:
    time_0 = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    if current_state != GAME_PLAY:
        if not see_animations:
            current_state = GAME_PLAY
            fade_alpha = 0
        if see_animations:  
            if current_state == FADE_BLACK:
                if timer > 0:
                    timer -=1
                else:
                    timer = 0
                    current_state = FADE_TO_EARTH
                    print("fade1 finis")

            if current_state == FADE_TO_EARTH:
                current_frame += animation_speed
                if current_frame >= len(frames):
                    current_frame = 0
                earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
                screen.blit(frames[int(current_frame)], earth_rect) 
                fade_alpha -= fade_speed 
                if fade_alpha <= 0:
                    fade_alpha = 0
                    current_state = SHOW_EARTH
                    print("fade2 finis")

            if current_state == SHOW_EARTH:
                current_frame += animation_speed
                if current_frame >= len(frames):
                    current_frame = 0
                earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
                screen.blit(frames[int(current_frame)], earth_rect) 
                earth_timer -= 1
                if earth_timer <=0:
                    current_state = FADE_TO_DIALOGUE
                    fade_alpha = 0
                    print('look at earth finis')

            if current_state == FADE_TO_DIALOGUE:
                current_frame += animation_speed
                if current_frame >= len(frames):
                    current_frame = 0
                earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
                screen.blit(frames[int(current_frame)], earth_rect) 
                fade_alpha += fade_speed
                if fade_alpha >= 255:
                    current_state = SHOW_DIALOGUE
                    fade_alpha = 0
                    print('fade3 finis')

            if current_state == SHOW_DIALOGUE: 
                for object in liste_dialoges:
                    object.process()   # ya une fonctions next qui fait directement changer le prochain current state
                    object.draw(screen) 
                previous_counter = counter
                if counter < speed * len(message) :
                    counter +=1
                elif counter >= speed * len(message):
                    done = True
                    text_sound.stop()
                current_char = counter // speed
                previous_char = previous_counter // speed
                if current_char == 1 and previous_char == 0 and not done and not fade_active and dialogue_box and not fade2_active:
                    text_sound.play()
                dialogue_1.snip = message[0:counter//speed]

                if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and cooldown_dialogue == False:
                    cooldown_dialogue = True
                    print(cooldown_dialogue)
                    if done:
                        if active_message < len(dialogue_1.dialogue_text) - 1:
                            active_message += 1
                            done = False
                            message = dialogue_1.dialogue_text[active_message]
                            counter = 0
                            text_sound.stop()
                        else :  
                            current_state = GAME_PLAY
                            dialogue_box = False
                            text_sound.stop()                        
                    else:
                        counter = speed * len(message)
                        done = True
                        text_sound.stop() 
                if keys[pygame.K_SPACE] == False:
                    cooldown_dialogue = False



###-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------
    if current_state == GAME_PLAY:
        coin_haut = (math.floor((Robot.pos[0]-W_2)/64),math.floor((Robot.pos[1]-H_2)/64))
        coin_bas = (math.ceil((Robot.pos[0]+W_2)/64),math.ceil((Robot.pos[1]+H_2)/64))

        for y in range(max(coin_haut[1],0),min(coin_bas[1],Actual_map.shape[0])): # montre la map
            for x in range(max(coin_haut[0],0),min(coin_bas[0],Actual_map.shape[1])):
                List_tiles[Actual_map[x,y]].blit_self(screen,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))
                List_tiles[Actual_map_objects_layer[x,y]].blit_self(screen,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))
                if can_see_pollution:
                    tile_surface = List_tiles[-2].image.copy()
                    tile_surface.set_alpha(Actual_map_pollution[x,y]*10)
                    screen.blit(tile_surface,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))

        if keys[pygame.K_e]: #recuperer objets
            for obj in List_ground_objets:
                if (Robot.pos[0] - obj[1][0])**2 +(Robot.pos[1] - obj[1][1])**2 <= (LEN_SQUARE*Robot.range_pickup)**2 and can_pickup:
                    can_pickup = False
                    if Robot.pickup(obj[0]):
                        List_ground_objets.remove(obj)
        else:
            can_pickup = True               

        if keys[pygame.K_F3]:              
            if cd_see_pollution == False:
                can_see_pollution = not can_see_pollution
                cd_see_pollution = True
        else:
            cd_see_pollution = False

        if keys[pygame.K_n]:
            if Robot.hotbar[Robot.held_item_indice] != None:
                List_ground_objets.append((Robot.hotbar[Robot.held_item_indice],Robot.pos))
                Robot.hotbar[Robot.held_item_indice] = None


        for obj in List_ground_objets: # mettre le texte pick up
            if (Robot.pos[0] - obj[1][0])**2 +(Robot.pos[1] - obj[1][1])**2 <= (LEN_SQUARE*Robot.range_pickup)**2:
                screen.blit(Surface_text_pickup, (obj[1][0]-Robot.pos[0]+W_2-Surface_text_pickup.get_size()[0]/2, obj[1][1]-Robot.pos[1]+H_2-Surface_text_pickup.get_size()[1]/2 - 32 - 10 - 8*math.cos(time.time())))
            screen.blit(pygame.transform.scale(obj[0].image,(32,32)),(obj[1][0]-Robot.pos[0]+W_2 - 16,obj[1][1]-Robot.pos[1]+H_2 - 16))



        Pos_souris_monde=(Robot.pos[0]-W_2+mouse_pos[0],Robot.pos[1]-H_2+mouse_pos[1]) # position de la souris ds le monde en pixels
        tile_souris = ((Pos_souris_monde[0]//LEN_SQUARE)*LEN_SQUARE,(Pos_souris_monde[1]//LEN_SQUARE)*LEN_SQUARE) # on va floor (si victor a raison que cest un floor mdr) la position a la case 
        centre_tile = (tile_souris[0]+32,tile_souris[1]+32) # on prends dcp le centre de la tile, en gros c juste len_square /2 mais on va simplifier
        diff = (centre_tile[0]-Robot.pos[0],centre_tile[1]-Robot.pos[1]) # reconversion en pos ecran

        if Robot.hotbar[Robot.held_item_indice] != None and Robot.hotbar[Robot.held_item_indice].can_see == True:
            if diff[0]**2+diff[1]**2<=(Robot.range_pickup*LEN_SQUARE+LEN_SQUARE)**2:
                screen_pos=(W_2-(Robot.pos[0]-tile_souris[0]),H_2-(Robot.pos[1]-tile_souris[1]))
                pygame.draw.rect(screen,"red",(screen_pos[0],screen_pos[1],LEN_SQUARE,LEN_SQUARE),2)
                if pygame.mouse.get_pressed() == (True,False,False) and 0 <= int(tile_souris[0]/64) < Actual_map.shape[0] and 0 <= int(tile_souris[1]/64) < Actual_map.shape[1]:
                    if Robot.hotbar[Robot.held_item_indice].type == "Plant":
                        Actual_map_objects_layer[int(tile_souris[0]/64),int(tile_souris[1]/64)] = Robot.hotbar[Robot.held_item_indice].indice_in_map
                        Robot.hotbar[Robot.held_item_indice] = None


        # print(Robot.pos)
        Robot.do_all(keys,dt,screen,Actual_map)






###-------------------------------------------------------
### ------------- CODE EUDOCIE
###-------------------------------------------------------
    if fade_alpha > 0 : # permet de faire le fade si yen a a faire dans le current state
        fade_surface = pygame.Surface((screen.get_width(),screen.get_height()))
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill((0, 0, 0))  
        screen.blit(fade_surface, (0, 0))
   
    if time.time()-time_0 > dt:
        print(" OH SHIT", time.time()-time_0- dt)
    pygame.display.flip()
    dt = clock.tick(fps) / 1000


pygame.quit()