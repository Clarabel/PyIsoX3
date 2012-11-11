import pygame
import cache
import Current

class Cursor(pygame.sprite.DirtySprite):

    def __init__(self, gamemap):
        pygame.sprite.DirtySprite.__init__(self)
        self.layer = 15
        self.dirty = 2
        #map coordinates
        self.map = gamemap
        self.x = 0
        self.y = 0
    
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = min(max(value, 0), self.map.width-1)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = min(max(value, 0), self.map.height-1)


    def _get_pos(self):
        return self.x, self.y
    def _set_pos(self, pos):
       self.x, self.y = pos
    pos = property(_get_pos, _set_pos)

    
class EditorCursor(Cursor):

    def __init__(self, gamemap):
        Cursor.__init__(self, gamemap)
        self._h = 0
        self.rect = pygame.Rect(0,0,0,0)
        self.draw_image()
    
    @property
    def h(self):
        return self.map.get_h(self.x, self.y)
        return self._h
##    @h.setter
##    def h(self, value):
##        self._h = min(max(0, value), 39)
        
    def draw_image(self):
        self.image = cache.load_cursor('iso_editor.bmp', 0)#self.h)
        self.rect.size = self.image.get_size()
        
##    def update(self):
##        if self.last_pos == (self.pos, self.h):
##            return
##        self.last_pos = self.pos, self.h
##        startx = self.map.startx
##        self.rect.x = startx + 32*(self.x-self.y)
##        self.rect.y = 16*(self.x+self.y) - 8*self.h
##        try:
##            self.h = self.map.get_tile_at(self.x, self.y)
##        except:
##            print('cursor upadte error at (%s,%s)'%(self.pos), tile)
            
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def move_to_screen(self, x, y):
        pos = self.map.mouse_square(x, y)
        if pos:
            self.pos = pos
        
    def update(self, event):
        dx, dy = 0, 0
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_DOWN:
                dy = 1
            elif key == pygame.K_UP:
                dy = -1
            elif key == pygame.K_LEFT:
                dx = -1
            elif key == pygame.K_RIGHT:
                dx = 1
        self.move(dx, dy)

