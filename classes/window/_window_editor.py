import pygame
from classes.gamemap import IsoTile
from pygame import Rect
import cache as Cache
from _windowbase import Window, WindowUser, WLH
from _widget import *


class WindowThumbTile(Window):
    """draw the active IsoTile for the IsoEditor"""

    H_MAX = 4
    
    def __init__(self, window_tileset):
        h_max = WindowThumbTile.H_MAX
        w = 2*self.offset + 64 + self.font.size('h = 99 ')[0]
        h = 2*self.offset + 32 + 8*h_max + self.font.get_linesize()
        screen_w, screen_h = pygame.display.get_surface().get_size()
        x = screen_w - w
        y = 0
        Window.__init__(self, x, y , w, h)
        self.tile = IsoTile(0, 0)
        self.h = 0#map.get_height(i, j)
        self.window_tileset = window_tileset
        self.last_param = None
        self.create_contents()
        self.windowskin = Cache.load_windowskin('editor.png')
        self.update()

    @property
    def ref(self):
        return self.window_tileset.tileref
    @ref.setter
    def ref(self, value):
        self.window_tileset.tileref = value
        
    @property
    def tileset(self):
        return self.window_tileset.tileset
    @tileset.setter
    def tileset(self, value):
        self.window_tileset.tileset = value
        
    @property
    def tilesetname(self):
        return self.window_tileset.tilesetname

    @property
    def offset(self):
        return 8
    
    def update(self, tileset=None, ref=None, h=None):
        if tileset != None: self.tileset = tileset
        if ref != None: self.ref = ref
        if h != None and 0<=h<40: self.h = h
        if self.last_param != (self.tilesetname, self.ref, self.h):
            self.last_param = self.tilesetname, self.ref, self.h
            self.need_refresh = True
            
    def mouseover(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False
    
    def refresh(self):
        self.need_refresh = False
        self.tile.draw_image(self.tilesetname, self.ref, self.h, 0, 64+8*(self.h-8))
        self.contents.fill((0, 0, 0, 0))
        self.draw_text(64, 0, "h = %s"%self.h)
        self.draw_text(0, self.contents_rect.height-self.font.get_linesize(),
                       self.tilesetname)
        self.contents.blit(self.tile.image, (0,0), (0,0,64,96))
        
    @property
    def tile_infos(self):
        return self.tileset, self.ref, self.h
    @tile_infos.setter
    def tile_infos(self, tile_infos):
        self.update(*tile_infos)
        
    def update_onclick(self, event):
        if self.rect.collidepoint(event.pos):
            dh = (event.button == 5) - (event.button == 4)
            if dh:
                self.update(h=self.h + dh)
            return True #get focus
        return False #have not focus

    def draw(self, destsurf):
        if self.need_refresh:
            self.refresh()
            Window.draw(self, destsurf)

            
class WindowTileset(Window):

    def __init__(self, gamemap):
        w = 512/2+2*self.offset
        h = 640/2+2*self.offset
        screen_w, screen_h = pygame.display.get_surface().get_size()
        x = screen_w - w
        y = screen_h - h
        Window.__init__(self, x, y, w, h)
        self.map = gamemap
        self.selected_rect = Rect(self.offset,self.offset,32,32)
        self.tileset = 0
        self._tileref = 0
        self.create_contents()
        self.need_refresh = True
        self.windowskin = Cache.load_windowskin('editor.png')
        
    @property
    def tileref(self):
        return self._tileref
    @tileref.setter
    def tileref(self, ref):
        self.need_refresh = True
        self._tileref = ref
        rx, ry = self.selected_rect.size 
        self.selected_rect.topleft = (self.offset+rx*(ref%8),
                                      self.offset+ry*(ref//8))
        
    @property
    def contents_src(self):
        self.contents_rect.move(self.scroll_x, self.scroll_y)

    @property
    def scroll_x(self):
        return 0
    @property
    def scroll_y(self):
        return 0
    
    @property
    def offset(self):
        return 8
    
    @property
    def tilesetname(self):
        return self.map.tilesetname(self.tileset)
            
    def create_contents(self):
        self.contents = pygame.Surface((512/2, 640/2)).convert_alpha()
        tset_src = Cache.load_tileset(self.tilesetname)
        pygame.transform.scale(tset_src, (256, 320), self.contents)
        self.src_rect = Rect(0,0,512,640)

    def onclick(self, event):
        if self.contents_rect.collidepoint(event.pos):
            if event.button == 1:
                x0, y0 = self.rect.move(self.offset, self.offset).topleft
                x = event.pos[0]-x0#abscisse in self.contents
                y = event.pos[1]-y0#ordonnée in self.contents
                rx, ry = self.selected_rect.size 
                ref = x//rx + 8*(y//ry)
                if self.tileref != ref:
                    self.tileref = ref
                    return True
        return False

    @property
    def tile(self):
        return self.tileset, self.tilref

    def draw(self, destsurf):
        if self.need_refresh:
            self.need_refresh = False
            Window.draw(self, destsurf)

            
class WindowNewMap(WindowUser):
    
    def __init__(self, datamap):
        w, h = 400, 400
        WindowUser.__init__(self, w, h)
        self.create_valid_cancel()
        self.data = datamap
        self.add_widgets()

    def add_widgets(self):
        sw = self.intputs = {}
        rows = VerticalBox(7, 7)
        self.add_widget(rows)
        w = self.contents.get_rect().width
        dy =  WLH+8
        y = 0 + 7
        rows.add(TextBox(0, 0, w-14, WLH,
                              u"Créer une nouvelle carte", align='center'))
        
        sw['name'] = InputText(0, 0, self.data.name, width=w-14, parent=self)
        rows.add(sw['name'])
        
        linesize = HorizontalBox(0,0)
        linesize.add(TextBox(0, 0, 110, WLH,
                              u"Size = ", align='centerleft'))
        sw['width'] = InputNumber(0, 0, self.data.w, parent=self)
        linesize.add(sw['width'])
        linesize.add(TextBox(0, 0, 20, WLH,
                              u"X", align='center'))
        
        #Number input : height
        sw['height'] = InputNumber(0, 0, self.data.h, parent=self)
        linesize.add(sw['height'])
        #Number input : Default height
        linealt = HorizontalBox(0,0)
        linealt.add(TextBox(0, 0, 110, WLH,
                              u"Altitude = ", align='centerleft'))
        sw['altitude'] = InputNumber(0, 0, self.data.height[0, 0],
                                     digit=2, parent=self)
        linealt.add(sw['altitude'])
        #Tileset chooser
        lineset = HorizontalBox(0,0)
        lineset.add(TextBox(0, 0, 110, WLH,
                              u"Tileset : ", align='centerleft'))
        sw['tileset'] = InputText(7+110, y, 'tileset.png', parent=self)
        lineset.add(sw['tileset'])
        #sol chooser
        linesol = HorizontalBox(0,0)
        linesol.add(TextBox(0, 0, 140, WLH,
                              u"Sol par défaut : ", align='centerleft'))
        sw['sol'] = Widget(0, 0, 64, 64, parent=self)
        sw['sol'].image.fill((209, 114, 224))
        linesol.add(sw['sol'])
        rows.add(linesize)
        rows.add(linealt)
        rows.add(lineset)
        rows.add(linesol)
        rows.x = 7
        rows.y = 7
        
    def draw_widgets(self):
        for widget in self.widgets:
            widget.draw(self.contents)
            
    def draw(self, surf):
        self.draw_widgets()
        Window.draw(self, surf)

    @property
    def new_data(self):
        sw = self.intputs
        #sw['tileset']sw['sol']
        self.data.size = (sw['width'].number, sw['height'].number)
        self.data.tilesets = [sw['tileset'].text]
        self.data.tileset.fill(0)
        self.data.tileref.fill(0)
        self.data.height.fill(sw['height'].number)
        self.data.name = sw['name'].text
        
        return self.data


class WindowMap(Window):
    "window for display map rendering"
    
    def __init__(self, size, game_map):
        x = 12
        y = 48
        w = size[0] + self.offset
        h = size[1] + self.offset
        Window.__init__(self, x, y, w, h)
        self.map = game_map
        screen = pygame.display.get_surface()
        self.image = screen.subsurface((x, y), (w, h))
        self.create_contents()
        self.last_param = None
        pygame.display.get_surface()
        #print(self.image.get_flags(), screen.get_flags())
        
    def draw(self, screen):
        pass
        #screen.blit(self.image, self.rect)
        screen.blit(self.contents, self.rect.move(self.offset, self.offset))
    
    def create_contents(self):
        rect = self.image.get_rect().inflate(-2*self.offset,-2*self.offset)
        self.contents = pygame.Surface(rect.size)#, flags=pygame.RLEACCEL)
        
    @property
    def offset(self):
        return 8

    def update(self, screen_rect, cursor):
        ox, oy = screen_rect.topleft
        if 1 or self.last_param != ((ox, oy), cursor.pos):
            self.last_param = ((ox, oy), cursor.pos)
            rect = self.contents_rect
            rect.topleft = 0,0
            #draw all tiles and cursor on map
            self.contents.fill((211, 188,100))
            
            for tile in self.map.tiles:
                tile_rect = tile.rect.move(ox, oy)
                if tile_rect.colliderect(rect):
                    self.contents.blit(tile.image, tile_rect, tile.source_rect)
                    if tile.x == cursor.x and tile.y == cursor.y:
                        self.contents.blit(cursor.image,tile_rect)
            
class WindowNameMap(Window):

    def __init__(self, width, height):
        x = 12
        y = 2
        width += self.offset
        height += self.offset
        Window.__init__(self, x, y, width, height)
        self.font = pygame.font.SysFont("timesnewroman", 40, bold=True, italic=True)
        self.create_contents()
        self.mapname = None
        
    @property
    def offset(self):
        return 2

    def update(self, mapname):
        "set and write the name of the map and return rect"
        if self.mapname != mapname:
            self.mapname = mapname
            self.contents.fill((212,191,18))
            title_surf = self.font.render(self.mapname, 1, (115,58,179))
            #centre le nom dans la fenêtre
            w, h = self.contents_rect.size
            wt, ht = title_surf.get_size()
            self.contents.blit(title_surf, ((w-wt)/2, (h-ht)/2))    
