import pygame
import os

pygame.display.init()
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
main_dir = os.path.split(os.path.abspath(main_dir))[0]
assets_dir = os.path.join(main_dir,"assets") 
img_dir = os.path.join(assets_dir,"Images") 
bg_image_dir = os.path.join(assets_dir,"Tiles/Background_images")
tiles_dir = os.path.join(assets_dir,"Tiles") 

class OBJET():
    def __init__(self,image_name,name,description,can_see):
        self.name = name
        self.description = description
        self.image = pygame.image.load(os.path.join(img_dir,image_name))
        self.image = pygame.transform.scale(self.image,(64,64))
        self.can_see = can_see
    

class Consumable(OBJET):
    def __init__(self, image_name, name, description):
        super().__init__(image_name, name, description,can_see=False)
        self.type = "consumable"

class Tool(OBJET):
    def __init__(self, image_name, name, description, damage, tier):
        super().__init__(image_name, name, description,can_see=True)
        self.type = "tool"
        self.damage = damage
        self.tier = tier

class Plant(OBJET):
    def __init__(self, image_name, name, description,image_tile,indice_in_map):
        super().__init__(image_name, name, description, can_see=True)
        self.type = "Plant"
        self.image_tile = image_tile
        self.indice_in_map = indice_in_map
    
class Machine_objet(OBJET):
    def __init__(self, image_name, name, description, tier, image_tile, indice_in_map):
        super().__init__(image_name, name, description, can_see=True)
        self.type = "Machine_objet"
        self.tier = tier
        self.image_tile = image_tile
        self.indice_in_map = indice_in_map