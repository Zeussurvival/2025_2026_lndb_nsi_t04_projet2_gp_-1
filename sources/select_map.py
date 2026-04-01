# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os
import random
import webbrowser
import subprocess
import sys

pygame.font.init()
pygame.display.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

main_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.split(os.path.abspath(main_dir))[0]
source_dir = os.path.join(main_dir,"source")
assets_dir = os.path.join(main_dir,"data")
hologram_dir = os.path.join(assets_dir,"hologram")
X3_dir = os.path.join(hologram_dir,"Card X3")
X2_dir = os.path.join(hologram_dir, "Card X2") 
button_1 = os.path.join(hologram_dir,"Button 1")
icons = os.path.join(hologram_dir,"Icons")
robot = os.path.join(assets_dir,"Robot")
saves_dir = os.path.join(main_dir, "saves")

Taille_map = int(sys.argv[1]) if len(sys.argv) > 1 else 200
pt_pollution = int(sys.argv[2]) if len(sys.argv) > 2 else 140


background_original = pygame.image.load(os.path.join(X3_dir,"Card X5.png")).convert_alpha()
time_to_quit = False

screen_width, screen_height = screen.get_size()
img_width, img_height = background_original.get_size()


scale_x = screen_width / img_width
scale_y = screen_height / img_height
scale = max(scale_x, scale_y)  

new_width = int(img_width * scale)
new_height = int(img_height * scale)

background_scaled = pygame.transform.scale(background_original, (new_width, new_height))

background = pygame.Surface((screen_width, screen_height))
x_offset = (new_width - screen_width) // 2
y_offset = (new_height - screen_height) // 2

background.blit(background_scaled, (-x_offset, -y_offset))

# pygame setup

button_size = (300, 100)
button_image = pygame.image.load(os.path.join(button_1,"Button Normal.png"))
button_hover = pygame.image.load(os.path.join(button_1,"Button Hover.png"))
button_click = pygame.image.load(os.path.join(button_1,"Button Active.png"))
icon_play = pygame.image.load(os.path.join(icons, "play.png"))
icon_settings = pygame.image.load(os.path.join(icons,"settings.png"))
icon_dons = pygame.image.load(os.path.join(icons, "dons.png"))
icon_discord = pygame.image.load(os.path.join(icons, "discord.png"))
icon_info = pygame.image.load(os.path.join(icons, "info.png"))
icon_down = pygame.image.load(os.path.join(icons, "down.png"))
icon_music = pygame.image.load(os.path.join(icons, "music.png"))
icon_quit = pygame.image.load(os.path.join(icons, "quit.png"))
icon_sound = pygame.image.load(os.path.join(icons, "sound.png"))
icon_up = pygame.image.load(os.path.join(icons, "up.png"))
icon_close = pygame.image.load(os.path.join(icons, "close.png"))
icon_mute = pygame.image.load(os.path.join(icons, "mute.png"))

title_image = pygame.image.load(os.path.join(assets_dir, "title.png"))

font = pygame.font.Font(None, 33)

font_difficult = pygame.font.Font(None, 23)
font_text = pygame.font.Font(None, 30)
font_map = pygame.font.Font(None, 3)

settings_panel = pygame.image.load(os.path.join(X2_dir,"Card X2.png"))
settings_panel_rect = settings_panel.get_rect()
settings_panel_rect.center = (400, 300)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
SEMI_TRANSPARENT = (0,0,0,180)

scroll_offset = 0
MAX_VISIBLE_SAVES = 5
selected_file = None
mode = "new"

title_image_resize = pygame.transform.scale(title_image,(256, int(92.75)))
title_image_rect = title_image_resize.get_rect()
title_image_rect.center = (400, 150)

running = True
dt = 0
mouse_clicked_button = False
objects = []
show_fichier = False


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, icon=None, icon_only=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.icon = icon
        self.icon_only = icon_only
    
        if not icon_only:
            self.normal_image = pygame.transform.scale(button_image, (width, height))
            self.hover_image = pygame.transform.scale(button_hover, (width, height))
            self.pressed_image = pygame.transform.scale(button_click, (width, height))

        self.buttonRect = pygame.Rect(0, 0, self.width, self.height)
        self.buttonRect.center = (x, y)
        
        self.buttonSurf = font.render(buttonText, True, WHITE)
        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mousePos):
            if not self.icon_only :
                screen.blit(self.pressed_image, self.buttonRect)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.icon_only :
                    screen.blit(self.pressed_image, self.buttonRect)
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                if not self.icon_only :
                    screen.blit(self.hover_image, self.buttonRect)
                self.alreadyPressed = False

        else:
            if not self.icon_only:
                screen.blit(self.normal_image, self.buttonRect)
            self.alreadyPressed = False 

        if self.icon :
            if self.icon_only:
                icon_rect = self.icon.get_rect(center=self.buttonRect.center)
                screen.blit(self.icon, icon_rect)
            else :    
                icon_rect = self.icon.get_rect()
                total_width = self.buttonSurf.get_width() + 15 + icon_rect.width       
            
                text_rect = self.buttonSurf.get_rect()
                text_rect.center = (self.buttonRect.centerx - total_width // 2 + self.buttonSurf.get_width() // 2, self.buttonRect.centery)
                
                icon_rect.midleft = (text_rect.right + 15, self.buttonRect.centery)


                screen.blit(self.buttonSurf, text_rect)
                screen.blit(self.icon, icon_rect)

        else:
            text_rect = self.buttonSurf.get_rect(center=self.buttonRect.center)
            screen.blit(self.buttonSurf, text_rect) 

class Settings_Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, icon=None, icon_only=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.icon = icon
        self.icon_only = icon_only
    
        if not icon_only:
            self.normal_image = pygame.transform.scale(button_image, (width, height))
            self.hover_image = pygame.transform.scale(button_hover, (width, height))
            self.pressed_image = pygame.transform.scale(button_click, (width, height))

        self.buttonRect = pygame.Rect(0, 0, self.width, self.height)
        self.buttonRect.center = (x, y)
        
        self.buttonSurf = font_difficult.render(buttonText, True, WHITE)
    def process(self):
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mousePos):
            if not self.icon_only :
                screen.blit(self.pressed_image, self.buttonRect)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.icon_only :
                    screen.blit(self.pressed_image, self.buttonRect)
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                if not self.icon_only :
                    screen.blit(self.hover_image, self.buttonRect)
                self.alreadyPressed = False

        else:
            if not self.icon_only:
                screen.blit(self.normal_image, self.buttonRect)
            self.alreadyPressed = False 

        if self.icon :
            if self.icon_only:
                icon_rect = self.icon.get_rect(center=self.buttonRect.center)
                screen.blit(self.icon, icon_rect)
            else :    
                icon_rect = self.icon.get_rect()
                total_width = self.buttonSurf.get_width() + 15 + icon_rect.width       
            
                text_rect = self.buttonSurf.get_rect()
                text_rect.center = (self.buttonRect.centerx - total_width // 2 + self.buttonSurf.get_width() // 2, self.buttonRect.centery)
                
                icon_rect.midleft = (text_rect.right + 15, self.buttonRect.centery)


                screen.blit(self.buttonSurf, text_rect)
                screen.blit(self.icon, icon_rect)

        else:
            text_rect = self.buttonSurf.get_rect(center=self.buttonRect.center)
            screen.blit(self.buttonSurf, text_rect) 

class Music_Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, icon=None, icon_only=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.icon = icon
        self.icon_only = icon_only
    
        if not icon_only:
            self.normal_image = pygame.transform.scale(button_image, (width, height))
            self.hover_image = pygame.transform.scale(button_hover, (width, height))
            self.pressed_image = pygame.transform.scale(button_click, (width, height))

        self.buttonRect = pygame.Rect(0, 0, self.width, self.height)
        self.buttonRect.center = (x, y)
        
        self.buttonSurf = font.render(buttonText, True, WHITE)
    def process(self):
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mousePos):
            if not self.icon_only :
                screen.blit(self.pressed_image, self.buttonRect)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if not self.icon_only :
                    screen.blit(self.pressed_image, self.buttonRect)
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                if not self.icon_only :
                    screen.blit(self.hover_image, self.buttonRect)
                self.alreadyPressed = False

        else:
            if not self.icon_only:
                screen.blit(self.normal_image, self.buttonRect)
            self.alreadyPressed = False 

        if self.icon :
            if self.icon_only:
                icon_rect = self.icon.get_rect(center=self.buttonRect.center)
                screen.blit(self.icon, icon_rect)
            else :    
                icon_rect = self.icon.get_rect()
                total_width = self.buttonSurf.get_width() + 15 + icon_rect.width       
            
                text_rect = self.buttonSurf.get_rect()
                text_rect.center = (self.buttonRect.centerx - total_width // 2 + self.buttonSurf.get_width() // 2, self.buttonRect.centery)
                
                icon_rect.midleft = (text_rect.right + 15, self.buttonRect.centery)


                screen.blit(self.buttonSurf, text_rect)
                screen.blit(self.icon, icon_rect)

        else:
            text_rect = self.buttonSurf.get_rect(center=self.buttonRect.center)
            screen.blit(self.buttonSurf, text_rect) 

class Slider:
    def __init__(self, x, y, width, min_val=0, max_val=100, initial_val=50):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False

        self.track_rect = pygame.Rect(x, y, width, 6)
        self.handle_radius = 12
        self.handle_x = x + int((initial_val - min_val) / (max_val - min_val) * width)

    def process(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        handle_rect = pygame.Rect(
            self.handle_x - self.handle_radius,
            self.y - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if handle_rect.collidepoint(mouse_pos):
                    self.dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        if self.dragging and mouse_pressed:
            self.handle_x = max(self.x, min(self.x + self.width, mouse_pos[0]))
            self.value = int(self.min_val + (self.handle_x - self.x) / self.width * (self.max_val - self.min_val))

        # Dessin
        pygame.draw.rect(screen, (7, 51, 51), self.track_rect, border_radius=3)
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x, self.y, self.handle_x - self.x, 6), border_radius=3)
        pygame.draw.circle(screen, WHITE, (self.handle_x, self.y + 3), self.handle_radius)

def launch_game():
    pygame.quit()
    main_path = os.path.join(source_dir, "jeu.py")
    if mode == "load":
        if selected_file and os.path.exists(selected_file):
            save_base = os.path.basename(selected_file).replace("_map.txt", "")
            objects_file = os.path.join(saves_dir, f"{save_base}_objects.txt")
            pollution_file = os.path.join(saves_dir, f"{save_base}_pollution.txt")
            subprocess.run(["python", main_path, str(Taille_map), str(pt_pollution), 
                          "load", selected_file, objects_file, pollution_file, save_base])
        else:
            print("aucun save sélectionné")
    else:
        subprocess.run(["python", main_path, str(Taille_map), str(pt_pollution), "new"])

def quit():
    global running
    running = False

def fonction ():
    print ("à faire")


def go_fichier():
    global show_fichier, mode, selected_save_index, scroll_offset
    show_fichier = not show_fichier
    if show_fichier:
        mode = "load"
        selected_save_index = 0
        scroll_offset = 0

def go_nouveau():
    global mode, selected_file
    mode = "new"
    selected_file = None
    print("nouvelle map")

def get_saves():
    saves = []
    if not os.path.exists(saves_dir):
        return saves
    i = 1
    while os.path.exists(os.path.join(saves_dir, f"save_{i}_map.txt")):
        saves.append(f"save_{i}")
        i += 1
    return saves
selected_save_index = 0

def select_save(index):
    global selected_file, selected_save_index
    selected_save_index = index
    selected_file = os.path.join(saves_dir, f"save_{index + 1}_map.txt")
    print(f"save sélectionné : save_{index + 1}")

Button(400, 450, 170, 50, 'Continuer', launch_game, icon=icon_play)
Button(50, 70, 50, 50, "", quit, icon=icon_quit, icon_only=True)
Button(300, 300, 100, 40, "fichier", go_fichier)
Button(500, 300, 120, 40, "nouveau", go_nouveau)
fichier_buttons= [
    Settings_Button(250, 160, 50, 50, '', go_fichier, icon=icon_close, icon_only=True),
]

while running:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                if show_fichier:
                    show_fichier = False
            if show_fichier:
                saves = get_saves()
                if event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - 1)
                if event.key == pygame.K_DOWN:
                    scroll_offset = min(max(0, len(saves) - MAX_VISIBLE_SAVES), scroll_offset + 1)
        if event.type == pygame.MOUSEWHEEL and show_fichier:
            saves = get_saves()
            scroll_offset -= event.y 
            scroll_offset = max(0, min(max(0, len(saves) - MAX_VISIBLE_SAVES), scroll_offset))
    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")
    mouse_pos = pygame.mouse.get_pos()


    screen.blit(background,(0,0))


    # screen.blit(perso_image, perso_image_rect)
    screen.blit(title_image_resize, title_image_rect)

    if show_fichier:
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill(SEMI_TRANSPARENT)
        screen.blit(overlay, (0, 0))
        screen.blit(settings_panel, settings_panel_rect)

        fichier_title = font.render("Choisir une map", True, WHITE)
        screen.blit(fichier_title, fichier_title.get_rect(center=(400, 200)))

        saves = get_saves()
        if not saves:
            no_save_text = font_text.render("Aucun save trouvé", True, WHITE)
            screen.blit(no_save_text, no_save_text.get_rect(center=(400, 310)))
        else:
            visible_saves = saves[scroll_offset:scroll_offset + MAX_VISIBLE_SAVES]
            for i, save_name in enumerate(visible_saves):
                real_index = i + scroll_offset
                y_pos = 260 + i * 45
                color = (0, 255, 200) if real_index == selected_save_index else WHITE
                save_surf = font_text.render(save_name, True, color)
                save_rect = save_surf.get_rect(center=(400, y_pos))
                screen.blit(save_surf, save_rect)

                if save_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, (0, 255, 200), save_rect.inflate(20, 8), 2)
                    if pygame.mouse.get_pressed()[0]:
                        select_save(real_index)

            

        for object in fichier_buttons:
            object.process()
    if not show_fichier:
        for object in objects:
            object.process()
  

         
    
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()