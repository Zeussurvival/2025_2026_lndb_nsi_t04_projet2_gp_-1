# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os


main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")


# pygame setup
pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
objects = []
timer = pygame.time.Clock()
counter = 0
speed = 4
done = False
active_message = 0


dialogue_image = pygame.image.load(os.path.join(assets_dir, "dialogue_box.png"))
police_dialogue_path = os.path.join(police_dir, "police_dialogue.ttf")
dialogue_sounds_path = os.path.join(sounds_dir, "typewriter.mp3")
text_sound = pygame.mixer.Sound(dialogue_sounds_path)
text_sound.set_volume(1)

dialogue_box_width = 400
dialogue_box_height = 200
dialogue_box_x = (screen.get_width() - dialogue_box_width) // 2
dialogue_box_y = (screen.get_height() - dialogue_box_height) // 2
dialogue_box = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Dialogue():
    def __init__(self, x, y, width, height, dialogue_text="hey", onlickFunction=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dialogue_text = dialogue_text
        self.snip = ""
        self.onclickFunction = onlickFunction
        self.one_press = one_press
        self.already_pressed = False

        self.dialogue_rect = pygame.Rect(0, 0, self.width, self.height)
        self.dialogue_rect.center = (x, y)

        self.normal_image = pygame.transform.scale(dialogue_image, (width, height))
        objects.append(self)

        self.font = pygame.font.Font(police_dialogue_path, 25)
        
    def draw(self, screen):
        screen.blit(self.normal_image, self.dialogue_rect)
        text_surface = self.font.render(self.snip, True, (137, 244, 255))
        text_rect = text_surface.get_rect(
            topleft=(self.dialogue_rect.left + 40, self.dialogue_rect.top + 40))
        screen.blit(text_surface, text_rect)

    def process(self):
        if pygame.mouse.get_pressed()[0]:
            if self.dialogue_rect.collidepoint(pygame.mouse.get_pos()):
                if self.one_press :
                    self.onclickFunction()
                elif not self.already_pressed:
                    self.onclickFunction()
                    self.already_pressed = True
                else :
                    self.already_pressed = True
        else :
            self.already_pressed = False


def open_dialogue_box ():
    global dialogue_box
    dialogue_box = True


def next():
    print("next")

dialogue_1 = Dialogue( 640,600, 894, 200, ["Initialisation…", "Unité de nettoyage autonome : R-0.", "Statut de la planète : inhabitable.", "Mission prioritaire : nettoyer."], next)
message = dialogue_1.dialogue_text[active_message]

# while running:
#     previous_counter = counter 
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     if counter < speed * len(message) :
#         counter +=1
#     elif counter >= speed * len(message):
#         done = True
#         text_sound.stop()
   

#     current_char = counter // speed
#     previous_char = previous_counter // speed

#     # if current_char > previous_char and current_char % 2 == 0 and not done:
#     #     text_sound.play()

#     if current_char == 1 and previous_char == 0 and not done:
#         text_sound.play()

#     # if current_char > previous_char and not done:
#     #     text_sound.play()
    
#     dialogue_1.snip = message[0:counter//speed]

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == (pygame.K_SPACE or pygame.K_RETURN):
#                 if done :
#                     if active_message < len(dialogue_1.dialogue_text) - 1:
#                         active_message += 1
#                         done = False
#                         message = dialogue_1.dialogue_text[active_message]
#                         counter = 0
#                         text_sound.stop()
#                     else :
#                         dialogue_box = False
#                         text_sound.stop()                        
#                 else:
#                     counter = speed * len(message)
#                     done = True
#                     text_sound.stop() 

#     screen.fill("purple")

#     pygame.draw.circle(screen, "red", player_pos, 40)

#     if dialogue_box == False :
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_z]:
#             player_pos.y -= 300 * dt
#         if keys[pygame.K_s]:
#             player_pos.y += 300 * dt
#         if keys[pygame.K_q]:
#             player_pos.x -= 300 * dt
#         if keys[pygame.K_d]:
#             player_pos.x += 300 * dt
    
#     if dialogue_box :
#         for object in objects:
#             object.process()
#             object.draw(screen)
        

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000


# pygame.quit()