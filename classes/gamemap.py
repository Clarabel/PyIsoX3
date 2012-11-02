import pygame, cache

class GameMap:

    def __init__(self, data):
        self.name = data['name']
        self.data = data['data']
        self.tilesets = data['tilesets']
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.startx = 32*self.height-32
        self.tiles = pygame.sprite.LayeredDirty()
        
    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                sprite = self.new_tile(i, j)
                
    def new_tile(self, i, j):
        x = self.startx + 32*i-32*j
        y = 16*i+16*j
        sprite = IsoTile(i, j, self.tiles)
        h = self.get_height(i, j)
        ref = self.get_tileref(i, j)
        tileset = self.get_tileset(i, j)
        tilesetname = self.tilesets[tileset]
        sprite.image = cache.load_tile(tilesetname, ref, h)
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x
        sprite.rect.bottom = y+32
        return sprite
    
    def get_tileset(self, *pos):
        x, y = pos
        return self.data[y][x][0]
    
    def set_tileset(self, t, *pos):
        x, y = pos
        prev = self.data[y][x]
        self.data[y][x] = (t, prev[1], prev[2])

    def get_tileref(self, *pos):
        x, y = pos
        return self.data[y][x][1]
    
    def set_tileref(self, ref, *pos):
        x, y = pos
        prev = self.data[y][x]
        self.data[y][x] = (prev[0], min(79, max(0, ref)), prev[2])
        
    def get_height(self, *pos):
        x, y = pos
        return self.data[y][x][2]
    get_h=get_height
    
    def set_height(self, h, *pos):
        x, y = pos
        prev = self.data[y][x]
        self.data[y][x] = (prev[0], prev[1], min(39, max(0, int(h))))
        
    def refresh_tile_at(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                tile.kill()
<<<<<<< HEAD
                break
        sprite = self.new_tile(x, y)
        return sprite
=======
                sprite = self.new_tile(x, y)
                return sprite
>>>>>>> origin/master

    def get_tile_infos(self, x, y):
        tileset = self.get_tileset(x, y)
        t_ref = self.get_tileref(x, y)
        tile_h = self.get_height(x, y)
        return (tileset, t_ref, tile_h)
        
    def set_tile_infos(self, x, y, infos):
        self.data[y][x] = infos


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

