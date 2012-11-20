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
        "return map height at cursor pos"
        return self.map.get_h(self.x, self.y)
    @h.setter
    def h(self, value):
        "set map height at cursor pos"
        self.map.set_height(value, self.x, self.y)
        
    def draw_image(self):
        self.image = cache.load_cursor('iso_editor.bmp', 0)#self.h)
        self.rect.size = self.image.get_size()
            
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
        
    @property
    def square_infos(self):
        return self.map.get_tile_infos(self.x, self.y)
    @square_infos.setter
    def square_infos(self, tile_infos):
        tset, tref, h = tile_infos
        self.map.set_tile_infos(self.x, self.y, *tile_infos)
