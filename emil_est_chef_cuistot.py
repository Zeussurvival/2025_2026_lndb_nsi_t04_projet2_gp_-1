from PIL import Image
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

image = Image.open("assets/TopDownApocalipticExteriorTileset/TileSheet.png")
print("Taille de l'image:", image.size)
print("Mode de couleur:", image.mode)
print("Format de l'image:", image.format)

for i in range (5):
    zone = (0+8*i, 0, 8+8*i, 8)
    image_coupee = image.crop(zone)
    text = "Temp/"+str(i)+"_image.png"
    image_coupee.save((text))









