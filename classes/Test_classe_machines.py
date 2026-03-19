import pygame
import os

pygame.display.init()
pygame.font.init()
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(main_dir,"assets")

class MACHINE():
    def __init__(self,location):
        self.location = location

class Depollution(MACHINE):
    def __init__(self, location,polu_reduced_per_30_sec,range_depo,tier,polu_capa_max):
        super().__init__(location)
        self.polu_reduced_per_30_sec = polu_reduced_per_30_sec
        self.range_depo = range_depo
        self.tier = tier
        self.polu_capa = 0
        self.polu_capa_max = polu_capa_max