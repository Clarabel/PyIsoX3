from pygame import image
import os

import pygame


def load_image(path, img):
    file = os.path.join('images', path, img)
    try:
        surf = image.load(file)
    except:
        print("n'a pas pu charger l'image"+file)
        raise
    return surf

Tilesets = {}

def load_tileset(tileset):
    "load cached tileset or draw and cache a new one"
    surf = Tilesets.get(tileset, None)
    if not surf:
        surf = load_image('tilesets', tileset)
        colorkey = surf.get_at((0,0))
        surf.set_colorkey(colorkey, pygame.RLEACCEL)
        surf = surf.convert_alpha()
        Tilesets[tileset] = surf
    return surf

Characters = {}
def load_character(character):
    #not yet
    "load cached tileset or draw and cache a new one"
    surf = Characters.get(character, None)
    if not surf:
        surf = load_image('Characters', character)
        colorkey = surf.get_at((0,0))
        surf.set_colorkey(colorkey, pygame.RLEACCEL)
        surf = surf.convert_alpha()
        Characters[character] = surf
    return surf

def load_cursor(filename, h=1, colorkey=-1):
    curs = load_image('cursor', filename)
    if colorkey == -1:
        colorkey = curs.get_at((0,0))
    curs.set_alpha(155)
    surf = load_mask(h)
    surf.blit(curs, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    surf.set_colorkey(colorkey, pygame.RLEACCEL)
    #surf.set_alpha(155)
    return surf#.convert_alpha()


Cached_tiles = {}

def load_tile(tileset, ref, h):
    "load cached tile or draw and cache a new one"
    tile = Cached_tiles.get((tileset, ref, h), False)
    if not tile:
        tile = draw_tile(tileset, ref, h)
        Cached_tiles[(tileset, ref, h)] = tile
    return tile
    
def draw_tile(tileset, ref, h):
    x, y = ref%8, ref//8
    rect = pygame.Rect(64*x, 64*y, 64, min(64, 32+32*h))
    tileset_img = load_tileset(tileset)
    surf = load_mask(h)
    tile_src = tileset_img.subsurface(rect)
    surf.blit(tile_src, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    surf.fill((0,0,0,0), ((0, 64), (64, 344)))
    return surf


Masks = {}

def load_mask(h):
    "load cached mask or draw and cache a new one"
    mask = Masks.get(h, None)
    if not mask:
        path = os.path.join('tilesets','masks')
        mask = load_image(path, "mask%s.bmp"%h)
        colorkey = mask.get_at((0,0))
        mask.set_colorkey(colorkey, pygame.RLEACCEL)
        mask = mask.convert_alpha()
        Masks[h] = mask
    return mask.copy()

def load_windowskin(skin):
    return load_image('windowskin', skin)
        
Iconeset = None
def iconset():
    if not surf:
        Iconeset = load_image('icones', 'iconeset.png')
    return Iconeset

def face(face_name):
    pass

def character(character_name):
    pass

if __name__ == "__main__":
    import pygame, os
    os.chdir('images/tilesets')
    ref_mask = pygame.image.load('mask0.bmp')
    surf_bas = ref_mask.subsurface(pygame.Rect(0,16,64,16))
    surf_haut = ref_mask.subsurface(pygame.Rect(0,0,64,16))
    for i in range(40):
        surf = pygame.Surface((64, 32 + 8*i))
        surf.fill((255,255,255))
        surf.blit(surf_haut, (0,0))
        surf.blit(surf_bas, (0,16+8*i))
        pygame.image.save(surf, "masks/mask%s.bmp"%i)
        surf.blit(surf_haut, (0,0))
