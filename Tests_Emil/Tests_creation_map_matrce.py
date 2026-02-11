import numpy as np
import pygame
import sys
import winreg
import random

import Test_def as D

def audio_device_available():
    # Retourne True si Windows a AU MOINS un périphérique audio fonctionnel.
    # On lit le registre Windows : s'il n'y a aucun endpoint audio actif,
    # pygame.mixer ne doit PAS être initialisé.
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render")
        pygame.mixer.init()
    except:
        return False

print(sys.executable)
pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

x_map = 50
y_map = 30
seed = 25
pollution_origins = 70
range_pollution = 5


# print(create_random_pos(seed,4,(x_map,y_map)))
# print(map123[-2::5,...])



map123 = D.creation_map_rectangle(x_map,y_map,0)
map123_pollution = D.set_pollution_map_rectangle(pollution_origins,seed,map123,range_pollution) # number_of_origins,seed,map,range_pollu

map123_pollution = D.floor_pollution_map_at_smth(map123_pollution,2)





house_matrice = np.array([[3,4,5,6],
                         [7,8,9,18],
                         [17,16,15,14],])


map123 = D.place_matrice_big_then_small(map123,house_matrice,(13,10))

# print(map123)
# print(map123_pollution)

# x = np.arange(36).reshape(6, 6)
# print(x[4::-2,...])

# for a in range(len(x)):
#     for y in range(len(x[a])):
#             print(x[a,y],(a,y))



Starting_pos = (0,0)
Len_square = 16

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,130,150))  # (100,200,100)

    for y in range(map123.shape[1]):
        for x in range(map123.shape[0]):
            pygame.draw.rect(screen,(100,(min(map123_pollution[x,y] *75+20,255)),100,0.1),(Len_square*x,Len_square*y,Len_square,Len_square))



    pygame.display.flip()
    dt = clock.tick(60) / 1000


pygame.quit()