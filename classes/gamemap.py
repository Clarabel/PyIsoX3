import pygame, cache

class GameMap(object):

    def __init__(self, data):
        self.data = data
        self.width, self.height = data.size
        self.startx = 32*self.height-32
        self.tiles = pygame.sprite.LayeredUpdates()
        #self.tiles = []
        self.random = False

    @property
    def name(self):
        return self.data.name
    @name.setter
    def name(self, newname):
        self.data.name = newname
    
    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, value):
        self.width, self.height = value
        print('new size', value, self.width, self.height)
        #need to resize the data array
        
    def draw_tiles(self):
        tiles = []
        for i in range(self.width):
            for j in range(self.height):
                tiles.append(self.new_tile(i, j))
        self.ordered_tiles = self.sort_tiles(tiles)
        self.tiles.add(self.ordered_tiles)
        
    def sort_tiles(self, tiles):
        z = lambda sp:sp.x + sp.y
        h = lambda sp:self.get_h(sp.x, sp.y)
        layer = lambda sp:(z(sp), h(sp))
        ordered_tiles = sorted(tiles, key=layer)
        l = 0
        last_zh = (0, 0)
        for sp in ordered_tiles:
            if last_zh < layer(sp):
                l += 16
                last_zh = layer(sp)
            sp._layer = l
        return ordered_tiles
    
    def new_tile(self, i, j):
        sprite = IsoTile(i, j)
        #debug/test
        import random
        if self.random:
            self.set_tileref(random.randint(0, 15), i, j)
        h = self.get_height(i, j)
        ref = self.get_tileref(i, j)
        tileset = self.get_tileset(i, j)
        tilesetname = self.tilesetname(tileset)
        x = self.startx + 32*i-32*j
        y = 16*i+16*j
        sprite.draw_image(tilesetname, ref, h, x, y)
        return sprite

    def tilesetname(self, tileset):
        return self.data.tilesets[tileset]
    
    def get_tileset(self, x, y):
        "return tileset indice for the tileset used at (x, y)"
        return self.data.tileset[x, y]
        
    def set_tileset(self, t, x, y, refresh=True):
        """set the tileset t for the square (x, y)
if refresh=True the tile is redrawned"""
        self.data.tileset[x, y] = t
        if refresh: self.refresh_tile_at(x, y)

    def get_tileref(self, x, y):
        "return the tileref for square (x, y)"
        return self.data.tileref[x, y]
    
    def set_tileref(self, ref, x, y, refresh=True):
        """set the tileref ref for the square (x, y)
if refresh=True the tile is redrawned"""
        self.data.tileref[x, y] = min(max(0, ref), 79)
        if refresh: self.refresh_tile_at(x, y)
        
    def get_height(self, x, y):
        "return the height at (x, y)"
        return self.data.height[x, y]
    get_h=get_height
    
    def set_height(self, h, x, y, refresh=True):
        """set the height h for the square (x, y)
if refresh=True the tile is redrawned"""
        self.data.height[x, y] = min(max(0, int(h)), 39)
        if refresh: self.refresh_tile_at(x, y)
        
    def get_tile_at(self, x, y):
        "return tile drawing the square (x, y)"
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
            
    def refresh_tile_at(self, x, y):
        "refresh the tile at (x, y)"
        tile = self.get_tile_at(x, y)
        tile.kill()
        tile = self.new_tile(x, y)
        tiles = self.tiles.sprites()
        tiles.append(tile)
        ordered_tiles = self.sort_tiles(tiles)
        self.tiles.empty()
        self.tiles.add(ordered_tiles)

    def get_tile_infos(self, x, y):
        "return a tuple (tileset, tileref, h)"
        tileset = self.get_tileset(x, y)
        t_ref = self.get_tileref(x, y)
        tile_h = self.get_height(x, y)
        return (tileset, t_ref, tile_h)
        
    def set_tile_infos(self, x, y, tileset=None, tileref=None, h=None):
        "Update the tile set, the ref and the height for the square (x, y)"
        if h!=None: self.set_height(h, x, y, False)
        if tileref!=None: self.set_tileref(tileref, x, y, False)
        if tileset!=None: self.set_tileset(tileset, x, y, False)
        self.refresh_tile_at(x, y)

    def mouse_square(self, x, y):
        """return the coordinates (i, j) the square below the screen pos (x, y)
        return None if no square are found"""
        for h in range(39, -1, -1):
            y0 = y + 8*h
            i = (x - 32 - self.startx + 2*y0) / 64.0
            j = (y0 - 16*i) / 16
            i, j = int(i), int(j)
            if 0<=i<self.width and 0<=j<self.height and\
               h == self.get_h(i, j):
                return i, j
        return None
    
class IsoTile(pygame.sprite.DirtySprite):

    def __init__(self, x, y):

        self.dirty = 1
        self.blendmode = 0  # pygame 1.8, referred to as special_flags in
                            # the documentation of Surface.blit
        self._visible = 1
        self._layer = 0    # READ ONLY by LayeredUpdates or LayeredDirty
        self.source_rect = None
        pygame.sprite.Sprite.__init__(self, )
        self.x, self.y = x, y

    @property
    def real_pos(self):
        return 16*self.x+16*self.y

    def draw_image(self, tilesetname, ref, h, x, y):
        self.image = cache.load_tile(tilesetname, ref, h)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y+32

