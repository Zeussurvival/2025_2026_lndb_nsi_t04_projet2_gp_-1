# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os 
import classe_dialogue as C_D


# Chemins
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")


font_1 = os.path.join(police_dir, "test_1.ttf")
font_2 = os.path.join(police_dir, "test_2.ttf")


# pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

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

earth_timer = 180
fade_alpha = 255 
fade_speed = 1
timer = 70
text_timer = 120


# Variables dialogue

counter = 0
speed = 4
done = False
active_message = 0


# Chargement des assets

dialogue_sounds_path = os.path.join(sounds_dir, "typewriter.mp3")
text_sound = pygame.mixer.Sound(dialogue_sounds_path)
text_sound.set_volume(0.5)


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)






objects = C_D.objects
counter = 0
speed = 4
done = False
active_message = 0
current_frame = 0
animation_speed = 0.3

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
text_1 = font.render("Cela fait 732 années que les humains ont quitté cette planète", 1, (255, 255, 255))
text_2 = font.render("Ils ont laissé derrière eux… ceci.", 1, (255, 255, 255))
text_rect_1 = text_1.get_rect(center=(640, 360))
text_rect_2 = text_2.get_rect(center=(640, 100))

dialogue_1 = C_D.Dialogue( 640,600, 894, 200, ["Initialisation…", "Unité de nettoyage autonome : R-0.", "Statut de la planète : inhabitable.", "Mission prioritaire : nettoyer."], next)
message = dialogue_1.dialogue_text[active_message]


frames = []
for i in range(30):

    img = pygame.image.load(f"assets/earth/sprite_{i:02d}.png")
    img = pygame.transform.scale(img,(256,256))
    frames.append(img)

while running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == (pygame.K_SPACE or pygame.K_RETURN):
                if current_state == SHOW_DIALOGUE :
                    if done :
                        if active_message < len(dialogue_1.dialogue_text) - 1:   # if len(active_message) <= 75
                            active_message += 1
                            done = False
                            message = dialogue_1.dialogue_text[active_message]
                            counter = 0
                            text_sound.stop()
                        else :  
                            current_state = GAME_PLAY                                                 #elif len(active_message)> 75
                            text_sound.stop()                        
                    else:
                        counter = speed * len(message)
                        done = True
                        text_sound.stop() 
    # fill the screen with a color to wipe away anything from last frame
    screen.fill((0,0,0))


       
    if current_state == FADE_BLACK:
        if timer > 0 :
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
            text_timer = 120
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
        screen.fill ((0,0,0))
        current_frame += animation_speed
        if current_frame >= len(frames):
            current_frame = 0
        earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
        screen.blit(frames[int(current_frame)], earth_rect) 
        screen.blit(text_2, text_rect_2) 
        fade_alpha -= fade_speed 
        if fade_alpha <= 0:
            fade_alpha = 0
            current_state = SHOW_EARTH
            earth_timer = 180
            print("terre visible")
    elif current_state == SHOW_EARTH:
        current_frame += animation_speed
        if current_frame >= len(frames):
            current_frame = 0
        earth_rect = frames[int(current_frame)].get_rect(center=(640, 360))
        screen.blit(frames[int(current_frame)], earth_rect) 
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
        screen.blit(text_2, text_rect_2)  
        fade_alpha += fade_speed
        if fade_alpha >= 255 :
            fade_alpha = 255
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

        if current_char == 1 and previous_char == 0 and not done :
            text_sound.play()
        
        dialogue_1.snip = message[0:counter//speed]
        
    elif current_state == GAME_PLAY :
        screen.fill("purple")
        pygame.draw.circle(screen, "red", player_pos, 40)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_q]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt
    if fade_alpha > 0:
        fade_surface = pygame.Surface((1280, 720))
        fade_surface.set_alpha(fade_alpha)
        fade_surface.fill((0, 0, 0))  
        screen.blit(fade_surface, (0, 0))

  

            


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()