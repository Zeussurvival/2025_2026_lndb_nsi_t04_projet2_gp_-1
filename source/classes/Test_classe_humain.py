import numpy
import pygame
import time
import math
import random
import os

pygame.display.init()
pygame.font.init()
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(main_dir,"assets") 
Robot_dir = os.path.join(assets_dir,"Robot") 


#         self.image = pygame.image.load(os.path.join(img_dir, image)).convert_alpha()
#         self.image = pygame.transform.rotate(self.image,rotate)
#         self.image = pygame.transform.scale(self.image,(16,16))
#         if background_image != None:
#             self.background_image = pygame.image.load(os.path.join(bg_image_dir, background_image)).convert_alpha()
#         else:
#             self.background_image = None
class Humanoid:
    def __init__(self,pos,pv,base_damage,speed,image,list_images,LEN_SQUARE, hotbar, inv):
        self.vect = pygame.math.Vector2(0,0)
        self.pos = pos
        self.pos_in_houses = (5*64,5*64)
        self.pv = pv
        self.speed = speed * LEN_SQUARE
        self.base_damage = base_damage
        self.image_length = (64,96)
        self.held_item_indice = 0
        self.hotbar = hotbar
        self.hotbar_len = 5
        self.inventory = inv
        self.inventory_size = 25
        self.range_pickup = 2.5


        self.last_direction = 2
        self.moove_this_frame = False

        self.image = pygame.image.load(os.path.join(Robot_dir, image)).convert_alpha()
        self.image = pygame.transform.scale(self.image,(64,96))

        self.True_list_images = []
        for liste in list_images:
            liste_temp = []
            for img in liste:
                image = pygame.image.load(os.path.join(Robot_dir, img)).convert_alpha()
                image = pygame.transform.scale(image,(64,96))
                liste_temp.append(image)
            self.True_list_images.append(liste_temp)
        self.indice_animation_en_cours = time.time()
        
    def blit_center_self(self,screen,mooves):
        H,W = pygame.Surface.get_height(screen),pygame.Surface.get_width(screen)
        indice_actu = int((time.time() - self.indice_animation_en_cours ) *6) % 4
        new_image = self.image
        
        if mooves[2] and self.moove_this_frame:
            new_image = self.True_list_images[3][indice_actu]
            self.last_direction = 3
        if mooves[3] and self.moove_this_frame:
            new_image = self.True_list_images[4][indice_actu]
            self.last_direction = 4
        if mooves[1] and self.moove_this_frame:
            new_image = self.True_list_images[2][indice_actu]
            self.last_direction = 2
        if mooves[0] and self.moove_this_frame:
            new_image = self.True_list_images[1][indice_actu]
            self.last_direction = 1
        if self.moove_this_frame == False:
            new_image = self.True_list_images[self.last_direction][2]

        if self.True_list_images == []:
            new_image = self.image
        screen.blit(new_image,(W/2-self.image_length[0]/2,H/2-self.image_length[1]/2))

    def pickup(self,obj):
        for i in range(len(self.hotbar)):
            if self.hotbar[i] == None:
                self.hotbar[i] = obj
                return True
        if None in self.inventory:
            i = self.inventory.index(None)
            if i >= -1:
                self.inventory[i] = obj
                return True
            return False

    def draw_hotbar(self,screen):
        lenght_square = 64
        width = 6
        true_lenght = lenght_square + 2*width
        offset = 15 
        y_offset = offset + 10
        number_shown = 5
        first_x = screen.get_size()[0]/2 - 2*(offset+true_lenght) - lenght_square/2
        y = screen.get_size()[1] -lenght_square - y_offset
        for i in range(0,number_shown):
            pygame.draw.rect(screen,(100,100,100),(first_x+(lenght_square+width+offset)*i,y,true_lenght,true_lenght),width)
            if self.hotbar[i] != None:
                screen.blit(pygame.transform.scale(self.hotbar[i].image,(lenght_square,lenght_square)),(first_x+width+(lenght_square+width+offset)*i,y+width))        
        pygame.draw.rect(screen,"white",(first_x+(lenght_square+width+offset)*self.held_item_indice  -2 ,y - 2,true_lenght + 4,true_lenght + 4 ),width+ 2)

    def change_held_item(self,keys):
        if keys[pygame.K_1]:
            self.held_item_indice = 0
            self.held_item = self.hotbar[0]
        if keys[pygame.K_2]:
            self.held_item_indice = 1
            self.held_item = self.hotbar[1]
        if keys[pygame.K_3]:
            self.held_item_indice = 2
            self.held_item = self.hotbar[2]
        if keys[pygame.K_4]:
            self.held_item_indice = 3
            self.held_item = self.hotbar[3]
        if keys[pygame.K_5]:
            self.held_item_indice = 4
            self.held_item = self.hotbar[4]



    def do_all(self,keys,screen,last_mvt):
        self.draw_hotbar(screen)
        self.change_held_item(keys)
        self.blit_center_self(screen,last_mvt)


