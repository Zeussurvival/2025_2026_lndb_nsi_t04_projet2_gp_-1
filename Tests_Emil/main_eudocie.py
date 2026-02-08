# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os 
import classe_dialogue as C_D
pygame.init()
pygame.font.init()
pygame.mixer.init()

###-------------------------------------------------------
### ------------- CODE EUDOCIE
###-------------------------------------------------------

# Chemins
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")
dialogue_sounds_path = os.path.join(sounds_dir, "typewriter.mp3")
text_sound = pygame.mixer.Sound(dialogue_sounds_path)
text_sound.set_volume(0.5)

# pygame setup
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
fps = 60

# Variables fade
FADE_BLACK = 0
FADE_TO_EARTH = 1  
SHOW_EARTH = 2      
FADE_TO_DIALOGUE = 3 
SHOW_DIALOGUE = 4   
GAME_PLAY = 5     
current_state = FADE_BLACK
earth_timer = 180
fade_alpha = 255 
fade_speed = 1
fade_active = True
timer = 70
fade2_active = False
earth_active = False
timer2= 180

# Variables dialogue
counter = 0
speed = 4
done = False
active_message = 0
dialogue_box = True
current_frame = 0
animation_speed = 0.3

# Chargement des assets  ### pour le dialogue
liste_dialoges = C_D.objets
dialogue_image = pygame.image.load(os.path.join(assets_dir, "dialogue_box.png"))
dialogue_box_width = 400
dialogue_box_height = 200
dialogue_box_x = (screen.get_width() - dialogue_box_width) // 2
dialogue_box_y = (screen.get_height() - dialogue_box_height) // 2
dialogue_box = True
dialogue_1 = C_D.Dialogue( 640,600, 894, 200, ["Initialisation…", "Unité de nettoyage autonome : R-0.", "Statut de la planète : inhabitable.", "Mission prioritaire : nettoyer."], next)
message = dialogue_1.dialogue_text[active_message]

# Frames pour planète
frames = []
for i in range(30):
    img = pygame.image.load(f"assets/earth/sprite_{i:02d}.png")
    img = pygame.transform.scale(img,(256,256))
    frames.append(img)


###-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------

###-------------------------------------------------------
### ------------- CODE EUDOCIE + START UN PEU EMIL
###-------------------------------------------------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
        if current_state == SHOW_DIALOGUE :
            if done :
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
            earth_timer = 180
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

    if current_state == FADE_TO_DIALOGUE :
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


###-------------------------------------------------------
### ------------- CODE EMIL
###-------------------------------------------------------
    elif current_state == GAME_PLAY :
        screen.fill((255,130,150))






###-------------------------------------------------------
### ------------- CODE EUDOCIE
###-------------------------------------------------------
    if fade_alpha > 0: # permet de faire le fade si yen a a faire dans le current state
        fade_surface = pygame.Surface((screen.get_width(),screen.get_height()))
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill((0, 0, 0))  
        screen.blit(fade_surface, (0, 0))
   
    pygame.display.flip()
    dt = clock.tick(fps) / 1000


pygame.quit()