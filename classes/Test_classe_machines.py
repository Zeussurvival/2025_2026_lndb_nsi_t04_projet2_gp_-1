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
    def __init__(self, location,percent_reduced,range_depo,tier):
        super().__init__(location)
        self.percentage_reduced = percent_reduced
        self.range_depo = range_depo
        self.tier = tier