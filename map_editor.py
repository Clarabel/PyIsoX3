#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, pickle, os, re
from pygame.locals import *
import classes.gamemap as gamemap
from classes.database import DataBase, DataMap
from classes.cursor import EditorCursor
from classes.window import *
import cache
import time


class EditorIso(object):
    
    COLOR_BGD=0x60a7ff
    SCREEN_MAP_POS = (12, 44)
    DEFAULT_SCREEN_SIZE = (1024, 768)
    DEFAULT_MAP_SCREEN_SIZE = (728, 600)
    
    def __init__(self, screen_size=None, mapsize=None):
        if not screen_size:
            screen_size = EditorIso.DEFAULT_SCREEN_SIZE
        if not mapsize:
            mapsize = EditorIso.DEFAULT_MAP_SCREEN_SIZE
        #set the display screen
        self.init_display(screen_size)
        #map frame
        self.mapsize = mapsize
        self.map_screen_rect = Rect(EditorIso.SCREEN_MAP_POS, self.mapsize)

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
        self.screen_size = screen_size
                
    def set_map(self, name='', data=None):
        if name:
            self.datamap = self.load_mapdata(name)
        elif data:
            self.datamap = data
        else:
            return
        self.map = gamemap.GameMap(self.datamap)
        self.map.draw_tiles()
        #create cursor
        self.cursor = EditorCursor(self.map)
        
    def new_map(self, screen):
        #create a new map
        new_data = DataMap()
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
            data = win_new_map.new_data
            self.set_map(data=data)
            
    def init_windows(self):
        windows = {}
        windows['tilesets'] = WindowTileset(self.map)
        windows['thumb'] = WindowThumbTile(windows['tilesets'])
        windows['map'] = WindowMap(self.map_screen_rect.size, self.map)
        windows['name'] = WindowNameMap(self.map_screen_rect.w, 40)
        for window in windows.values():
            window.draw(self.screen)
        return windows
            
    def write_name(self):
        "write the name of the map and return rect"
        w = self.map_screen_rect.w
        h = self.map_screen_rect.y
        x = self.map_screen_rect.x
        self.screen.fill((212,191,18), (x, 0, w, h))
        title_font = pygame.font.SysFont("timesnewroman", 40,
                                         bold=True, italic=True)
        title_surf = title_font.render(self.map.name, 1, (115,58,179))
        wt, ht = title_surf.get_size()
        title_rect = self.screen.blit(title_surf, ((w-wt)/2, (h-ht)/2))
        return title_rect

    def load_map(self):
        maps_names = []
        for datamap in DataBase.maps:
            maps_names.append(datamap.name)
        n = WindowChoices(maps_names).loop()
        self.set_map(data=DataBase.maps[n])
        
    def load_mapdata(self, name):
        filename = os.path.join('data', 'maps', name)
        with open(filename, 'r') as f:
            data_map = pickle.load(f)
        return data_map

    def save_mapdata(self):
        filename = self.map.data.get_filename()
        text = "Enregistrer la carte %s ?"%(filename[:-4])
        if WindowConfirm(text).loop():
            self.map.data.save()
            
    def rename_map(self):
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
        return new_name
    
    def set_tile_infos(self, win_thumb):
        "set cursor square infos to win_thumb infos"
        win_thumb.tile_infos = self.cursor.square_infos
        
                
##    def modifie_sol(self, key):
##        "modifie le sol avec PAGEUP et PAGEDOWN"
##        dref = (pygame.K_PAGEUP == key) - (pygame.K_PAGEDOWN == key)
##        ref = self.map.get_tileref(x, y)
##        self.map.set_tileref(ref + dref, x, y)

        
            
 
            
    def main(self):
        """main loop of editor"""
        #screen initialise
        screen = self.screen
        map_screen = self.screen.subsurface(self.map_screen_rect)
        #rect of the view
        screen_rect = self.map_screen_rect.copy()
        #orange background
        self.screen.fill(EditorIso.COLOR_BGD)
        #initialise event
        pygame.event.clear()
        pygame.key.set_repeat(200, 50)
        #thumb & tile window
        
        windows = self.init_windows()
        #Name of the map
        
        pygame.display.flip()
        continuer = True
        #initialise state button
        map_left_button_pressed = False
        start_time = time.time()
        horloge = pygame.time.Clock()
        while continuer:
            for event in pygame.event.get():
                ctrl = pygame.key.get_mods() & KMOD_CTRL
                if event.type == pygame.QUIT or\
                   event.type == KEYDOWN and event.key == K_ESCAPE:
                    continuer = False
                    return
                elif event.type == MOUSEMOTION:
                    if self.map_screen_rect.collidepoint(event.pos):
                        if pygame.mouse.get_pressed()[1]:
                            screen_rect.move_ip(event.rel[0], event.rel[1])
                        elif not('last_roll'in locals() and\
                                time.time() - last_roll < 0.5):
                            x, y = event.pos
                            x -= screen_rect.x
                            x -= windows['map'].contents_rect.x
                            y -= screen_rect.y
                            y -= windows['map'].contents_rect.y
                            self.cursor.move_to_screen(x, y)
                        
                elif event.type == MOUSEBUTTONDOWN:
                    button = event.button
                    if windows['tilesets'].onclick(event) or\
                       windows['thumb'].update_onclick(event):
                        pass
                    elif windows['map'].rect.collidepoint(event.pos):
                        if button in [4, 5]:
                            last_roll = time.time()
                            dh = (5 == button) - (4 == button)
                            self.cursor.h += dh
                            x, y = event.pos
                            y -= 8*dh
                            pygame.mouse.set_pos([x,y])
                        elif button == 3:
                            self.set_tile_infos(windows['thumb'])
                        elif button == 1 :
                            map_left_button_pressed = True 
                    elif windows['name'].rect.collidepoint(event.pos):
                        self.rename_map()

                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    map_left_button_pressed = False
                elif pygame.key.get_pressed()[K_SPACE]:
                        map_left_button_pressed = True
                elif event.type == KEYDOWN:
                    key = event.key
                    if key == K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == K_s and ctrl:
                        self.save_mapdata()
                    elif event.key == K_l and ctrl:
                        self.load_map()
                        windows['map'].map = self.map
                    elif ctrl and event.key == K_n :
                        self.new_map(screen)
                        windows['map'].map = self.map
                    elif key == K_q and ctrl:
                       pygame.event.post(pygame.event.Event(QUIT, {}))
                    elif key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                        self.cursor.update(event)
                    elif key in [K_KP_PLUS, K_KP_MINUS]:
                        dh = (K_KP_PLUS == key) - (K_KP_MINUS == key)
                        self.cursor.h += dh
                    elif key == K_c:
                        self.set_tile_infos(windows['thumb'])
                    elif key == K_v:
                        self.cursor.square_infos = windows['thumb'].tile_infos
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        map_left_button_pressed = False
            if map_left_button_pressed:
                #left clic on the map
                tset, tref, h = windows['thumb'].tile_infos
                if not(ctrl):
                    h = self.cursor.h
                self.cursor.square_infos = tset, tref, h
            windows['name'].update(self.map.name)
            windows['map'].update(screen_rect, self.cursor)
            
            for win in windows.values():
                win.draw(screen)
            pygame.display.flip()
            horloge.tick(60)

            
if __name__ == '__main__':
    pygame.init()
    try:
        screen = pygame.display.set_mode((1024, 768))
        editor = EditorIso(screen_size = (1024, 768), mapsize = (728, 600))
        editor.load_map()
        editor.main()
        pygame.quit()
    except:
        pygame.quit()
        raise
    
