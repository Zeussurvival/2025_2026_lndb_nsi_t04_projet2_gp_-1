# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os 
import classes.classe_dialogue as C_D
import winreg
import numpy
import random
import time
import math
import classes.Test_def as D
import classes.Test_classe_tile as CT
import classes.Test_classe_humain as CH
import classes.Test_classe_objets as CO
import classes.Test_classe_machines as CM
import sys

mode = sys.argv[3] if len(sys.argv) > 3 else "new"
file_path = sys.argv[4] if len(sys.argv) > 4 else None

# Chemins
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")
font_1 = os.path.join(police_dir, "test_1.ttf")
font_2 = os.path.join(police_dir, "test_2.ttf")
def audio_device_available():
    # Retourne True si Windows a AU MOINS un périphérique audio fonctionnel.
    # On lit le registre Windows : s'il n'y a aucun endpoint audio actif,
    # pygame.mixer ne doit PAS être initialisé.
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render")
        pygame.mixer.init()
    except: 
        return False

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
fps = 240

# Variables ordre
FADE_BLACK = 0  
FADE_IN_TEXT_1 = 1
SHOW_TEXT_1 = 2
FADE_TEXT_1 = 3    
FADE_TO_EARTH = 4  
SHOW_EARTH = 5
SHOW_TEXT_2 = 6   
FADE_TO_DIALOGUE = 7 
SHOW_DIALOGUE = 8
GAME_PLAY = 9
current_state = FADE_BLACK

earth_timer = 180*60/fps
fade_alpha = 255 
fade_speed = 1*60/fps
timer = 70*60/fps
text_timer = 70*60/fps

see_minimap = False 

# Variables dialogue

counter = 0
speed = round(25 * 60/fps)
done = False
active_message = 0


# Chargement des assets

dialogue_sounds_path = os.path.join(sounds_dir, "typewriter.mp3")
text_sound = pygame.mixer.Sound(dialogue_sounds_path)
text_sound.set_volume(0.5)


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)



objects = C_D.objects
counter = 0

done = False
active_message = 0
current_frame = 0
current_frame_p = 0
animation_speed = 0.3*60/fps
animation_p_speed = 0.05*60/fps
dialogue_image = pygame.image.load(os.path.join(assets_dir, "dialogue_box.png"))
police_dialogue_path = os.path.join(police_dir, "police_dialogue.ttf")
dialogue_sounds_path = os.path.join(sounds_dir, "typewriter.mp3")
text_sound = pygame.mixer.Sound(dialogue_sounds_path)
text_sound.set_volume(1)

dialogue_box_width = 400
dialogue_box_height = 200
dialogue_box_x = (screen.get_width() - dialogue_box_width) // 2
dialogue_box_y = (screen.get_height() - dialogue_box_height) // 2


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

font = pygame.font.Font(font_1, 25)
font_coord = pygame.font.Font(font_1, 15)
text_1 = font.render("Cela fait 732 années que les humains ont quitté cette planète", 1, (255, 255, 255))
text_2 = font.render("Ils ont laissé derrière eux… ceci.", 1, (255, 255, 255))
text_rect_1 = text_1.get_rect(center=(640, 360))
text_rect_2 = text_2.get_rect(center=(640, 100))

dialogue_1 = C_D.Dialogue(640, 600, 894, 200, dialogue_image, police_dialogue_path, 
                          ["Initialisation…", "Unité de nettoyage autonome : Xénia.", 
                           "Statut de la planète : inhabitable.", 
                           "Mission prioritaire : nettoyer."], next)

message = dialogue_1.dialogue_text[active_message]


frames = []
frames_pollution_earth = []
for i in range(30):

    img = pygame.image.load(f"assets/earth/sprite_{i:02d}.png")
    img = pygame.transform.scale(img,(256,256))
    frames.append(img)

for i in range(1, 6):

    img = pygame.image.load(f"assets/pollution_cloud/pollution{i}.png")
    img = pygame.transform.scale(img,(256,256))
    frames_pollution_earth.append(img)
see_animations = False
cooldown_dialogue = False

#MINIMAP
def draw_minimap(screen, Robot, Actual_map, Actual_map_pollution, tileset_paths, LEN_SQUARE, W, H):

    minimap_scale = 3        
    minimap_range = 30      
    minimap_size = minimap_range * 2 * minimap_scale
    minimap_x = 10           
    minimap_y = 10

    # Fond semi-transparent
    minimap_surf = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
    minimap_surf.fill((0, 0, 0, 150))

    
    player_tile_x = int(Robot.pos[0] // LEN_SQUARE)
    player_tile_y = int(Robot.pos[1] // LEN_SQUARE)

    for dy in range(-minimap_range, minimap_range):
        for dx in range(-minimap_range, minimap_range):
            tx = player_tile_x + dx
            ty = player_tile_y + dy
            if 0 <= tx < Actual_map.shape[0] and 0 <= ty < Actual_map.shape[1]:

                px = (dx + minimap_range) * minimap_scale
                py = (dy + minimap_range) * minimap_scale
                tile_indice = Actual_map[tx, ty]
                if 8 <= tile_indice < len(tileset_paths) - 3:
                    pygame.draw.rect(minimap_surf, (255, 0, 0), (px, py, minimap_scale, minimap_scale))
                else:
                    pygame.draw.rect(minimap_surf, (20, 60, 20), (px, py, minimap_scale, minimap_scale))
                pollution = Actual_map_pollution[tx, ty]
                alpha = min(180, int(pollution * 12))

                if alpha > 0:
                    pollution_tile = pygame.Surface((minimap_scale, minimap_scale), pygame.SRCALPHA)
                    pollution_tile.fill((255, 255, 0, alpha))
                    minimap_surf.blit(pollution_tile, (px, py))

    pygame.draw.rect(minimap_surf, (255, 255, 255),
                     (minimap_range * minimap_scale - 2, minimap_range * minimap_scale - 2, 4, 4))

    screen.blit(minimap_surf, (minimap_x, minimap_y))
    coords_text = font_coord.render(f"X: {player_tile_x}  Y: {player_tile_y}", True, (255, 255, 255))
    screen.blit(coords_text, (minimap_x, minimap_y + minimap_size + 5))




###-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------

### SETUP PYGAME ET IMPORTANTS
W,H = (1280, 720)
W_2,H_2 = W/2,H/2
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
LEN_SQUARE = 64
dt = 0
construction_dir = os.path.join(assets_dir,"Building_txt")
tiles_dir = os.path.join(assets_dir,"Tiles")
autres_tiles_dir = os.path.join(tiles_dir,"Autres")
batiments_tiles_dir = os.path.join(tiles_dir,"Batiment")

### CREATION MAP
Taille_map = int(sys.argv[1]) if len(sys.argv) > 1 else 20
pt_pollution = int(sys.argv[2]) if len(sys.argv) > 2 else 3
pt_pollution *= 3
List_batiments = []

for file in os.listdir(os.path.join("assets","Building_txt")):
    bat_actuel = []
    with open(os.path.join("assets","Building_txt", file),"r") as f:
        for line in f:
            bat_actuel.append(line.strip())
    List_batiments.append(bat_actuel)

seed = random.seed(time.time()) # creation de la map des settings de la pollu et autres

# Actual_map = D.creation_map_rectangle(Taille_map,Taille_map,0)

if mode == "load" and file_path and os.path.exists(file_path):
    Actual_map = numpy.loadtxt(file_path, dtype=int)
    Actual_map_objects_layer = numpy.loadtxt("testobjects.txt", dtype=int)
    Actual_map_pollution = numpy.loadtxt("testpollution.txt", dtype=int)
    result = D.set_pollution_map_rectangle(pt_pollution, seed, Actual_map, 5, 10, 1, 10)
    Liste_dechets = result[1]  # juste pour avoir la liste
else:
    Actual_map = D.creation_map_rectangle(Taille_map, Taille_map, 0)
    Actual_map_objects_layer = D.creation_map_rectangle(Taille_map, Taille_map, -1)
    result = D.set_pollution_map_rectangle(pt_pollution, seed, Actual_map, 5, 10, 1, 10)
    Actual_map_pollution = result[0]
    Liste_dechets = result[1]
    for y in range(Actual_map.shape[0]):
        for x in range(Actual_map.shape[1]):
            Actual_map[x,y] = random.randint(0,7)


pollution_initiale = numpy.sum(Actual_map_pollution)
pollution_actuelle = pollution_initiale
pollution_max_possible = pollution_initiale *2



### ENREGISTREMENT DES TILES
tileset = []
tileset_paths = []
tileset_paths += [os.path.join(autres_tiles_dir,"background_1.png"),os.path.join(autres_tiles_dir,"background_2.png"),os.path.join(autres_tiles_dir,"background_3.png"),os.path.join(autres_tiles_dir,"background_4.png")]\
               + [os.path.join(autres_tiles_dir,"background_5.png"),os.path.join(autres_tiles_dir,"background_6.png"),os.path.join(autres_tiles_dir,"background_7.png"),os.path.join(autres_tiles_dir,"background_8.png")]
dict_image_bats = {}
for i in range(len(tileset_paths)):
    tile = tileset_paths[i]
    dict_image_bats[tile] = len(tileset_paths)
    tileset.append(CT.Tile(tile,None,0))

for img in os.listdir(batiments_tiles_dir):
    true_img = os.path.join(batiments_tiles_dir,img)
    dict_image_bats[true_img] = len(tileset_paths)
    tileset_paths.append(true_img)
    tileset.append(CT.Tile(true_img,None,0))

Bats_in_map = []
for bat in List_batiments:
    temp_list = []
    x,y = bat[0],bat[1]
    for elmt in bat[2:]:
        temp_list.append(dict_image_bats[os.path.join(batiments_tiles_dir,elmt)])
    Bats_in_map.append(D.list_dindice_avec_param_en_indice_0_1_vers_matrice([int(x),int(y)]+temp_list))
Bats_zones_in_map = []
Bats_in_map = [D.replace_matrice_big_then_small(Actual_map_objects_layer,Bats_in_map[0],(0,0))]



temp_list = ["Depollution_machine_t_1.png","Bush_tile.png","pollution_texture.png","transparent.png"]
for tile in temp_list:
    true_path = os.path.join(autres_tiles_dir,tile)
    if true_path not in dict_image_bats:
        dict_image_bats[true_path] = len(tileset)
        tileset_paths += [true_path]
        tileset += [CT.Tile(os.path.join(true_path),None,0)]


### AUTRES
List_machines_depollution = []
machine_depo_1_obj = CO.Machine_objet("Depollution_machine_t_1_objet.png","MAchine de dépollution","Une machine pour dépolluer les environs",1,"Depollution_machine_t_1.png",dict_image_bats[os.path.join(autres_tiles_dir,"Depollution_machine_t_1.png")])


List_ground_objets = []
pomme = CO.Consumable("apple.png","Pomme","Une pomme bien délicieuse")
List_ground_objets.append((pomme,(300,200)))
Bush_basique = CO.Plant("bush.png","Buisson","Ce buisson permet de cultiver des pommes",tileset[dict_image_bats[os.path.join(autres_tiles_dir,"Bush_tile.png")]],len(tileset)-3)
bush = Bush_basique
Liste_bush_on_map = []

Arial_font = pygame.font.SysFont('Arial', 30)
Surface_text_pickup = Arial_font.render('Press [E] to pick it up !', False, (255,255,255))
can_pickup = True
can_see_pollution = True
cd_see_pollution = True

hotbar = [bush,machine_depo_1_obj,None,None,None]
Robot = CH.Humanoid((3*LEN_SQUARE,3*LEN_SQUARE),100,5,5,"robot_front_walking.png",["robot_front_walking.png"],LEN_SQUARE,hotbar)
time_for_every_sec = int(time.time())
time_for_every_30_sec = int(time.time())


print("running now")
while running:
    time_0 = time.time()
    keys = pygame.key.get_pressed()  
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((0,0,0))
    if not see_animations:
        current_state = GAME_PLAY
        fade_alpha = 0
    if current_state != GAME_PLAY:
        if current_state == FADE_BLACK:
            if timer > 0:
                timer -=1
            else :
                current_state = FADE_IN_TEXT_1
                fade_alpha = 255 
        
                print("fade1 finis")

        elif current_state == FADE_IN_TEXT_1:

            screen.blit(text_1, text_rect_1)
            fade_alpha -= fade_speed 
            if fade_alpha <= 0:
                fade_alpha = 0
                current_state = SHOW_TEXT_1
                print("Texte 1 ")
        elif current_state == SHOW_TEXT_1:
            screen.blit(text_1, text_rect_1)
            if text_timer > 0:
                text_timer -= 1
            else:
                current_state = FADE_TEXT_1
                fade_alpha = 0    
        elif current_state == FADE_TEXT_1:
            screen.blit(text_1, text_rect_1)
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                current_state = FADE_TO_EARTH
                print("vers la terre")
        elif current_state == FADE_TO_EARTH:
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect) 
            current_frame_p += animation_p_speed
            if current_frame_p >= len(frames_pollution_earth):
                current_frame_p = 0
            pollution_rect = frames_pollution_earth[int(current_frame_p)].get_rect(center=(640, 360))
            screen.blit(frames_pollution_earth[int(current_frame_p)], pollution_rect) 
            screen.blit(text_2, text_rect_2) 
            fade_alpha -= fade_speed 
            if fade_alpha <= 0:
                fade_alpha = 0
                current_state = SHOW_EARTH
                print("terre visible")
        elif current_state == SHOW_EARTH:
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect) 
            current_frame_p += animation_p_speed
            if current_frame_p >= len(frames_pollution_earth):
                current_frame_p = 0
            pollution_rect = frames_pollution_earth[int(current_frame_p)].get_rect(center=(640, 360))
            screen.blit(frames_pollution_earth[int(current_frame_p)], pollution_rect)
            screen.blit(text_2, text_rect_2)  
            earth_timer -= 1
            if earth_timer <=0:
                current_state = FADE_TO_DIALOGUE
                fade_alpha = 0

        elif current_state == FADE_TO_DIALOGUE :
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect)
            current_frame_p += animation_p_speed
            if current_frame_p >= len(frames_pollution_earth):
                current_frame_p = 0
            pollution_rect = frames_pollution_earth[int(current_frame_p)].get_rect(center=(640, 360))
            screen.blit(frames_pollution_earth[int(current_frame_p)], pollution_rect)
            screen.blit(text_2, text_rect_2)  
            fade_alpha += fade_speed
            if fade_alpha >= 255 :
                current_state = SHOW_DIALOGUE
                fade_alpha = 0
                
        elif current_state == SHOW_DIALOGUE: 
            for object in objects:
                object.process()
                object.draw(screen)
            previous_counter = counter 
            if counter < speed * len(message) :
                counter +=1
            elif counter >= speed * len(message):
                done = True
                text_sound.stop()
            current_char = counter // speed
            previous_char = previous_counter // speed
            if current_char == 1 and previous_char == 0 and not done:
                text_sound.play()
            dialogue_1.snip = message[0:counter//speed]

            if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] and cooldown_dialogue == False:
                cooldown_dialogue = True
                if done:
                    if active_message < len(dialogue_1.dialogue_text) - 1:
                        active_message += 1
                        done = False
                        message = dialogue_1.dialogue_text[active_message]
                        counter = 0
                        text_sound.stop()
                    else:  
                        current_state = GAME_PLAY
                        text_sound.stop()                        
                else:
                    counter = speed * len(message)
                    done = True
                    text_sound.stop()
            if not keys[pygame.K_RETURN] and not keys[pygame.K_SPACE]:
                cooldown_dialogue = False

##-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------  
    if current_state == GAME_PLAY:
        see_minimap = True
        coin_haut = (math.floor((Robot.pos[0]-W_2)/LEN_SQUARE),math.floor((Robot.pos[1]-H_2)/LEN_SQUARE))
        coin_bas = (math.ceil((Robot.pos[0]+W_2)/LEN_SQUARE),math.ceil((Robot.pos[1]+H_2)/LEN_SQUARE))

        for y in range(max(coin_haut[1],0),min(coin_bas[1],Actual_map.shape[0])): # montre la map
            for x in range(max(coin_haut[0],0),min(coin_bas[0],Actual_map.shape[1])):
                tileset[Actual_map[x,y]].blit_self(screen,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))
                tileset[Actual_map_objects_layer[x,y]].blit_self(screen,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))
                if can_see_pollution:
                    tile_surface = tileset[-2].image.copy()
                    tile_surface.set_alpha(Actual_map_pollution[x,y]*10)
                    screen.blit(tile_surface,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))


        if keys[pygame.K_e]: #recuperer objets
            for obj in List_ground_objets:
                if (Robot.pos[0] - obj[1][0])**2 +(Robot.pos[1] - obj[1][1])**2 <= (LEN_SQUARE*Robot.range_pickup)**2 and can_pickup:
                    can_pickup = False
                    if Robot.pickup(obj[0]):
                        List_ground_objets.remove(obj)
                        for y in range(Actual_map_pollution.shape[0]):
                            for x in range(Actual_map_pollution.shape[1]):
                                Actual_map_pollution[x, y] -= 0.1
                                if Actual_map_pollution[x, y] < 0:
                                    Actual_map_pollution[x, y] = 0
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
                screen.blit(Surface_text_pickup, (obj[1][0]-Robot.pos[0]+W/2-Surface_text_pickup.get_size()[0]/2, obj[1][1]-Robot.pos[1]+H/2-Surface_text_pickup.get_size()[1]/2 - 32 - 10 - 8*math.cos(time.time())))
            screen.blit(pygame.transform.scale(obj[0].image,(32,32)),(obj[1][0]-Robot.pos[0]+W/2 - 16,obj[1][1]-Robot.pos[1]+H/2 - 16))



        Pos_souris_monde=(Robot.pos[0]-W/2+mouse_pos[0],Robot.pos[1]-H/2+mouse_pos[1]) # position de la souris ds le monde en pixels
        tile_souris = ((Pos_souris_monde[0]//LEN_SQUARE)*LEN_SQUARE,(Pos_souris_monde[1]//LEN_SQUARE)*LEN_SQUARE) # on va floor (si victor a raison que cest un floor mdr) la position a la case 
        centre_tile = (tile_souris[0]+32,tile_souris[1]+32) # on prends dcp le centre de la tile, en gros c juste len_square /2 mais on va simplifier
        diff = (centre_tile[0]-Robot.pos[0],centre_tile[1]-Robot.pos[1]) # reconversion en pos ecran


        if Robot.hotbar[Robot.held_item_indice] != None and Robot.hotbar[Robot.held_item_indice].can_see == True:
            if diff[0]**2+diff[1]**2<=(Robot.range_pickup*LEN_SQUARE+LEN_SQUARE)**2:
                screen_pos=(W/2-(Robot.pos[0]-tile_souris[0]),H/2-(Robot.pos[1]-tile_souris[1]))
                pygame.draw.rect(screen,"red",(screen_pos[0],screen_pos[1],LEN_SQUARE,LEN_SQUARE),2)
                if pygame.mouse.get_pressed() == (True,False,False) and 0 <= int(tile_souris[0]/LEN_SQUARE) < Actual_map.shape[0] and 0<= int(tile_souris[1]/LEN_SQUARE) < Actual_map.shape[1]:
                    if Robot.hotbar[Robot.held_item_indice].type == "Plant":
                        Actual_map_objects_layer[int(tile_souris[0]/LEN_SQUARE),int(tile_souris[1]/LEN_SQUARE)] = Robot.hotbar[Robot.held_item_indice].indice_in_map
                        Robot.hotbar[Robot.held_item_indice] = None
                        Liste_bush_on_map.append([(int(tile_souris[0]/LEN_SQUARE),int(tile_souris[1]/LEN_SQUARE)) ,math.floor(time.time())+random.randint(30,50)])
                        
                    elif Robot.hotbar[Robot.held_item_indice].type == "Machine_objet":
                        List_machines_depollution.append(CM.Depollution((int(tile_souris[0]/LEN_SQUARE),int(tile_souris[1]/LEN_SQUARE)),0.1,5,1,polu_capa_max=40))
                        Actual_map_objects_layer[int(tile_souris[0]/64),int(tile_souris[1]/64)] = Robot.hotbar[Robot.held_item_indice].indice_in_map
                        Robot.hotbar[Robot.held_item_indice] = None
                        

        if time_for_every_sec +1 <= int(time.time()):
            for bush in Liste_bush_on_map:
                if bush[1] <= int(time.time()):
                    bush[1] = int(time.time())+random.randint(30,50)
                    print("ya eu le bush")
                    List_ground_objets.append([Bush_basique,(bush[0][0]*LEN_SQUARE+LEN_SQUARE/2 + random.randint(int(LEN_SQUARE/2),LEN_SQUARE)*(random.randint(0,1) *2 -1),
                                                            bush[0][1]*LEN_SQUARE+LEN_SQUARE/2+ random.randint(int(LEN_SQUARE/2),LEN_SQUARE)*(random.randint(0,1) *2 -1))])
            time_for_every_sec = int(time.time())+1

        if time_for_every_30_sec + 30 <= int(time.time()):
            for machine in List_machines_depollution:
                if machine.polu_capa < machine.polu_capa_max:
                    chng = D.to_remove_bro(Actual_map_pollution,machine.location,machine.range_depo,machine.polu_reduced_per_30_sec,machine.polu_capa_max - machine.polu_capa)
                    machine.polu_capa += chng
            time_for_every_30_sec = int(time.time()) + 30
            pollution_actuelle = numpy.sum(Actual_map_pollution)


        #AFFICHAGE INDICE POLLUTION
        if pollution_max_possible > 0:
            pourcentage_pollution = pollution_actuelle/pollution_max_possible*100
        else:
            pourcentage_pollution = 0
        indice_width = 200
        indice_height = 30
        indice_x = W - indice_width - 20
        indice_y = 20
        interface_padding = 12
        interface_rect = pygame.Rect(indice_x - interface_padding, 
                                     indice_y - interface_padding, 
                                     indice_width + 2*interface_padding, 
                                     indice_height + 50)
        interface_surface = pygame.Surface((interface_rect.width, interface_rect.height))
        interface_surface.set_alpha(200)
        interface_surface.fill((20, 20, 20))
        screen.blit(interface_surface, interface_rect.topleft)
        pollution_value_font = pygame.font.Font(font_1, 20)
        pollution_value_text = pollution_value_font.render(f"{pourcentage_pollution:.1f}%", 1, (255, 255, 255))
        value_rect = pollution_value_text.get_rect(center=(indice_x + indice_width/2, indice_y + 30))
        screen.blit(pollution_value_text, value_rect)

        # print(Robot.pos[0]//64,Robot.pos[1]//64)
        Robot.do_all(keys,dt,screen,Actual_map,LEN_SQUARE)

###-------------------------------------------------------
### ------------- CODE EUDOCIE
###-------------------------------------------------------
    if fade_alpha > 0 : # permet de faire le fade si yen a a faire dans le current state
        fade_surface = pygame.Surface((screen.get_width(),screen.get_height()))
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill((0, 0, 0))  
        screen.blit(fade_surface, (0, 0))
    if see_minimap == True :
        draw_minimap(screen, Robot, Actual_map_objects_layer, Actual_map_pollution, tileset_paths, LEN_SQUARE, W, H)

    # if time.time()-time_0 > dt:
    #     print(" OH SHIT", time.time()-time_0- dt)

    pygame.display.flip()
    dt = clock.tick(fps) / 1000
pygame.quit()
numpy.savetxt("testmap.txt", Actual_map, fmt="%d")  
numpy.savetxt("testobjects.txt", Actual_map_objects_layer, fmt="%d")  
numpy.savetxt("testpollution.txt", Actual_map_pollution, fmt="%d")