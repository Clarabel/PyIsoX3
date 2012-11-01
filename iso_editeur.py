import pygame

import data.maps as maps
import cache
from cursor import EditorCursor
import Current
from gamemap import GameMap, IsoTile

#charge la carte 1 de test
test_map = maps.map1
#initialise la carte
Current.Game_Map = GameMap(test_map)
print('Chargement réussi de', Current.Game_Map.name)

#initialise le screen
screen = pygame.display.set_mode((800, 600))
screen.fill((212,191,18))
#les tiles
all_tiles = pygame.sprite.LayeredDirty()
all_sprites = pygame.sprite.LayeredDirty()
background = pygame.Surface((800, 600))
background.fill((12,191,180))
#affiche la carte
game_map = Current.Game_Map
game_map.draw(all_tiles)
map_diag = (game_map.width+game_map.height)
calc_dim = (32*map_diag+32, 16*map_diag+32)
all_map_surf = pygame.Surface(calc_dim)
for tile in all_tiles:
    all_map_surf.blit(tile.image, tile.rect)

#crée le curseur
cursor = EditorCursor(cache.load_tileset('test0.bmp', alpha=False).convert())
all_sprites.add(all_tiles, cursor)
#all_sprites.clear(screen, background)
all_sprites.clear(all_map_surf, background)
#all_sprites.draw(screen, background)
all_sprites.draw(all_map_surf, background)
pygame.display.flip()
continuer = True
horloge = pygame.time.Clock()
pygame.event.clear()
pygame.key.set_repeat(200, 100)
all_map_pic = []

try:
    speed = 1
    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
               event.type == pygame.MOUSEBUTTONDOWN:
                print('bye!')
                continuer = False
                break
##            elif event.type == pygame.KEYDOWN and\
##                 event.key == pygame.K_RETURN:
##                map_diag = (game_map.width+game_map.height)
##                all_map_pic.append(pygame.Surface((32*map_diag, 16*map_diag)).convert())
##                print("il y a", len(all_map_pic), 'images dans la liste')
            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_DOWN:
                    dy = speed
                elif event.key == pygame.K_UP:
                    dy = -speed
                elif event.key == pygame.K_LEFT:
                    dx = -speed
                elif event.key == pygame.K_RIGHT:
                    dx = speed
                elif event.key == pygame.K_KP_PLUS:
                    h=game_map.get_h(cursor.x, cursor.y)
                    game_map.set_height(h+1, cursor.x, cursor.y)
                    for tile in all_tiles:
                        if tile.x == cursor.x and tile.y == cursor.y:
                            tile.kill()
                            sprite = game_map.new_tile(cursor.x, cursor.y,
                                                       all_tiles)
                            sprite.add(all_sprites)
                            
                cursor.move(dx, dy)
##                for spr in all_sprites:
##                    spr.rect.move_ip(dx, dy)
##                    spr.dirty = 1
        all_sprites.change_layer(cursor, 2*(cursor.x+cursor.y)+1)
        rects = all_sprites.draw(all_map_surf)
        #all_map_surf.blit(cursor.image, cursor.rect)
        screen.blit(all_map_surf, (0,0),
                    pygame.Rect(cursor.rect.x-400, cursor.rect.y-300,
                                                     800, 600))
        #pygame.display.update(rects)
        pygame.display.flip()
        horloge.tick(0)
        #print(horloge.get_fps())
    from pprint import *
    pprint(cache.cached_tiles)
    pprint(all_sprites)
except:
    raise
pygame.quit()


