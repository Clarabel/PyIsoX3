import pygame, time
import cache, cursor
from data import maps
import random
map1 = maps.map1

map_x, map_y = 20, 40
screen_x, screen_y = map_x*64+32, map_y*16+32+16
screen = pygame.display.set_mode((screen_x, screen_y))
offsety = 32
screen.fill((212,191,18))
pygame.display.flip()
######################################
##tile = cache.load_tile('tile.bmp')
##tile2 = cache.load_tile('tile2.bmp')



##mask0 = cache.load_tile('mask0.bmp')
##mask1 = cache.load_tile('mask1.bmp')
##mask0
##
##all_masks = [mask0, mask1]
try:
    all_tiles = pygame.sprite.LayeredDirty()
    all_sprites = pygame.sprite.LayeredDirty()

    cursor_img = cache.load_tileset('test0.bmp', alpha=False).convert()
    cursor_sprite = cursor.Cursor(cursor_img)
    cursor_sprite.add(all_sprites)
    all_sprites.change_layer(cursor_sprite, 1)

    #chargement de la map1

    map_x = len(map1[0])
    map_y = len(map1)
    screen_x, screen_y = map_x*64+32, map_y*16+32+16
    #29x64
    screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)

    startx = 32*(map_y-1)
    for i in range(map_x):
        for j in range(map_y):
            x = startx + 32*i-32*j
            y = 32+16*i+16*j
            rect = pygame.Rect(x, y, 64, 32)
            sprite = pygame.sprite.DirtySprite(all_sprites, all_tiles)
            all_sprites.change_layer(sprite, 10*(i+j))
            h = map1[j][i][1]
            ref = map1[j][i][0]
            sprite.image = cache.load_tile(ref, h)
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = x
            sprite.rect.bottom = y+32
            sprite.dirty=0
    map_boundaries=[#minx, miny, width, height
        0, 0, 32*(map_x+map_y-1), 16*(map_x+map_y+2)]
    
    background = pygame.Surface((1920, 1080))
    background.fill((12,191,180))
    all_sprites.clear(screen, background)
    all_sprites.draw(screen, background)
    pygame.display.flip()
    continuer = True
    horloge = pygame.time.Clock()
    pygame.event.clear()
    pygame.key.set_repeat(200, 100)
    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
               event.type == pygame.MOUSEBUTTONDOWN:
                print('bye!')
                continuer = False
                break
            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_DOWN and\
                   map_boundaries[1]<0:
                    dy = +32
                elif event.key == pygame.K_UP and\
                     map_boundaries[1]+map_boundaries[3]>=600:                    dy = -32
                elif event.key == pygame.K_LEFT and\
                      map_boundaries[0]+map_boundaries[2]>=800:
                    dx = -32
                elif event.key == pygame.K_RIGHT and\
                     map_boundaries[0]<0:
                    dx = +32
                for spr in all_sprites:
                    spr.rect.move_ip(dx, dy)
                    spr.dirty = 1
                map_boundaries[0] += dx
                map_boundaries[1] += dy
        #positionner la souris
        m_pos = pygame.mouse.get_pos()
        dist=lambda a:abs(a[0]+32-m_pos[0])+2*abs(a[1]+16-m_pos[1])
        tiles = all_tiles.get_sprites_at(m_pos)
        #choisi le meilleur tile
        tle=None
        if tiles:
            cursor_sprite.visible = 1
            tiles.sort(key=lambda pos:all_sprites.get_layer_of_sprite(pos))
            for tile in reversed(tiles):
                if dist(tile.rect.topleft)<32:
                    tle = tile
                    break
        if tle:
            layer = all_sprites.get_layer_of_sprite(tle)
            all_sprites.change_layer(cursor_sprite, layer+1)
            cursor_sprite.rect.topleft = tle.rect.topleft
        else:
            cursor_sprite.visible = 0
        
        rects = all_sprites.draw(screen)
        pygame.display.update(rects)
        horloge.tick(60)
except:
    raise
pygame.quit()
