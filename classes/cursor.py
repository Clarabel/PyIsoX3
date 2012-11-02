import pygame
import cache
import Current

class Cursor(pygame.sprite.DirtySprite):

    def __init__(self, surf):
        surf.set_alpha(155)
        pygame.sprite.DirtySprite.__init__(self)
        self.layer = 23
        self.image = surf
        self.dirty = 2
        self.rect = surf.get_rect()
        self.last_pos = None

        
class EditorCursor(Cursor):

    def __init__(self, surf):
        Cursor.__init__(self, surf)
        #map coordinates
        self.x = 0
        self.y = 0
        self.map = None

    def update(self, all_sprites):
        if self.last_pos == self.pos:
            return
        self.last_pos = self.pos
        startx = self.map.startx
        self.rect.x = startx + 32*(self.x-self.y)
        self.rect.y = 16*(self.x+self.y) \
                      - 8*self.map.get_h(self.x, self.y)
        all_sprites.change_layer(self,
                                 2*(self.x+self.y)+1)

    def move(self, *rel):
        dx, dy = rel
        self.x = min(max(self.x+dx, 0), self.map.width-1)
        self.y = min(max(self.y+dy, 0), self.map.height-1)

    def key_move(self, key):
        dx, dy = 0, 0
        if key == pygame.K_DOWN:
            dy = 1
        elif key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        self.move(dx, dy)

    def _get_pos(self):
        return self.x, self.y

    def _set_pos(self, pos):
       self.x, self.y = pos

    pos = property(lambda self: self._get_pos(),
                   lambda self, value: self._set_pos(value))
