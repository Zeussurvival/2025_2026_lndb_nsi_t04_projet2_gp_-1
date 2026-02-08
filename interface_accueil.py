# Example file showing a circle moving on screen
import pygame # python3 -m pip install -U pygame --user
import os
import random
import webbrowser
import subprocess

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
hologram_dir = os.path.join(assets_dir,"1. Free Hologram Interface Wenrexa")
X3_dir = os.path.join(hologram_dir,"Card X3")
X2_dir = os.path.join(hologram_dir, "Card X2") 
button_1 = os.path.join(hologram_dir,"Button 1")
icons = os.path.join(hologram_dir,"Icons")
robot = os.path.join(assets_dir,"Robot")



# background_original = pygame.image.load(os.path.join(X3_dir,"Card X5.png")).convert_alpha()
# background_original = pygame.image.load(os.path.join(X3_dir,"Card X5.png")).convert_alpha()
# background = pygame.transform.scale(background_original,(screen.get_size()))


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
perso_image = pygame.image.load(os.path.join(robot, "robot_v1.png"))
title_image = pygame.image.load(os.path.join(assets_dir, "title.png"))

settings_panel = pygame.image.load(os.path.join(X2_dir,"Card X2.png"))
settings_panel_rect = settings_panel.get_rect()
settings_panel_rect.center = (400, 300)

music_panel = pygame.image.load(os.path.join(X2_dir,"Card X2.png"))
music_panel_rect = music_panel.get_rect()
music_panel_rect.center = (400,300)

font = pygame.font.Font(None, 36)
# font_title 


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
SEMI_TRANSPARENT = (0,0,0,180)


title_image_resize = pygame.transform.scale(title_image,(256, int(92.75)))
title_image_rect = title_image_resize.get_rect()
title_image_rect.center = (400, 150)

running = True
dt = 0
mouse_clicked_button = False
objects = []
show_settings = False
show_music = False

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

def go_settings():
    global show_settings
    show_settings = not show_settings
    print("settings ouverts/fermés")

def change_volume():
    print("changement volume")

def launch_game():
    pygame.quit()
    subprocess.run(["python", "main.py"])      
    print('Button Pressed')

def close_music():
    global show_music
    show_music = False
    for btn in settings_buttons:
        btn.alreadyPressed = True
    print ("music fermé")

def open_music():
    global show_music
    show_music = True
    print("music ouvert")

def mute():
    print ("muted")

def up():
    print("music up")

def down():
    print("music_down")

def redirect():
    webbrowser.open("https://discord.gg/EBkmmfwn")

def quit():
    global running
    running = False

def fonction ():
    print ("à faire")

Button(400, 450, 140, 50, 'Jouer', launch_game, icon=icon_play)
Button(70, 70, 50, 50, '', go_settings, icon=icon_settings, icon_only=True )
Button(730, 70, 50, 50, "", fonction, icon=icon_info, icon_only=True)
Button(730, 120, 50, 50, "", redirect, icon=icon_discord, icon_only=True)
Button(730, 170, 50, 50, "", fonction, icon=icon_dons, icon_only=True)
Button(120, 70, 50, 50, "", quit, icon=icon_quit, icon_only=True)

settings_buttons = [
    Settings_Button(400, 300, 50, 50, '', open_music, icon=icon_sound, icon_only=True),
    Settings_Button(250, 160, 50, 50, '', go_settings, icon=icon_close, icon_only=True)    
]

music_buttons = [
    Music_Button(300, 335, 50, 50, '', mute, icon=icon_mute, icon_only=True),
    Music_Button(400, 335, 50, 50, '', down, icon=icon_down, icon_only=True),
    Music_Button(500, 335, 50, 50, '', up, icon=icon_up, icon_only=True),
    Music_Button(250, 160, 50, 50, '', close_music, icon=icon_close, icon_only=True)
]

perso_image_scaled = pygame.transform.scale(perso_image, (128, 188))        
perso_image_rect = perso_image_scaled.get_rect ()
# perso_image_rect = perso_image.get_rect ()
perso_image_rect.center = (400, 300)

perso_speed_x = random.choice([-200, -150, 150, 200]) 
perso_speed_y = random.choice([-200, -150, 150, 200])



while running:
    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE :
                if show_music:
                    show_music = False
                elif show_settings:
                    show_settings = False

    # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")
    mouse_pos = pygame.mouse.get_pos()


    screen.blit(background,(0,0))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pass

    

    perso_image_rect.x += perso_speed_x * dt
    perso_image_rect.y += perso_speed_y * dt


    if perso_image_rect.left <= 0 or perso_image_rect.right >= 800:
        perso_speed_x = -perso_speed_x

    if perso_image_rect.top <= 0 or perso_image_rect.bottom >= 600:
        perso_speed_y = -perso_speed_y

    screen.blit(perso_image_scaled, perso_image_rect)
    # screen.blit(perso_image, perso_image_rect)
    screen.blit(title_image_resize, title_image_rect)

    for object in objects:
        object.process()


    if show_settings and not show_music:
        # Créer un overlay semi-transparent
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill(SEMI_TRANSPARENT)
        screen.blit(overlay, (0, 0))
        
        # Dessiner le panneau de réglages
        # settings_panel = pygame.Rect(200, 150, 400, 300)
        # pygame.draw.rect(screen, (20, 20, 40), settings_panel)
        # pygame.draw.rect(screen, WHITE, settings_panel, 3)  # Bordure
        screen.blit(settings_panel, settings_panel_rect)
        settings_title = font.render("Réglages", True, WHITE)
        settings_title_rect = settings_title.get_rect(center=(400, 200))
        screen.blit(settings_title, settings_title_rect)
        

        for btn in settings_buttons:
            btn.process()
    
    elif show_music :
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill(SEMI_TRANSPARENT)
        screen.blit(overlay, (0, 0))
        
        screen.blit(music_panel, music_panel_rect)
        music_title = font.render("Sons", True, WHITE)
        music_title_rect = music_title.get_rect(center=(400, 200))
        screen.blit(music_title, music_title_rect)
        

        for btn in music_buttons:
            btn.process()
    
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()