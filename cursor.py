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

class EditorCursor(Cursor):

    def __init__(self, surf):
        Cursor.__init__(self, surf)
        #map coordinates
        self.x = 0
        self.y = 0
        self.map = None

    def update(self):
        startx = 32*Current.Game_Map.height
        self.rect.x = startx + 32*(self.x-self.y)
        self.rect.y = 32+16*(self.x+self.y) \
                      - 32*Current.Game_Map.get_h(self.x, self.y)

    def move(self, *rel):
        dx, dy = rel
        self.x = min(max(self.x+dx, 0), Current.Game_Map.width-1)
        self.y = min(max(self.y+dy, 0), Current.Game_Map.height-1)
        self.update()
