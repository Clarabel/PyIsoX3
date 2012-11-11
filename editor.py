import pygame, pickle, os
from pygame.locals import *
import classes.gamemap as gamemap
from classes.cursor import EditorCursor
from classes.windows import WindowTile, WindowTileset, WindowInput, WindowConfirm
import cache
import time


class EditorIso():

    def __init__(self, name=''):
        self.datamap = self.load_mapdata(name)
    
    def main(self):
        """main loop of editor"""
        self.load_new_map()
        screen = pygame.display.get_surface()
        map_screenrect = Rect((12,44),mapsize)
        map_screen = screen.subsurface(map_screenrect)
        screen_w, screen_h = screen.get_size()
        map_w, map_h = mapsize
        self.map.draw_tiles()

        continuer = True
        horloge = pygame.time.Clock()
        pygame.event.clear()
        pygame.key.set_repeat(200, 50)
        pygame.display.flip()
        
        #thumb tile window
        windows = {}
        windows['thumb'] = WindowTile(self.map)
        #windows['thumb'].draw(screen)
        self.cursor = EditorCursor(windows['thumb'].tile)
        self.cursor.map = self.map
        screen_rect = map_screenrect.copy()
        real_x, real_y = 16*screen_rect.x, 16*screen_rect.y
        windows['tilesets'] = WindowTileset(self.map)
        for window in windows.values():
            window.draw(screen)
        #Name of the map
        title_rect = self.write_name(screen, map_w, map_screenrect.y)
        
        pygame.display.flip()
        while continuer:
            for event in pygame.event.get():
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
                        pos = self.map.mouse_square(x, y)
                        if pos:
                            self.cursor.pos = pos
                        
                elif event.type == MOUSEBUTTONDOWN:
                    key = event.button
                    if windows['tilesets'].onclick(event):
                        tset = windows['tilesets'].tileset
                        ref = windows['tilesets'].tileref
                        windows['tilesets'].draw(screen)
                        windows['thumb'].update(tileset=tset, ref=ref)
                        pygame.display.flip()
                    elif event.button in [4, 5]:
                        if windows['thumb'].rect.collidepoint(event.pos):
                            dh = 1*(key == 5) - 1*(key == 4)
                            h = windows['thumb'].h + dh
                            windows['thumb'].update(h=h)
                            self.cursor.h = h
                    elif event.button == 1 and\
                         map_screen.get_rect().collidepoint(event.pos):
                        #left clic on the map
                        x, y = self.cursor.pos
                        tset, tref, h = windows['thumb'].tile_infos
                        self.map.set_tile_infos(x, y, tset, tref, h)
                        
                    elif event.button == 3:
                        if map_screenrect.collidepoint(event.pos):    
                            x, y = self.cursor.pos
                            tileset, ref, h = self.map.get_tile_infos(x, y)
                            windows['thumb'].update(tileset, ref, h)
                        elif title_rect.collidepoint(event.pos):
                            name_input = WindowInput(self.map.name)
                            new_name = name_input.main()
                            if new_name:
                                self.map.name = new_name
                            self.write_name(screen, map_w, map_screenrect.y)
                            del name_input
##                    elif event.button == 7:
##                        print('gauche haut')
##                    elif event.button == 8:
##                        print('gauche bas')
##                    else:
##                        print(event.button)
                elif event.type == KEYDOWN:
                    if event.key == K_s and pygame.key.get_mods() & KMOD_LCTRL:
                        text = "Enregistrer la carte %s ?"%('map001.pxs')
                        if WindowConfirm(text).loop():
                            self.save_mapdata('map001.pxs')
                    elif event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                        self.cursor.key_move(event.key)
                    elif event.key in [K_KP_PLUS, K_KP_MINUS]:
                        self.modifie_height(event.key)
                    elif event.key in [K_PAGEDOWN, K_PAGEUP]:
                        #modifie le sol
                        self.modifie_sol(event.key)
                    elif event.key == K_c:
                        x, y = self.cursor.pos
                        tileset, ref, h = self.map.get_tile_infos(x, y)
                        windows['thumb'].update(tileset, ref, h)
                    elif event.key == K_v:
                        x, y = self.cursor.pos
                        tset, tref, h = windows['thumb'].tile_infos
                        self.map.set_tile_infos(x, y, tset, tref, h)

            #draw sprites on map
            map_screen.fill((211, 188,100))
            ox, oy = screen_rect.topleft
            for tile in self.map.tiles:
                tile_rect = tile.rect.move(ox, oy)
                if tile.x == self.cursor.x and\
                   tile.y == self.cursor.y:
                    map_screen.blit(tile.image, tile_rect, tile.source_rect)
                    map_screen.blit(self.cursor.image,tile_rect)
                else:
                    map_screen.blit(tile.image, tile_rect, tile.source_rect)
            pygame.display.flip()
            horloge.tick(60)
            
    def write_name(self, screen, w, h):
        "write the name of the map and return rect"
        screen.fill((212,191,18), (0,0, w, h))
        title_font = pygame.font.SysFont("timesnewroman", 40,
                                         bold=True, italic=True)
        title_surf = title_font.render(self.map.name, 1, (115,58,179))
        wt, ht = title_surf.get_size()
        title_rect = screen.blit(title_surf, ((w-wt)/2, (h-ht)/2))
        return title_rect
    
    def load_new_map(self):
        """load a new_map from data"""
        self.map = gamemap.GameMap(self.datamap)
        
##    def create_cursor(self):
##        "create cursor, return None"
##        self.cursor = EditorCursor()

##    def center_screen(self, real_x, real_y, screen_rect, scroll_speed=12):
##        "parametre le scrolling de la vue"
##        #accélère le scrolling si le curseur est trop loin
##        map_diag = (self.map.width+self.map.height)
##        screen_w, screen_h = screen_rect.size
##        calc_dim = (32*map_diag-screen_w, 16*map_diag-screen_h)
##        scroll_x = 16*(min(calc_dim[0], max(0, self.cursor.rect.x\
##                                            - (screen_w-64)//2))) - real_x
##        scroll_y = 16*(min(calc_dim[1], max(0, self.cursor.rect.y\
##                                            - (screen_h-32)//2))) - real_y
##        if scroll_x or scroll_y:
##            dblex = abs(scroll_x)//(60*scroll_speed) +1
##            dbley = abs(scroll_y)//(60*scroll_speed) +1
##            real_x += dblex * max(-scroll_speed, min(scroll_speed, scroll_x))
##            real_y += dbley * max(-scroll_speed, min(scroll_speed, scroll_y))
##        #return screen_x, screen_y
##        screen_rect.topleft = real_x//16, real_y//16
##
##        return  real_x, real_y

    def modifie_sol(self, key):
        "modifie le sol avec PAGEUP et PAGEDOWN"
        dref = (pygame.K_PAGEUP == key) - (pygame.K_PAGEDOWN == key)
        ref = self.map.get_tileref(self.cursor.x, self.cursor.y)
        self.map.set_tileref(ref + dref, self.cursor.x, self.cursor.y)

    def modifie_height(self, key):
        "modifie la hauteur avec les touches PLUS et MINUS"
        dh = (K_KP_PLUS == key) - (K_KP_MINUS == key)
        h = self.map.get_h(self.cursor.x, self.cursor.y)
        self.map.set_height(h + dh, self.cursor.x, self.cursor.y)
                    
##    def draw_fps(self, screen, delai, fps_bmp):
##        if 0: return
##        fps = str(int(delai))#int(horloge.get_fps()))
##        fps_bmp.fill((0,0,0))
##        txt = FPS_FONT.render(fps, 1, (255,255,255))
##        fps_bmp.blit(txt, (1,1))
##        screen.blit(fps_bmp, (0, 0))
        
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
            
#################TODO###################
#class Editor2D:

if __name__ == '__main__':
    pygame.init()
    FPS_FONT = pygame.font.SysFont("",32)
    fps_bmp = pygame.Surface((40, 40))
    
    #initialise le screen
    print(pygame.display.list_modes())
    screen_size = (1580, 856)#pygame.display.list_modes()[1]
    mapsize = (1024, 768)#pygame.display.list_modes()[3]
    screen = pygame.display.set_mode(screen_size,
              #pygame.FULLSCREEN |
                                     pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

    
    screen.fill((212,112,18))
    #charge la carte 1 de test
    
    try:
        editor = EditorIso('map001.pxs')
    
        editor.main()
    except:
        pygame.quit()
        raise
