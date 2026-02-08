import pygame
import os

# Chemins
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
police_dir = os.path.join(assets_dir,"polices")
sounds_dir = os.path.join(assets_dir, "sounds")

# Chargement des assets
dialogue_image = pygame.image.load(os.path.join(assets_dir, "dialogue_box.png"))
police_dialogue_path = os.path.join(police_dir, "police_dialogue.ttf")

objets = []

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
        objets.append(self)
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