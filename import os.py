import os
import numpy
import pygame
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# i = 5
# for file in os.listdir(os.path.join("assets","Tiles","Batiment")):
#     print(file,i)
#     i += 1
# zone = [64,32]
# zone = zone[0] % 8, zone[1] % 8
# print (zone)

# matrice = numpy.full((10,10), 1,dtype=numpy.float32)
# center = 5,5
# range_depo = 4
# to_remove = 0.1

# def to_remove_bro(center,range_depo,to_remove):
#     actuel = 0
#     nb_a_faire = 1
#     pos_actu = center
#     for i in range(range_depo):
#         if i == 0:
#             matrice[center[0],center[1]] -= to_remove
#         else:
#             pos_actu=center[0]-i,center[1]-i
#             for t in range(nb_a_faire+2*i):
#                 matrice[pos_actu[0],pos_actu[1]+t] -= to_remove
#                 matrice[pos_actu[0]+2*i,pos_actu[1]+t] -= to_remove
#                 actuel += 2*to_remove
#             pos_actu=center[0]-i+1,center[1]-i
#             for t in range(nb_a_faire+2*i-2):
#                 matrice[pos_actu[0]+t,pos_actu[1]] -= to_remove
#                 matrice[pos_actu[0]+t,pos_actu[1]+2*i] -= to_remove
#                 actuel += 2*to_remove
#     return round(actuel,10)


# print(to_remove_bro(center,range_depo,to_remove))
# print(matrice)

# IMAGEEE = pygame.image.load(os.path.join(main_dir,"trophee_nsi/assets/Tiles/Autres/pollution_texture.png"))
# rect1 = pygame.rect.Rect(50,50,40,40)
# offset1 = 5

# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((0,0,0))


#     img_surface = IMAGEEE.copy()
#     img2 = img_surface.copy()
#     img2.set_alpha(10)
#     img3 = img_surface.copy()
#     img3.set_alpha(200)
#     img_surface.set_alpha(15.8)
#     screen.blit(img_surface,(10,10))
#     screen.blit(img2,(50,10))
#     screen.blit(img3,(90,10))


#     mouse_pos = pygame.mouse.get_pos()
#     mouse_rect = pygame.rect.Rect(mouse_pos[0]-offset1,mouse_pos[1]-offset1,offset1*2,offset1*2)
#     if mouse_rect.colliderect(rect1):
#         print("AH, Nous avons une collision avec l'un des elements")
#     pygame.draw.rect(screen,"red",rect1,0)


#     pygame.display.flip()
#     dt = clock.tick(60) / 1000


# pygame.quit()

mat = numpy.full((5,5),-1)
print(mat)