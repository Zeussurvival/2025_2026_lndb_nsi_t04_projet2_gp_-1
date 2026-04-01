import pygame
import os

pygame.display.init()
pygame.font.init()
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
main_dir = os.path.split(os.path.abspath(main_dir))[0]
assets_dir = os.path.join(main_dir,"data") 
img_dir = os.path.join(assets_dir,"Tiles") 
# bg_image_dir = os.path.join(main_dir,"Tiles/Background_images")


#         self.image = pygame.image.load(os.path.join(img_dir, image)).convert_alpha()
#         self.image = pygame.transform.rotate(self.image,rotate)
#         self.image = pygame.transform.scale(self.image,(16,16))
#         if background_image != None:
#             self.background_image = pygame.image.load(os.path.join(bg_image_dir, background_image)).convert_alpha()
#         else:
#             self.background_image = None
class Tile:
    def __init__(self,image,list_images,rotate):
        if image != None:
            self.path = image
            self.image = pygame.image.load(os.path.join(img_dir, self.path)).convert_alpha()
            self.image = pygame.transform.rotate(self.image,rotate)
            self.image = pygame.transform.scale(self.image,(64,64))
        else:
            self.image = None #a supr qd plus de tile
        if rotate != None: #a supr qd plus de tile
            self.rotate = rotate #a supr qd plus de tile
        else: #a supr qd plus de tile 
            self.rotate = None #a supr qd plus de tile

        if list_images != None:
            self.images_to_add = list_images
            self.indice_list_images = 0
        else:
            self.images_to_add = None
        self.poid = 0

    def blit_self(self,screen,pos):
        if self.image != None:
            screen.blit(self.image,pos)