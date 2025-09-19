import pygame
from moneySmarts.screens.base_screens import Screen
from moneySmarts.tilemap import TileMap

class OverworldScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        # Example CSV and tileset path; replace with actual map and tileset
        self.tilemap = TileMap(
            map_csv="assets/images/buildings/exteriors/modernexteriors-win/Modern_Exteriors_16x16/Modern_Exteriors_Complete_Singles_16x16/map.csv",
            tileset_path="assets/images/buildings/exteriors/modernexteriors-win/Modern_Exteriors_16x16/Modern_Exteriors_Complete_Singles_16x16/ME_Singles_City_Props_16x16_Stop_Barrier_Up_Front.png",
            tile_size=16
        )
        self.camx = 0
        self.camy = 0

    def handle_event(self, event):
        # Add camera movement or other controls here
        pass

    def update(self):
        pass

    def draw(self, surface):
        self.tilemap.draw(surface, self.camx, self.camy)
