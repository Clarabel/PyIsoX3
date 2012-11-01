from pygame import image
import os

def load(img):
    file = os.path.join('images', img)
    surf = image.load(file)
    surf = surf.convert()
    return surf


def load_tileset(img, alpha=True):
    file = os.path.join('images', 'tilesets', img)
    surf = image.load(file)
    colorkey = surf.get_at((0,0))
    surf.set_colorkey(colorkey)
    if alpha:
        surf = surf.convert_alpha()
    return surf

import pygame
#pygame.display.set_mode((800, 600))
tileset = None


cached_tiles = {}
def load_tile(ref, h):
    if not tileset:
        global tileset, masks
        tileset_file = os.path.join('images', 'tilesets', 'tileset.png')
        tileset = image.load(tileset_file)
        tileset = tileset.convert_alpha()

        mask0 = load_tileset('mask0.bmp')
        mask1 = load_tileset('mask1.bmp')
        masks = [mask0, mask1]
    result = cached_tiles.get((ref, h), False)
    if not result:
        x, y = ref%8, ref//8
        rect = pygame.Rect(64*x, 64*y, 64, 32+32*h)
        surf = tileset.subsurface(rect)
        result = masks[h].copy()
        result.blit(surf, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
        cached_tiles[(ref, h)] = result
    return result


test_value = 17
