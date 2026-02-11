import pygame
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
    except:
        return False
    
# https://www.youtube.com/watch?v=uWvb3QzA48c&list=PLsk-HSGFjnaG-BwZkuAOcVwWldfCLu1pq

pygame.display.init()
pygame.font.init()

W,H = (1280, 720)
W_2,H_2 = W/2,H/2
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
LEN_SQUARE = 64
dt = 0
Taille_map = 100
Actual_map = D.creation_map_rectangle(Taille_map,Taille_map,0)
Actual_map_pollution = D.set_pollution_map_rectangle(Taille_map,Taille_map,Actual_map,5)
Actual_map_objects_layer = D.creation_map_rectangle(Taille_map,Taille_map,-1)

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
can_see_pollution = False
cd_see_pollution = False


hotbar = [bush,None,None,None,None]
Robot = CH.Humanoid((15*LEN_SQUARE,15*LEN_SQUARE),100,5,5,"robot_front_wait.png",["robot_front_walking.png"],LEN_SQUARE,hotbar)
print("running now")
running = True
while running:
    time_0 = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

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

    if keys[pygame.K_F3]:              
        if cd_see_pollution == False:
            can_see_pollution = not can_see_pollution
            cd_see_pollution = True
    else:
        cd_see_pollution = False

    if keys[pygame.K_e]: #recuperer objets
        for obj in List_ground_objets:
            if (Robot.pos[0] - obj[1][0])**2 +(Robot.pos[1] - obj[1][1])**2 <= (LEN_SQUARE*Robot.range_pickup)**2 and can_pickup:
                can_pickup = False
                if Robot.pickup(obj[0]):
                    List_ground_objets.remove(obj)
    else:
        can_pickup = True               

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
    pygame.display.flip()
    if time.time()-time_0 > dt:
        print(" OH SHIT", time.time()-time_0- dt)
    # print(time.time()-time_0- dt)
    dt = clock.tick(120) / 1000

pygame.quit()