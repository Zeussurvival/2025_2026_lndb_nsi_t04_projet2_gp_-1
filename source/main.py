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
import json

mode = sys.argv[3] if len(sys.argv) > 3 else "new"
file_path = sys.argv[4] if len(sys.argv) > 4 else None
objects_path = sys.argv[5] if len(sys.argv) > 5 else None
pollution_path = sys.argv[6] if len(sys.argv) > 6 else None
first_machine_placed = False
machine_dialogue_active = False
first_craft = False
craft_dialogue_active = False
ship_moving = True
ship_finished = False
ship_visible = True

# Chemins
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")
saves_dir = os.path.join(main_dir, "saves")
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
FADE_BLACK_END = 10
FADE_TO_END_3 = 11
FADE_TO_END_4 = 12
FADE_TO_END_5 = 13
FADE_TO_END_6 = 14
SHOW_EARTH_END = 15
END = 16

current_state = FADE_BLACK

earth_timer = 180*60/fps
fade_alpha = 255 
fade_speed = 1*60/fps
timer = 70*60/fps
text_timer = 70*60/fps
end_text_timer = 180*60/fps
see_minimap = False 

animation_ship_speed = 0.3*60/fps
ship_y = 800
ship_x = 640
ship_target_y = 500
ship_speed = 200
ship_moving = True
current_frame_ship = 0

# Variables dialogue

counter = 0
# speed = round(25 * 60/fps)
speed = 2
done = False
active_message = 0
machine_dialogue_cooldown = 0
machine_dialogue_cooldown_delay = 200 


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
text_3 = font.render("Une fois la planète entièrement nettoyée, tout semble enfin apaisé.", 1, (255, 255, 255))
text_4 = font.render("Le joueur a accompli sa mission : rendre la planète de nouveau habitable.", 1, (255, 255, 255))
text_5 = font.render("Cependant, cet équilibre est de courte durée.", 1, (255, 255, 255))
text_6 = font.render("La planète, pourtant sauvée, commence à replonger dans le même état critique qu’auparavant.", 1, (255, 255, 255))
text_rect_3 = text_3.get_rect(center=(640, 100))
text_rect_4 = text_4.get_rect(center=(640, 100))
text_rect_5 = text_5.get_rect(center=(640, 100))
text_rect_6 = text_6.get_rect(center=(640, 100))

dialogue_1 = C_D.Dialogue(640, 600, 894, 200, dialogue_image, police_dialogue_path, 
                          ["Initialisation…", "Unité de nettoyage autonome : Xénia.", 
                           "Statut de la planète : inhabitable.", 
                           "Mission prioritaire : nettoyer."], lambda: None)

message = dialogue_1.dialogue_text[active_message]


frames = []
frames_pollution_earth = []
frames_starship = []
for i in range(30):

    img = pygame.image.load(f"assets/earth/sprite_{i:02d}.png")
    img = pygame.transform.scale(img,(256,256))
    frames.append(img)

for i in range(1, 6):

    img = pygame.image.load(f"assets/pollution_cloud/pollution{i}.png")
    img = pygame.transform.scale(img,(256,256))
    frames_pollution_earth.append(img)

for i in range(11):
    img = pygame.image.load(f"assets/spaceship_long/ship_frame{i:02d}.png")
    img = pygame.transform.scale_by(img, 2)
    frames_starship.append(img)




### VOIR ANIMATIONS
see_animations = False 
cooldown_dialogue = False


see_animation_end = False




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
                tile_indice = Actual_map[ty, tx]
                if 8 <= tile_indice < len(tileset_paths) - 3:
                    pygame.draw.rect(minimap_surf, (111, 166, 150), (px, py, minimap_scale, minimap_scale))
                else:
                    pygame.draw.rect(minimap_surf, (80, 85, 80), (px, py, minimap_scale, minimap_scale))
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
Taille_map = int(sys.argv[1]) if len(sys.argv) > 1 else 40
pt_pollution = int(sys.argv[2]) if len(sys.argv) > 2 else 3
pt_pollution *= 3
seed = random.seed(time.time()) # creation de la map des settings de la pollu et autres





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

temp_list = ["Depollution_machine_t_1.png","plank.png","Bush_tile.png","pollution_texture.png","transparent.png"]
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
Pomme_basique = CO.Consumable("apple.png","Pomme","Une pomme bien délicieuse")
pomme = Pomme_basique
List_ground_objets.append((pomme,(1024,2048)))
Bush_basique = CO.Plant("bush.png","Buisson","Ce buisson permet de cultiver des pommes",tileset[dict_image_bats[os.path.join(autres_tiles_dir,"Bush_tile.png")]],len(tileset)-3)
bush = Bush_basique
Ferraille_basique = CO.Consumable("ferraille_v1.png", "Ferraille", "Un tas de ferraille rouillée")
ferraille = Ferraille_basique
Liste_bush_on_map = []

Arial_font = pygame.font.SysFont('Arial', 30)
Surface_text_pickup = Arial_font.render('Press [E] to pick it up !', False, (255,255,255))
can_pickup = True
can_see_pollution = True
cd_see_pollution = True

hotbar = [bush,machine_depo_1_obj,None,None,None]
inventory = [None]*25
inventory[3] = Pomme_basique
Robot = CH.Humanoid((8*64,8*64),100,5,5,"robot_front/front1.png",[["robot_front/front1.png"],\
                                                                         ["robot_back/back1.png","robot_back/back2.png","robot_back/back3.png","robot_back/back4.png"],\
                                                                         ["robot_front/front1.png","robot_front/front2.png","robot_front/front3.png","robot_front/front4.png"],\
                                                                         ["robot_left/left_0.png","robot_left/left_1.png","robot_left/left_2.png","robot_left/left_3.png"],\
                                                                         ["robot_right/right_0.png","robot_right/right_1.png","robot_right/right_2.png","robot_right/right_3.png"]], \
                    64,hotbar,inventory)




### SYSTEME DE SAUVEGARDE
if mode == "load" and file_path and os.path.exists(file_path):
    bushes_path = os.path.join(saves_dir, f"{sys.argv[7]}_bushes.json")
    machines_path = os.path.join(saves_dir, f"{sys.argv[7]}_machines.json")
    Actual_map = numpy.loadtxt(file_path, dtype=int)
    Actual_map_objects_layer = numpy.loadtxt(objects_path, dtype=int)
    Actual_map_pollution = numpy.loadtxt(pollution_path, dtype=float)

    if os.path.exists(bushes_path):
        with open(bushes_path, "r") as f:
            Liste_bush_on_map = json.load(f)
        

    for bush_data in Liste_bush_on_map:
        # bush_data == [ (y,x), next_time ]
        pos, next_time = bush_data
        y, x = pos
     
        Actual_map_objects_layer[y, x] = dict_image_bats[os.path.join(autres_tiles_dir, "Bush_tile.png")]


    if os.path.exists(machines_path):
        with open(machines_path, "r") as f:
            machines_data = json.load(f)
    List_machines_depollution = [
        CM.Depollution(
            tuple(m["location"]),
            m["polu_reduced_per_30_sec"],
            m["range_depo"],
            1,
            polu_capa_max=m["polu_capa_max"]
        ) for m in machines_data
    ]

    for i, machine in enumerate(List_machines_depollution):
        machine.polu_capa = machines_data[i]["polu_capa"]
        machine.image_path = machines_data[i].get("image_path", "Depollution_machine_t_1.png")  
        for machine in List_machines_depollution:
            x, y = machine.location
            Actual_map_objects_layer[y][x] = dict_image_bats[os.path.join(autres_tiles_dir, machine.image_path)]

    else:

        Actual_map = numpy.loadtxt(file_path, dtype=int)
        Actual_map_objects_layer = numpy.loadtxt(objects_path, dtype=int)
        Actual_map_pollution = numpy.loadtxt(pollution_path, dtype=float)
        result = D.set_pollution_map_rectangle(pt_pollution, seed, Actual_map, 5, 10, 1, 10)
        Liste_dechets = result[1]  # juste pour avoir la liste
    inventory_path = os.path.join(saves_dir, f"{sys.argv[7]}_inventory.json")

    if os.path.exists(inventory_path):
        with open(inventory_path, "r") as f:
            inventory_data = json.load(f)

        Robot.hotbar = []

        for item in inventory_data:
            if item is None:
                Robot.hotbar.append(None)
            elif item["type"] == "Plant":
                Robot.hotbar.append(bush)
            elif item["type"] == "Machine_objet":
                Robot.hotbar.append(machine_depo_1_obj)
            elif item["type"] == "Consumable":
                Robot.hotbar.append(pomme)
                Robot.hotbar.append(ferraille)

        while len(Robot.hotbar) < 5:
            Robot.hotbar.append(None)
else:
    Actual_map = D.creation_map_rectangle(Taille_map, Taille_map, 0)
    Actual_map_objects_layer = D.creation_map_rectangle(Taille_map, Taille_map, -1)
    result = D.set_pollution_map_rectangle(pt_pollution, seed, Actual_map, 5, 10, 1, 10)
    Actual_map_pollution = result[0]
    Liste_dechets = result[1]
    for y in range(Actual_map.shape[0]):
        for x in range(Actual_map.shape[1]):
            Actual_map[x,y] = random.randint(0,7)
    Liste_bush_on_map = []
    List_machines_depollution = []




## Creation de la dimension pour les maisons
Map_House = numpy.full((10000,100),-1)
indice_maison = 0
decallage_houses = 40

# def collision des portes
def verif_collis(souris_pos,liste_collision_portes):
    i = 0
    for rect in liste_collision_portes:
        if rect.collidepoint(souris_pos):
            return i
        i += 1
    return False




### INVENTAIRE
ingame_menu_dir = os.path.join(assets_dir,"ingame_menus")
background_inventaire = pygame.image.load(os.path.join(ingame_menu_dir,"inventaire.png")).convert_alpha()
background_inventaire = pygame.transform.scale2x(background_inventaire)
background_craft = pygame.image.load(os.path.join(ingame_menu_dir,"craft.png")).convert_alpha()

first_slot_pos = (104,136)
decallage = 16
longueur_slot = 48
surfacee = pygame.Surface((longueur_slot, longueur_slot),pygame.SRCALPHA)
surfacee.fill((0,0,0,0))
pygame.draw.rect(surfacee, (150,150,150), (0, 0, longueur_slot, longueur_slot), 4)
picked_slot = -1
IN_INV = False
cd_inv = False

pos_image_inventaire = (150,50)

inventaire_surface = pygame.Surface((512,512),pygame.SRCALPHA)
inventaire_surface.blit(background_inventaire,(0,0))
List_collision_slots = []

# (pos_image_inventaire[0] + first_slot_pos[0]+(decallage+longueur_slot)*(i%5), pos_image_inventaire[1] + first_slot_pos[1]+(decallage+longueur_slot)*(i//5))

for n in range(25):
    inventaire_surface.blit(surfacee,(first_slot_pos[0]+(decallage+longueur_slot)*(n%5),first_slot_pos[1]+(decallage+longueur_slot)*(n//5)))
    List_collision_slots.append(pygame.Rect(pos_image_inventaire[0]+first_slot_pos[0]+(decallage+longueur_slot)*(n%5),first_slot_pos[1]+(decallage+longueur_slot)*(n//5),longueur_slot,longueur_slot))
print(List_collision_slots)



## Batiments et collisions
List_batiments_raw = []

for file in os.listdir(os.path.join("assets","Building_txt")): # va enregistrer les lignes du txt en element dans une liste
    bat_actuel = []
    with open(os.path.join("assets","Building_txt", file),"r") as f:
        for line in f:
            bat_actuel.append(line.strip())
    List_batiments_raw.append(bat_actuel)


List_bats_zones_collision_fix = [[0,0,10,8,5],[1,3,10,6,3],[1,0,10,9,3]]
List_bats_zones_collision_portes_fix = [[4,6,2,2],[3,7,1,2],[6,7,2,2]]
List_bats_zones_collision_en_plus_fix = [[  ],[ [0,6,1,2], [4,0,6,3] ],[ [11,4,1,3], [3,9,2,1], [8,9,1,1] ]]
List_batiments_net = []
for bat in List_batiments_raw: # enregistre une matrice en fct de lindice de limage dans la tileset
    temp_list = []
    x,y = bat[0],bat[1]
    for elmt in bat[2:]:
        temp_list.append(dict_image_bats[os.path.join(batiments_tiles_dir,elmt)])
    List_batiments_net.append(D.list_dindice_avec_param_en_indice_0_1_vers_matrice([int(x),int(y)]+temp_list))
Bats_zones_in_map = []

List_batiments_zones_collision = [pygame.Rect(-128,-128,Actual_map.shape[0]*64,128),pygame.Rect(-128,-128,128,Actual_map.shape[1]*64),\
                                  pygame.Rect(-128,Actual_map.shape[0]*64,Actual_map.shape[0]*64+128,128),pygame.Rect(Actual_map.shape[0]*64,-128,128,Actual_map.shape[1]*64+128)]

List_bats_zones_collision_portes = []
List_offset_entree = [[0,0],[1,-3],[-2,0]]
List_collision_house_map = []
List_entree_dans_maison = []
List_sorti_hors_maison = []
List_house_collision = []

# Ajout des Bats a la map
indice_maison = 0
def ajout_de_linterieur_de_bat(position,indice):
    global List_entree_dans_maison
    global List_sorti_hors_maison
    global List_collision_house_map
    global indice_maison
    List_batiments_zones_collision.append(pygame.Rect((position[0]+List_bats_zones_collision_fix[indice][0])*64,(position[1]+List_bats_zones_collision_fix[indice][1])*64,List_bats_zones_collision_fix[indice][2]*64,List_bats_zones_collision_fix[indice][3]*64))
    D.replace_matrice_big_then_small(Actual_map_objects_layer,List_batiments_net[indice],position)
    for t in range(len(List_bats_zones_collision_en_plus_fix[indice])):
        List_batiments_zones_collision.append(pygame.Rect((position[0]+List_bats_zones_collision_en_plus_fix[indice][t][0])*64,(position[1]+List_bats_zones_collision_en_plus_fix[indice][t][1])*64,List_bats_zones_collision_en_plus_fix[indice][t][2]*64,List_bats_zones_collision_en_plus_fix[indice][t][3]*64))
    List_bats_zones_collision_portes.append(pygame.Rect((position[0]+List_bats_zones_collision_portes_fix[indice][0])*64,(position[1]+List_bats_zones_collision_portes_fix[indice][1])*64,List_bats_zones_collision_portes_fix[indice][2]*64,List_bats_zones_collision_portes_fix[indice][3]*64))

    matrice_temp = numpy.full((List_bats_zones_collision_fix[indice][2],List_bats_zones_collision_fix[indice][3]),dict_image_bats[os.path.join(autres_tiles_dir,"plank.png")])
    D.replace_matrice_big_then_small(Map_House,matrice_temp,(0,indice*decallage_houses))
    List_entree_dans_maison += [(1+List_bats_zones_collision_portes_fix[indice][0]+indice*decallage_houses+List_offset_entree[indice][0],1+List_bats_zones_collision_portes_fix[indice][1]+List_offset_entree[indice][1])]
    List_sorti_hors_maison += [(position[0]+List_bats_zones_collision_portes_fix[indice][0]+List_bats_zones_collision_portes_fix[indice][2]+0.5,position[1]+List_bats_zones_collision_portes_fix[indice][1]+List_bats_zones_collision_portes_fix[indice][3])]
    
    pos = indice_maison*decallage_houses,0
    List_collision_house_map.append(pygame.rect.Rect(pos[0]*64-64,-64,List_bats_zones_collision_fix[indice][2]*64+128,64))
    List_collision_house_map.append(pygame.rect.Rect(pos[0]*64-64,-64,64,List_bats_zones_collision_fix[indice][3]*64+128))
    List_collision_house_map.append(pygame.rect.Rect((List_bats_zones_collision_fix[indice][2]+ pos[0])*64,-64,64,List_bats_zones_collision_fix[indice][3]*64+64))
    List_collision_house_map.append(pygame.rect.Rect(pos[0]*64-64,List_bats_zones_collision_fix[indice][3]*64,List_bats_zones_collision_fix[indice][2]*64+64,64))
    indice_maison += 1
ajout_de_linterieur_de_bat((0,0),0)
ajout_de_linterieur_de_bat((16,20),1)
ajout_de_linterieur_de_bat((0,15),0)
ajout_de_linterieur_de_bat((25,29),2)

List_batiments_zones_collision = [List_batiments_zones_collision,List_collision_house_map]
List_collision_house_map
indice_maison = -1




# KEYBINDS
touche_direction_gauche = pygame.K_q
touche_direction_droite = pygame.K_d
touche_direction_haut = pygame.K_z
touche_direction_bas = pygame.K_s
touche_affichage_pollution = pygame.K_F3
touche_jet_ditem = pygame.K_n
touche_recuperation_ditem = pygame.K_e
touche_utiliser_porte = pygame.K_f
touche_affichage_inventaire = pygame.K_TAB

# Pollu encore
pollution_initiale = numpy.sum(Actual_map_pollution)
pollution_actuelle = pollution_initiale
pollution_max_possible = pollution_initiale *2

time_for_every_sec = int(time.time())
time_for_every_30_sec = int(time.time())
List_ground_objets.append((ferraille, (10*64 + 64//2, 10*64 + 64//2)))
IN_HOUSE = False
cd_porte = False
Pos_souris_monde = (0,0)

print("running now")
while running:
    time_0 = time.time()
    keys = pygame.key.get_pressed()  
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    if not running:
        break


    if keys[pygame.K_F5]:
        current_state = FADE_BLACK_END
        fade_alpha = 255
        timer = 70*60/fps      # reset le timer du FADE_BLACK_END
        earth_timer = 180*60/fps  # reset pour SHOW_EARTH_END
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
                counter += dt * 60
            elif counter >= speed * len(message):
                done = True
                text_sound.stop()
            current_char = counter // speed
            previous_char = previous_counter // speed
            if current_char == 1 and previous_char == 0 and not done:
                text_sound.play()
            dialogue_1.snip = message[0:int(counter//speed)]

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
        elif current_state == FADE_BLACK_END:
            if timer > 0:
                timer -=1
            else :
                current_state = FADE_TO_END_3
                fade_alpha = 255 
        
                print("fade1 finis")
        elif current_state == FADE_TO_END_3:
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect) 

         
            text_surf = text_3.copy()
            text_alpha = max(0, 255 - int(fade_alpha))  
            text_surf.set_alpha(text_alpha)
            screen.blit(text_surf, text_rect_3)

            if fade_alpha > 0:
                fade_alpha -= fade_speed
            elif end_text_timer > 0:
                end_text_timer -= 1
            else:
                end_text_timer = 180*60/fps
                current_state = FADE_TO_END_4
                fade_alpha = 255

        elif current_state == FADE_TO_END_4:
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect) 


            text_surf = text_4.copy()
            text_alpha = max(0, 255 - int(fade_alpha))  
            text_surf.set_alpha(text_alpha)
            screen.blit(text_surf, text_rect_4)

            if fade_alpha > 0:
                fade_alpha -= fade_speed
            elif end_text_timer > 0:
                end_text_timer -= 1
            else:
                end_text_timer = 180*60/fps
                current_state = FADE_TO_END_5
                fade_alpha = 255
        elif current_state == FADE_TO_END_5:

   
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect)


            if ship_moving and not ship_finished:
                current_frame_ship += animation_ship_speed
                if current_frame_ship >= len(frames_starship):
                    current_frame_ship = len(frames_starship) - 1

                ship_y -= ship_speed * dt
                if ship_y <= ship_target_y:
                    ship_y = ship_target_y
                    ship_moving = False
                    ship_finished = True
                    ship_visible = False
            if ship_visible:
                ship_rect = frames_starship[int(current_frame_ship)].get_rect(center=(ship_x, ship_y))
                screen.blit(frames_starship[int(current_frame_ship)], ship_rect)

            # Texte
            text_surf = text_5.copy()
            text_alpha = max(0, 255 - int(fade_alpha))
            text_surf.set_alpha(text_alpha)
            screen.blit(text_surf, text_rect_5)

            if fade_alpha > 0:
                fade_alpha -= fade_speed
            elif end_text_timer > 0:
                end_text_timer -= 1
            else:
                end_text_timer = 180*60/fps
                current_state = FADE_TO_END_6
                fade_alpha = 255

        elif current_state == FADE_TO_END_6:
            # fade vers noir
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                current_state = SHOW_EARTH_END

        elif current_state == SHOW_EARTH_END:
            # afficher la terre finale
            current_frame += animation_speed
            if current_frame >= len(frames):
                current_frame = 0
            earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
            screen.blit(frames[int(current_frame)], earth_rect)

            end_text_timer -= 1
            if end_text_timer <= 0:
                current_state = END

        elif current_state == END:
            # écran final noir
            screen.fill((0,0,0))


##-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------  
    if current_state == GAME_PLAY:
        if not IN_HOUSE:
            
            see_minimap = True
            coin_haut = (math.floor((Robot.pos[0]-W_2)/LEN_SQUARE),math.floor((Robot.pos[1]-H_2)/LEN_SQUARE))
            coin_bas = (math.ceil((Robot.pos[0]+W_2)/LEN_SQUARE),math.ceil((Robot.pos[1]+H_2)/LEN_SQUARE))

            for y in range(max(coin_haut[1],0),min(coin_bas[1],Actual_map.shape[0])): # montre la map, polution et objet_layer
                for x in range(max(coin_haut[0],0),min(coin_bas[0],Actual_map.shape[1])):
                    tileset[Actual_map[x,y]].blit_self(screen,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))
                    tileset[Actual_map_objects_layer[y,x]].blit_self(screen,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))
                    if can_see_pollution:
                        tile_surface = tileset[-2].image.copy()
                        tile_surface.set_alpha(Actual_map_pollution[x,y]*10)
                        screen.blit(tile_surface,(x*LEN_SQUARE-Robot.pos[0]+W_2, y*LEN_SQUARE-Robot.pos[1]+H_2))


            if keys[touche_recuperation_ditem]: #recuperer objets
                for obj in List_ground_objets:
                    if (Robot.pos[0] - obj[1][0])**2 +(Robot.pos[1] - obj[1][1])**2 <= (LEN_SQUARE*Robot.range_pickup)**2 and can_pickup:
                        can_pickup = False
                        if Robot.pickup(obj[0]):
                            List_ground_objets.remove(obj)
            else:
                can_pickup = True     

                      
            result = verif_collis(Pos_souris_monde,List_bats_zones_collision_portes) # collision pour les portes
            if type(result) is int:
                indice_maison = result
            else:
                indice_maison = -1


            if keys[touche_affichage_pollution]: # afficher pollution
                if cd_see_pollution == False:
                    can_see_pollution = not can_see_pollution
                    cd_see_pollution = True
            else:
                cd_see_pollution = False

            if keys[touche_jet_ditem]: # jeter item
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

            # print("Item actuel :", Robot.hotbar[Robot.held_item_indice])
            if diff[0]**2+diff[1]**2<=(Robot.range_pickup*LEN_SQUARE+LEN_SQUARE)**2 and not IN_INV:
                if Robot.hotbar[Robot.held_item_indice] != None and Robot.hotbar[Robot.held_item_indice].can_see == True: # affichage des carrés et voir si on peut utiliser items

                    screen_pos=(W/2-(Robot.pos[0]-tile_souris[0]),H/2-(Robot.pos[1]-tile_souris[1]))
                    pygame.draw.rect(screen,"red",(screen_pos[0],screen_pos[1],LEN_SQUARE,LEN_SQUARE),2)
                    
                    if pygame.mouse.get_pressed() == (True,False,False) and 0 <= int(tile_souris[0]/LEN_SQUARE) < Actual_map.shape[0] and 0<= int(tile_souris[1]/LEN_SQUARE) < Actual_map.shape[1] and \
                    Actual_map_objects_layer[int(tile_souris[1]//64),int(tile_souris[0])//64] == -1:

                        if Robot.hotbar[Robot.held_item_indice].type == "Plant":
                            Actual_map_objects_layer[int(tile_souris[1]/LEN_SQUARE),int(tile_souris[0]/LEN_SQUARE)] = Robot.hotbar[Robot.held_item_indice].indice_in_map
                            Robot.hotbar[Robot.held_item_indice] = None
                            Liste_bush_on_map.append([(int(tile_souris[1]/LEN_SQUARE),int(tile_souris[0]/LEN_SQUARE)) ,math.floor(time.time())+random.randint(30,50)])
                            
                        elif Robot.hotbar[Robot.held_item_indice].type == "Machine_objet":
                            List_machines_depollution.append(CM.Depollution((int(tile_souris[1]/LEN_SQUARE),int(tile_souris[0]/LEN_SQUARE)),0.1,5,1,polu_capa_max=40))
                            Actual_map_objects_layer[int(tile_souris[1]/64),int(tile_souris[0]/64)] = Robot.hotbar[Robot.held_item_indice].indice_in_map
                            Robot.hotbar[Robot.held_item_indice] = None
                        if not first_machine_placed:
                            first_machine_placed = True

                            dialogue_1.dialogue_text = [
                                "Bravo, voici ta première machine.", 
                                "Elle va te permettre de purifier ton environnement.",
                                "Ta mission est simple… en apparence.",
                                "Récupère de la ferraille pour en construire plus.",
                            ]

                            active_message = 0
                            counter = 0
                            done = False
                            message = dialogue_1.dialogue_text[active_message]

                            machine_dialogue_active = True
                            see_animations = True
                            cooldown_dialogue = True
                        if not first_craft:
                            first_craft = True

                            dialogue_1.dialogue_text = [
                                "Regarde autour de toi… Ce paysage était autrefois vivant.", 
                                "La nature peut encore renaître… mais elle a besoin de toi.",
                                "Ta mission est simple… en apparence.",
                                "Nettoyer, reconstruire, et redonner vie à cet environnement.",
                                "Avec les ressources récupérées, tu peux construire des machines.",
                                "Ces machines permettent de purifier la terre et l’air."
                            
                            ]

                            active_message = 0
                            counter = 0
                            done = False
                            message = dialogue_1.dialogue_text[active_message]

                            craft_dialogue_active = True
                            see_animations = True
                            cooldown_dialogue = True

                if keys[touche_utiliser_porte] and cd_porte == False:
                    if indice_maison >= 0:
                        IN_HOUSE = True
                        Robot.last_direction = 1
                        Robot.pos_in_houses = (List_entree_dans_maison[indice_maison][0] * 64,List_entree_dans_maison[indice_maison][1]*64)
                        cd_porte = True
                if not keys[touche_utiliser_porte]:
                    cd_porte = False


            if time_for_every_sec +1 <= int(time.time()):
                for bush in Liste_bush_on_map:
                    if bush[1] <= int(time.time()):
                        bush[1] = int(time.time())+random.randint(30,50)
                        List_ground_objets.append([pomme,(bush[0][1]*64+32 + 64*(random.random() *2 -1),
                                                                bush[0][0]*64+ 32+ 64*(random.random() *2 -1))])
                        List_ground_objets.append([ferraille,(bush[0][1]*64+ 32 + 64*(random.random() *2 -1),
                                                                bush[0][0]*64+ 32+ 64*(random.random() *2 -1))])
                time_for_every_sec = int(time.time())+1

            if time_for_every_30_sec + 20 <= int(time.time()):
                for machine in List_machines_depollution:
                    if machine.polu_capa < machine.polu_capa_max:
                        chng = D.to_remove_bro(Actual_map_pollution,machine.location,machine.range_depo,machine.polu_reduced_per_30_sec,machine.polu_capa_max - machine.polu_capa)
                        machine.polu_capa += chng
                time_for_every_30_sec = int(time.time()) + 30
                pollution_actuelle = numpy.sum(Actual_map_pollution)


            #AFFICHAGE INDICE POLLUTION
            if pollution_max_possible > 0:
                pourcentage_pollution = round(pollution_actuelle,4)
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
            pollution_value_text = pollution_value_font.render(f"{pourcentage_pollution:.1f}g totale.", 1, (255, 255, 255))
            value_rect = pollution_value_text.get_rect(center=(indice_x + indice_width/2, indice_y + 30))
            screen.blit(pollution_value_text, value_rect)


            # verification du mouvement du joueur
            has_not_moove = True
            vect_mvt = pygame.math.Vector2(0,0)
            if keys[touche_direction_gauche]:
                vect_mvt[0] -= Robot.speed * dt
            if keys[touche_direction_droite]:
                vect_mvt[0] += Robot.speed * dt
            if keys[touche_direction_haut]:
                vect_mvt[1] -= Robot.speed * dt
            if keys[touche_direction_bas]:
                vect_mvt[1] += Robot.speed * dt
            if vect_mvt.length() != 0:
                if vect_mvt.length() / (Robot.speed * dt + 0.00001) > 1:
                    vect_mvt = vect_mvt.normalize() * Robot.speed * dt
                has_not_moove = True 
                new_pos = Robot.pos + pygame.math.Vector2(vect_mvt[0],0)
                rect_robot = pygame.rect.Rect(new_pos[0]-Robot.image_length[0]/2,new_pos[1],64,52)
                if rect_robot.collidelist(List_batiments_zones_collision[0]) == -1: # verif sur laxe x
                    Robot.pos = new_pos

                new_pos = Robot.pos + pygame.math.Vector2(0,vect_mvt[1])
                rect_robot = pygame.rect.Rect(new_pos[0]-Robot.image_length[0]/2,new_pos[1],64,52)
                if rect_robot.collidelist(List_batiments_zones_collision[0]) == -1: # verif sur laxe y
                    Robot.pos = new_pos
            else:
                has_not_moove = False

                    
                
    
            Robot.moove_this_frame = has_not_moove
            Robot.pos = (round(Robot.pos[0],5),round(Robot.pos[1],5))
        
            last_mvt = [keys[touche_direction_haut],keys[touche_direction_bas],keys[touche_direction_gauche],keys[touche_direction_droite]]   # -----> pour faire les animations mais la jai pas le temps ptdr
            Robot.do_all(keys,screen,last_mvt)

            if fade_alpha > 0 : # permet de faire le fade si yen a a faire dans le current state
                fade_surface = pygame.Surface((screen.get_width(),screen.get_height()))
                fade_surface.set_alpha(fade_alpha)
                fade_surface.fill((0, 0, 0))  
                screen.blit(fade_surface, (0, 0))
            if see_minimap == True :
                draw_minimap(screen, Robot, Actual_map_objects_layer, Actual_map_pollution, tileset_paths, LEN_SQUARE, W, H)

        if IN_HOUSE:
            keys = pygame.key.get_pressed()
            coin_haut = (math.floor((Robot.pos_in_houses[0]-W_2)/LEN_SQUARE),math.floor((Robot.pos_in_houses[1]-H_2)/LEN_SQUARE))
            coin_bas = (math.ceil((Robot.pos_in_houses[0]+W_2)/LEN_SQUARE),math.ceil((Robot.pos_in_houses[1]+H_2)/LEN_SQUARE))

            for y in range(max(coin_haut[1],0),min(coin_bas[1],Map_House.shape[0])): # montre la map, polution et objet_layer
                for x in range(max(coin_haut[0],0),min(coin_bas[0],Map_House.shape[1])):
                    tileset[Map_House[x,y]].blit_self(screen,(x*LEN_SQUARE-Robot.pos_in_houses[0]+W_2, y*LEN_SQUARE-Robot.pos_in_houses[1]+H_2))


            ### Mouvement
            has_not_moove = True
            vect_mvt = pygame.math.Vector2(0,0)
            if keys[touche_direction_gauche]:
                vect_mvt[0] -= Robot.speed * dt
            if keys[touche_direction_droite]:
                vect_mvt[0] += Robot.speed * dt
            if keys[touche_direction_haut]:
                vect_mvt[1] -= Robot.speed * dt
            if keys[touche_direction_bas]:
                vect_mvt[1] += Robot.speed * dt
            if vect_mvt.length() != 0:
                if vect_mvt.length() / (Robot.speed * dt + 0.00001) > 1:
                    vect_mvt = vect_mvt.normalize() * Robot.speed * dt
                has_not_moove = True 
                new_pos = Robot.pos_in_houses + pygame.math.Vector2(vect_mvt[0],0)
                rect_robot = pygame.rect.Rect(new_pos[0]-Robot.image_length[0]/2,new_pos[1],64,52)
                if rect_robot.collidelist(List_batiments_zones_collision[1  ]) == -1: # verif sur laxe x
                    Robot.pos_in_houses = new_pos

                new_pos = Robot.pos_in_houses + pygame.math.Vector2(0,vect_mvt[1])
                rect_robot = pygame.rect.Rect(new_pos[0]-Robot.image_length[0]/2,new_pos[1],64,52)
                if rect_robot.collidelist(List_batiments_zones_collision[1]) == -1: # verif sur laxe y
                    Robot.pos_in_houses = new_pos
            else:
                has_not_moove = False

            Robot.moove_this_frame = has_not_moove
            last_mvt = [keys[touche_direction_haut],keys[touche_direction_bas],keys[touche_direction_gauche],keys[touche_direction_droite]]  
            Robot.do_all(keys,screen,last_mvt)
            # fin mvt


            if keys[touche_utiliser_porte] and not cd_porte:
                IN_HOUSE = False
                Robot.last_direction = 2
                Robot.pos = (List_sorti_hors_maison[indice_maison][0]*64 -64,List_sorti_hors_maison[indice_maison][1]*64)
                cd_porte = True
            if not keys[touche_utiliser_porte]:
                cd_porte = False
            
            print(indice_maison)

        if keys[touche_affichage_inventaire] and not cd_inv:
            cd_inv = True
            IN_INV = not IN_INV
        if not keys[touche_affichage_inventaire]:
            cd_inv = False

        if IN_INV:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            clique = False
            changed = False
            collision = False
            actual_slot = -1
            if mouse_click[0] == False:
                clique = True
            else:
                pass
            screen.blit(inventaire_surface,pos_image_inventaire)

            for i in range(Robot.inventory_size):
                if List_collision_slots[i].collidepoint(mouse_pos):
                    collision = True
                    if picked_slot == -1 and clique:
                        picked_slot = i
                        changed = True
                    else:
                        changed = False
                    if not clique:                   
                        if picked_slot != -1:
                            pass

                obj = Robot.inventory[i]
                if obj != None:
                    new_img = pygame.transform.scale(obj.image,(48,48))
                    screen.blit(new_img,(pos_image_inventaire[0] + first_slot_pos[0]+(decallage+longueur_slot)*(i%5), pos_image_inventaire[1] + first_slot_pos[1]+(decallage+longueur_slot)*(i//5)))
            if not collision:
                if not clique:
                    picked_slot = -1
                
            print(picked_slot,actual_slot)
            #first_slot_pos[0]+(decallage+longueur_slot)*(n%5),first_slot_pos[1]+(decallage+longueur_slot)*(n//5)

        current_time = pygame.time.get_ticks()
        if machine_dialogue_active:
            for object in objects:
                object.process()
                object.draw(screen)

            previous_counter = counter 
            if counter < speed * len(message):
                counter += 1
            else:
                done = True
                text_sound.stop()

            current_char = counter // speed
            previous_char = previous_counter // speed

            if current_char == 1 and previous_char == 0 and not done:
                text_sound.play()

            dialogue_1.snip = message[0:counter//speed]

            current_time = pygame.time.get_ticks()
            if (keys[pygame.K_RETURN] or keys[pygame.K_SPACE]) and current_time - machine_dialogue_cooldown > machine_dialogue_cooldown_delay:
                machine_dialogue_cooldown = current_time
                if done:
                    if active_message < len(dialogue_1.dialogue_text) - 1:
                        active_message += 1
                        done = False
                        message = dialogue_1.dialogue_text[active_message]
                        counter = 0
                        text_sound.stop()
                    else:
                        machine_dialogue_active = False
                        text_sound.stop()
                else:
                    counter = speed * len(message)
                    done = True
                    text_sound.stop()

        # if machine_dialogue_active:
        #     if (keys[pygame.K_SPACE] or keys[pygame.K_RETURN]) and current_time - machine_dialogue_cooldown > machine_dialogue_cooldown_delay:
        #         machine_dialogue_cooldown = current_time

             
        #         active_message += 1
        #     for object in objects:
        #         object.process()
        #         object.draw(screen)

        #     previous_counter = counter 
        #     if counter < speed * len(message):
        #         counter +=1
        #     else:
        #         done = True
        #         text_sound.stop()

        #     current_char = counter // speed
        #     previous_char = previous_counter // speed

        #     if current_char == 1 and previous_char == 0 and not done:
        #         text_sound.play()

        #     dialogue_1.snip = message[0:counter//speed]

        #     if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
        #         if done:
        #             if active_message < len(dialogue_1.dialogue_text) - 1:
        #                 active_message += 1
        #                 done = False
        #                 message = dialogue_1.dialogue_text[active_message]
        #                 counter = 0
        #             else:
        #                 machine_dialogue_active = False
        #         else:
        #             counter = speed * len(message)
        #             done = True
    if fade_alpha > 0 and current_state not in (FADE_TO_END_4, FADE_TO_END_5, FADE_TO_END_6, SHOW_EARTH_END):
        fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill((0, 0, 0))
        screen.blit(fade_surface, (0, 0))
    pygame.display.flip()
    dt = clock.tick(fps) / 1000


save_dir = os.path.join(main_dir, "saves")
os.makedirs(save_dir, exist_ok=True)

current_save = sys.argv[7] if len(sys.argv) > 7 else None

if current_save:
    save_name = current_save  
else:
    save_index = 1
    while os.path.exists(os.path.join(save_dir, f"save_{save_index}_map.txt")):
        save_index += 1
    save_name = f"save_{save_index}"





numpy.savetxt(os.path.join(save_dir, f"{save_name}_map.txt"), Actual_map, fmt="%d")
numpy.savetxt(os.path.join(save_dir, f"{save_name}_objects.txt"), Actual_map_objects_layer, fmt="%d")
numpy.savetxt(os.path.join(save_dir, f"{save_name}_pollution.txt"), Actual_map_pollution, fmt="%.4f")


with open(os.path.join(save_dir, f"{save_name}_bushes.json"), "w") as f:
    json.dump(Liste_bush_on_map, f)

machines_data = []
for m in List_machines_depollution:
    machines_data.append({
        "location": [int(m.location[0]), int(m.location[1])],  # garder l'ordre que tu utilises partout
        "polu_reduced_per_30_sec": m.polu_reduced_per_30_sec,
        "range_depo": m.range_depo,
        "polu_capa": m.polu_capa,
        "polu_capa_max": m.polu_capa_max,
        "image_path": m.image_path if hasattr(m, "image_path") else "Depollution_machine_t_1.png"
    })


for machine, m in zip(List_machines_depollution, machines_data):
    machine.polu_capa = m["polu_capa"]
with open(os.path.join(save_dir, f"{save_name}_machines.json"), "w") as f:
    json.dump(machines_data, f)

inventory_data = []
for item in Robot.hotbar:
    if item is None:
        inventory_data.append(None)
    else:
        if isinstance(item, CO.Plant):
            inventory_data.append({"type":"Plant", "id":"Bush_tile.png"})
        elif isinstance(item, CO.Machine_objet):
            inventory_data.append({"type":"Machine_objet", "id":"Depollution_machine_t_1.png"})
        elif isinstance(item, CO.Consumable):
            inventory_data.append({"type":"Consumable", "id":"apple.png", "count":1})
        elif item["type"] == "Consumable" and item.get("id") == "ferraille_v1.png":
            Robot.hotbar.append(ferraille)
        else:
            inventory_data.append({"type":"Unknown"})
with open(os.path.join(save_dir, f"{save_name}_inventory.json"), "w") as f:
    json.dump(inventory_data, f)
    
print(f"Partie sauvegardée : {save_name}")

pygame.quit()