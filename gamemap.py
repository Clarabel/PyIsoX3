import pygame, cache

class GameMap:

    def __init__(self, data):
        self.name = data['name']
        self.data = data['data']
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.startx = 32*self.height

    def draw(self, map_tiles):
        for i in range(self.width):
            for j in range(self.height):
                sprite = self.new_tile(i, j, map_tiles)
                
    def new_tile(self, i, j, map_tiles):
        x = self.startx + 32*i-32*j
        y = 32+16*i+16*j
        rect = pygame.Rect(x, y, 64, 32)
        sprite = IsoTile(i, j, map_tiles)
        #map_tiles.change_layer(sprite, 2*(i+j))
        h = self.data[j][i][1]
        ref = self.data[j][i][0]
        sprite.image = cache.load_tile(ref, h)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x
        sprite.rect.bottom = y+32
        return sprite

    def get_tile(self, *pos):
        x, y = pos
        return self.data[y][x][0]
    
    def get_height(self, *pos):
        x, y = pos
        return self.data[y][x][1]
    
    def set_height(self, h, *pos):
        x, y = pos
        prev = self.data[y][x]
        ref = self.data[y][x][0]
        self.data[y][x] = (ref, h)
        print(prev, '=>', self.data[y][x])
    get_h=get_height

class IsoTile(pygame.sprite.DirtySprite):

    def __init__(self, x, y, *groups):

        self.dirty = 1
        self.blendmode = 0  # pygame 1.8, referred to as special_flags in
                            # the documentation of Surface.blit
        self._visible = 1
        self._layer = 2*(x+y)    # READ ONLY by LayeredUpdates or LayeredDirty
        self.source_rect = None
        pygame.sprite.Sprite.__init__(self, *groups)
        self.x, self.y = x, y

