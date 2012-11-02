import pygame
from pygame.locals import *
from classes.cursor import EditorCursor
from classes.gamemap import GameMap
import cache
import time

class Editor:

    def __init__(self, datamap=None):
        self.datamap = datamap
        self.create_cursor()


def draw_black(surf, rect):
    surf.fill((0,0,0), rect)
    
class EditorIso(Editor):
    
    def main(self):
        """main loop of editor"""
        self.load_new_map()
        screen = pygame.display.get_surface()
        screen_w, screen_h = screen.get_size()
        self.map.draw()
        self.all_sprites = pygame.sprite.LayeredDirty()
        self.all_sprites.add(self.map.tiles, self.cursor)
        map_diag = (self.map.width+self.map.height)
        calc_dim = (32*map_diag, 16*map_diag)
        all_map_surf = pygame.Surface(calc_dim,  pygame.HWSURFACE)
        all_map_surf.fill((212, 138, 55))
        self.all_sprites.set_timing_treshold(1000 / 30)
        self.all_sprites.draw(all_map_surf)
        background = all_map_surf.copy()
        background = background.convert(32, pygame.RLEACCEL)
        print('bgd', background.get_flags())
        print('map', all_map_surf.get_flags())
        self.all_sprites.clear(all_map_surf, background)
##        for tile in self.map.tiles:
##            tile.kill()
        continuer = True
        horloge = pygame.time.Clock()
        pygame.event.clear()
        pygame.key.set_repeat(200, 50)
        
        self.cursor.move(0, 0)
        self.cursor.update(self.all_sprites)
        screen_x, screen_y = self.cursor.rect.x - screen_w//2,\
                             self.cursor.rect.y - 300//2
        real_x, real_y = 16*screen_x, 16*screen_y
        pygame.display.flip()
        tile_infos = None
        last_time = time.time()
        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or\
                   event.type == pygame.MOUSEBUTTONDOWN:
                    continuer = False
                    pygame.quit()
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        stop = pygame.event.Event(pygame.QUIT, {})
                        pygame.event.post(stop)
                        break
                    elif event.key in [K_DOWN, K_UP, K_LEFT, K_RIGHT]:
                        self.cursor.key_move(event.key)
                    elif event.key in [K_KP_PLUS, K_KP_MINUS]:
                        self.modifie_height(event.key)
                    elif event.key in [K_PAGEDOWN, K_PAGEUP]:
                        #modifie le sol
                        self.modifie_sol(event.key)
                    elif event.key == K_c:
                        x, y = self.cursor.pos
                        tile_infos = self.map.get_tile_infos(x, y)
                    elif event.key == K_v and tile_infos:
                        x, y = self.cursor.pos
                        self.map.set_tile_infos(x, y, tile_infos)
                        self.refresh_tile_at(self.cursor.pos)
            #update cursor z
            self.cursor.update(self.all_sprites)
            #screen update
            last_screen_pos = screen_x, screen_y
            real_x, real_y = self.center_screen(real_x, real_y)
            screen_x, screen_y = real_x//16, real_y//16
            srceen_rect = pygame.Rect(screen_x, screen_y, screen_w, screen_h)
            
            #draw sprites on map
            rects_a = self.all_sprites.draw(all_map_surf)
            
            screen.blit(all_map_surf, (0,0), srceen_rect)
            if 1:
                now = time.time()
                ftime = now - last_time
                last_time = now
                fps = str(int(horloge.get_fps()))
                fps_bmp.fill((0,0,0))
                txt = FPS_FONT.render(fps, 1, (255,255,255))
                fps_bmp.blit(txt, (1,1))
                screen.blit(fps_bmp, (0, 0))
            if last_screen_pos != (screen_x, screen_y):
                pygame.display.flip()
            else:
                for rect in rects_a:
                    rect.move_ip(-screen_x, -screen_y)
                rects_a.append(pygame.Rect(0,0,40,40))
                pygame.display.update(rects_a)
            horloge.tick(0)
            
    def load_new_map(self):
        """load a new_map from data"""
        self.map = GameMap(self.datamap)
        self.cursor.map = self.map
        
    def create_cursor(self):
        "create cursor, return None"
        surf = cache.load_cursor('iso_editor.bmp')
        self.cursor = EditorCursor(surf)

    def center_screen(self, real_x, real_y, scroll_speed=12):
        "parametre le scrolling de la vue"
        #accélère le scrolling si le curseur est trop loin
        map_diag = (self.map.width+self.map.height)
        screen_w, screen_h = pygame.display.get_surface().get_size()
        calc_dim = (32*map_diag-screen_w, 16*map_diag-screen_h)
        scroll_x = 16*(min(calc_dim[0], max(0, self.cursor.rect.x\
                                            - (screen_w-64)//2))) - real_x
        scroll_y = 16*(min(calc_dim[1], max(0, self.cursor.rect.y\
                                            - (screen_h-32)//2))) - real_y
        if scroll_x or scroll_y:
            dblex = abs(scroll_x)//(60*scroll_speed) +1
            dbley = abs(scroll_y)//(60*scroll_speed) +1
            real_x += dblex * max(-scroll_speed, min(scroll_speed, scroll_x))
            real_y += dbley * max(-scroll_speed, min(scroll_speed, scroll_y))
        #return screen_x, screen_y
        return  real_x, real_y

    def modifie_sol(self, key):
        "modifie le sol avec PAGEUP et PAGEDOWN"
        dref = (pygame.K_PAGEUP == key) - (pygame.K_PAGEDOWN == key)
        ref = self.map.get_tileref(self.cursor.x,
                                   self.cursor.y)
        self.map.set_tileref(ref + dref,
                            self.cursor.x, self.cursor.y)
        spr = self.map.refresh_tile_at(self.cursor.x,
                                       self.cursor.y)
        spr.add(self.all_sprites)

    def modifie_height(self, key):
        "modifie la hauteur avec les touches PLUS et MINUS"
        dh = (K_KP_PLUS == key) - (K_KP_MINUS == key)
        h = self.map.get_h(self.cursor.x, self.cursor.y)
        self.map.set_height(h + dh, self.cursor.x,
                            self.cursor.y)
        self.refresh_tile_at(self.cursor.pos)
        
    def refresh_tile_at(self, pos):
        x, y = pos
        spr = self.map.refresh_tile_at(x, y)
        spr.add(self.all_sprites)

    



        
#################TODO###################
#class Editor2D:

if __name__ == '__main__':
    pygame.init()
    FPS_FONT = pygame.font.SysFont("arial.ttf",32)
    fps_bmp = pygame.Surface((40, 40))
    
    #initialise le screen
    screen = pygame.display.set_mode((1920, 1080),
              pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

    test = pygame.display.mode_ok((1920, 1080),
            pygame.OPENGL | pygame.FULLSCREEN | pygame.HWSURFACE)
    print(test)
    
    #return 'youpi'
    print(pygame.display.Info())#,pygame.SDL_VIDEODRIVER)
    import pprint
    pprint.pprint(pygame.display.get_wm_info())

    
    screen.fill((212,191,18))
    #charge la carte 1 de test
    import data.maps as maps
    test_map = maps.map1
    
    editor = EditorIso(test_map)
    try:
        editor.main()
    except:
        pygame.quit()
        raise
