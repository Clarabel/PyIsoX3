import pygame
from classes.gamemap import IsoTile
from pygame import Rect
import cache as Cache
from _windowbase import Window, WindowUser, WLH
from _widget import *


class WindowTile(Window):
    """draw the active IsoTile for the IsoEditor"""
    def __init__(self, gamemap):
        w = 64 + 64 + 32
        h = 64 + 64 + 32
        screen_w, screen_h = pygame.display.get_surface().get_size()
        x = screen_w - w
        y = 0
        Window.__init__(self, x, y , w, h)
        self.tile = IsoTile(0, 0)
        self.h = 0#map.get_height(i, j)
        self.ref = 0#map.get_tileref(i, j)
        self.tileset = 0#map.get_tileset(i, j)
        self.map = gamemap
        self.last_param = None
        self.create_contents()
        self.windowskin = Cache.load_windowskin('editor.png')
        self.update()
        
    @property
    def tilesetname(self):
        return self.map.tilesetname(self.tileset)
    
    def update(self, tileset=None, ref=None, h=None):
        if tileset != None: self.tileset = tileset
        if ref != None: self.ref = ref
        if h != None and 0<=h<40: self.h = h
        if self.last_param != (self.tilesetname, self.ref, self.h):
            self.last_param = self.tilesetname, self.ref, self.h
            self.refresh()
        self.draw(pygame.display.get_surface())
        pygame.display.update(self.rect)

    def mouseover(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False
    
    def refresh(self):
        self.tile.draw_image(self.tilesetname, self.ref, self.h, 0, 64+8*(self.h-8))
        self.contents.fill((0, 0, 0, 0))
        self.draw_text(64, 0, "h = %s"%self.h)
        self.draw_text(0, 128-WLH, self.tilesetname)
        self.contents.blit(self.tile.image, (0,0), (0,0,64,96))
        
    @property
    def tile_infos(self):
        return self.tileset, self.ref, self.h


class WindowTileset(Window):

    def __init__(self, gamemap):
        w = 512+2*self.offset
        h = 640+2*self.offset
        screen_w, screen_h = pygame.display.get_surface().get_size()
        x = screen_w - w
        y = screen_h - h
        Window.__init__(self, x, y, w, h)
        self.map = gamemap
        self.tileset = 0
        self.tileref = 0
        self.create_contents()
        self.windowskin = Cache.load_windowskin('editor.png')
        self.selected_rect = Rect(self.offset,self.offset,64,64)
    
    @property
    def offset(self):
        return 8
    
    @property
    def tilesetname(self):
        return self.map.tilesetname(self.tileset)
            
    def create_contents(self):
        self.contents = Cache.load_tileset(self.tilesetname)
        self.src_rect = Rect(0,0,512,640)

    def onclick(self, event):
        if self.rect.inflate(-2*self.offset,-2*self.offset)\
           .collidepoint(event.pos):
            if event.button == 1:
                x0, y0 = self.rect.move(self.offset, self.offset).topleft
                x = event.pos[0]-x0#abscisse in self.contents
                y = event.pos[1]-y0#ordonnée in self.contents
                ref = x//64 + 8*(y//64)
                if self.tileref != ref:
                    self.tileref = ref
                    self.selected_rect = Rect(self.offset+64*(ref%8),
                                              self.offset+64*(ref//8),64,64)
                    return True
        return False


class WindowNewMap(WindowUser):
    
    def __init__(self, datamap):
        w, h = 400, 400
        WindowUser.__init__(self, w, h)
        self.create_valid_cancel()
        self.data = datamap
        self.add_widgets()

    def add_widgets(self):
        sw = self.intputs = {}
        w = self.contents.get_rect().width
        dy =  WLH+8
        y = 0 + 7
        self.add_widget(TextBox(7, y, w-14, WLH,
                              u"Créer une nouvelle carte", align='center'))
        #text input : map name
        y += dy
        sw['name'] = InputText(7, y, self.data.name, width=w-14, parent=self)
        self.add_widget(sw['name'])
        #Number input : width
        y += dy
        x = 7
        sw['size'] = TextBox(x, y, 110, WLH,
                              u"Size = ", align='centerleft')
        x += sw['size'].rect.w + 4
        self.add_widget(sw['size'])
        sw['width'] = InputNumber(x, y, self.data.w, parent=self)
        self.add_widget(sw['width'])
        x += sw['width'].rect.w + 4
        sw['x'] = TextBox(x, y, 20, WLH,
                              u"X", align='center')
        self.add_widget(sw['x'])
        x += sw['x'].rect.w + 4
        #Number input : height
        sw['height'] = InputNumber(x, y, self.data.h, parent=self)
        self.add_widget(sw['height'])
        #Number input : Default height
        y += dy
        x = 7
        sw['text_alt'] = TextBox(x, y, 110, WLH,
                              u"Altitude = ", align='centerleft')
        self.add_widget(sw['text_alt'])
        x += 110
        sw['altitude'] = InputNumber(x, y, self.data.height[0, 0],
                                     digit=2, parent=self)
        self.add_widget(sw['altitude'])
        #Tileset chooser
        y += dy
        x = 7
        sw['text_tileset'] = TextBox(x, y, 110, WLH,
                              u"Tileset : ", align='centerleft')
        self.add_widget(sw['text_tileset'])
        sw['tileset'] = InputText(7+110, y, 'tileset.png', parent=self)
        self.add_widget(sw['tileset'])
        #sol chooser
        x = 7
        y += dy
        sw['text_sol'] = TextBox(x, y, 140, WLH,
                              u"Sol par défaut : ", align='centerleft')
        self.add_widget(sw['text_sol'])
        x += 140
        sw['sol'] = Widget(x, y, 64, 64, parent=self)
        sw['sol'].image.fill((209, 114, 224))
        self.add_widget(sw['sol'])
        
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
