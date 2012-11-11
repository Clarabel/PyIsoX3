#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, pickle, os
from pygame.locals import *
import classes.gamemap as gamemap
import classes.database as db
from classes.cursor import EditorCursor
from classes.window import *
import cache
import time


class EditorIso(object):

    def __init__(self, screen_size = (1580, 856), mapsize=(1024, 768)):
        #set the display screen
        self.init_display(screen_size)
        #map frame
        self.mapsize = mapsize
        self.map_screen_rect = Rect((12,44), self.mapsize)

    def init_display(self, screen_size):
        screen = pygame.display.get_surface()
        if screen:
            self.screen = screen
        else:
            self.screen = pygame.display.set_mode(screen_size,
                                     #pygame.FULLSCREEN |\
                                     pygame.HWSURFACE |\
                                     pygame.DOUBLEBUF,
                                     32)
        self.screen_size = self.screen.get_size()
                
    def set_map(self, name='', data=None):
        if name:
            self.datamap = self.load_mapdata(name)
        elif data:
            self.datamap = data
        else:
            #no data, no map
            return
        self.map = gamemap.GameMap(self.datamap)
        self.map.draw_tiles()
        #create cursor
        self.cursor = EditorCursor(self.map)

    def new_map(self, screen):
        #create a new map
        new_data = db.DataMap()
        win_new_map = WindowNewMap(new_data)
        pygame.display.get_surface()
        pygame.event.clear()
        result = None
        while result == None:
            for event in pygame.event.get():
                if event.type == KEYDOWN and\
                   event.key == K_ESCAPE:
                    return
                else:
                    result = win_new_map.update(event)
            win_new_map.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        if result:
            print('nouvelle map')
            data = win_new_map.new_data
            self.set_map(data=data)
            
    def init_windows(self):
        windows = {}
        windows['thumb'] = WindowTile(self.map)
        windows['tilesets'] = WindowTileset(self.map)
        for window in windows.values():
            window.draw(self.screen)
        return windows
            
    def write_name(self, screen, rect):
        "write the name of the map and return rect"
        w = rect.w
        h = rect.y
        x = rect.x
        screen.fill((212,191,18), (x, 0, w, h))
        title_font = pygame.font.SysFont("timesnewroman", 40,
                                         bold=True, italic=True)
        title_surf = title_font.render(self.map.name, 1, (115,58,179))
        wt, ht = title_surf.get_size()
        title_rect = screen.blit(title_surf, ((w-wt)/2, (h-ht)/2))
        return title_rect
        
    def modifie_sol(self, key):
        "modifie le sol avec PAGEUP et PAGEDOWN"
        dref = (pygame.K_PAGEUP == key) - (pygame.K_PAGEDOWN == key)
        
        ref = self.map.get_tileref(x, y)
        self.map.set_tileref(ref + dref, x, y)

    def modifie_height(self, dh):
        "modifie la hauteur avec les touches PLUS et MINUS"
        x, y = self.cursor.pos
        h = self.cursor.h
        self.map.set_height(h + dh, x, y)
        
    def load_mapdata(self, name):
        filename = os.path.join('data', 'maps', name)
        with open(filename, 'r') as f:
            data_map = pickle.load(f)
        return data_map

    def save_mapdata(self, name):
        data = self.map.data
        filename = os.path.join('data', 'maps', name)
        with open(filename, 'w') as f:
            pickle.dump(data, f)
            
    def rename_map(self, rect):
        screen = pygame.display.get_surface()
        name_input = WindowInput(self.map.name)
        new_name = None
        while new_name == None:
            name_input.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                result = name_input.update(event)
                if result != None:
                    new_name = result
                    break
        if new_name:
            self.map.name = new_name
            
        self.write_name(screen, rect)
        
    def set_square_infos(self, *tile_infos):
        x, y = self.cursor.pos
        self.map.set_tile_infos(x, y, *tile_infos)

    def set_tile_infos(self, win_thumb):
        x, y = self.cursor.pos
        tileset, ref, h = self.map.get_tile_infos(x, y)
        win_thumb.update(tileset, ref, h)
        
    def main(self):
        """main loop of editor"""
        #screen initialise
        screen = self.screen
        map_screenrect = self.map_screen_rect
        map_w, map_h = self.map_screen_rect.size
        map_screen = self.screen.subsurface(map_screenrect)
        screen_w, screen_h = self.screen.get_size()
        #rect of the view
        screen_rect = map_screenrect.copy()
        real_x, real_y = 16*screen_rect.x, 16*screen_rect.y
        #orange background
        self.screen.fill((212,112,18))
        #initialise event
        pygame.event.clear()
        pygame.key.set_repeat(200, 50)
        #thumb & tile window
        windows = self.init_windows()
        #Name of the map
        title_rect = self.write_name(screen, map_screenrect)
        
        pygame.display.flip()
        continuer = True
        #initialise state button
        map_left_button_pressed = False
        while continuer:
            
            for event in pygame.event.get():
                ctrl = pygame.key.get_mods() & KMOD_CTRL
                if event.type == pygame.QUIT or\
                   event.type == KEYDOWN and event.key == K_ESCAPE:
                    continuer = False
                    pygame.quit()
                    return
                elif event.type == MOUSEMOTION:
                    if pygame.mouse.get_pressed()[1]:
                        screen_rect.move_ip(event.rel)
                    if map_screenrect.collidepoint(event.pos):
                        x, y = event.pos
                        x -= screen_rect.x + map_screenrect.x
                        y -= screen_rect.y + map_screenrect.y
                        self.cursor.move_to_screen(x, y)
                        
                elif event.type == MOUSEBUTTONDOWN:
                    key = event.button
                    if windows['tilesets'].onclick(event):
                        tset = windows['tilesets'].tileset
                        ref = windows['tilesets'].tileref
                        windows['tilesets'].draw(screen)
                        windows['thumb'].update(tileset=tset, ref=ref)
                    elif event.button in [4, 5]:
                        if windows['thumb'].rect.collidepoint(event.pos):
                            dh = 1*(key == 5) - 1*(key == 4)
                            h = windows['thumb'].h + dh
                            windows['thumb'].update(h=h)
                        elif map_screen.get_rect().collidepoint(event.pos):
                            b = event.button
                            dh = (5 == b) - (4 == b)
                            self.modifie_height(dh)
                            x, y = event.pos
                            y -= 8*dh
                            pygame.mouse.set_pos([x,y])
                    elif event.button == 1 and\
                         map_screen.get_rect().collidepoint(event.pos):
                        map_left_button_pressed = True
                    elif event.button == 3:
                        if map_screenrect.collidepoint(event.pos):    
                            x, y = self.cursor.pos
                            tileset, ref, h = self.map.get_tile_infos(x, y)
                            windows['thumb'].update(tileset, ref, h)
                        elif title_rect.collidepoint(event.pos):
                            self.rename_map(map_screenrect)

                elif event.type == MOUSEBUTTONUP and\
                     event.button == 1:
                    map_left_button_pressed = False
                elif pygame.key.get_pressed()[K_SPACE]:
                        map_left_button_pressed = True
                elif event.type == KEYDOWN:
                    key = event.key
                    if event.key == K_s and ctrl:
                        text = "Enregistrer la carte %s ?"%('map001.pxs'[:-4])
                        if WindowConfirm(text).loop():
                            self.save_mapdata('map001.pxs')
                    elif ctrl and event.key == K_n :
                        self.new_map(screen)
                    elif key == K_q and ctrl:
                       pygame.event.post(pygame.event.Event(QUIT, {}))
                    elif key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                        self.cursor.update(event)
                    elif key in [K_KP_PLUS, K_KP_MINUS]:
                        dh = (K_KP_PLUS == key) - (K_KP_MINUS == key)
                        self.modifie_height(dh)
                    elif key == K_c:
                        self.set_tile_infos(windows['thumb'])
                    elif key == K_v:
                        self.set_square_infos(windows['thumb'].tile_infos)
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        map_left_button_pressed = False
            if map_left_button_pressed:
                #left clic on the map
                tset, tref, h = windows['thumb'].tile_infos
                if not(ctrl):
                    x, y = self.cursor.pos
                    h = self.cursor.h
                self.set_square_infos( tset, tref, h)
                        
            #draw all tiles and cursor on map
            map_screen.fill((211, 188,100))
            ox, oy = screen_rect.topleft
            for tile in self.map.tiles:
                tile_rect = tile.rect.move(ox, oy)
                map_screen.blit(tile.image, tile_rect, tile.source_rect)
                if tile.x == self.cursor.x and tile.y == self.cursor.y:
                    map_screen.blit(self.cursor.image,tile_rect)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == '__main__':
    pygame.init()
    try:
        editor = EditorIso(screen_size = (1580, 856), mapsize = (1024, 768))
        editor.set_map('map001.pxs')
        editor.main()
    except:
        pygame.quit()
        raise
