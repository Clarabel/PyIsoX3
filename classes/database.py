import numpy as np


class Tileset(object):
    
    def __init__(self, filename):
        #filename in './images/tilesets/'
        self.filename = filename
        #name for the database
        self.name = filename.rstrip('.png')
        #sol, bloc, autotile, decoration
        self.type = 'bloc'
        #pygame.Surface
        self.image = None
        #numer of tile
        self.number = 0
        #dimension for each tile
        self.tilesize = (64, 64)
        self.tiles_per_row = 8

    @property
    def tpr(self):
        return self.tiles_per_row
    @property 
    def tile_width(self):
        return self.tilesize[0]
    tile_w=tile_width
    
    @property 
    def tile_height(self):
        return self.tilesize[0]
    tile_h=tile_height
    

class DataMap(object):
    
    def __init__(self):
        self._size = (10,10) #map size
        self.tilesets = [] #list of tilesets used
        self.tileset = np.zeros(self.size, np.int8) #tileset source for the tile
        self.tileref = np.zeros(self.size, np.int16) #ref in the tileset
        self.height = np.zeros(self.size, np.int8) #height of the square
        self.name = "New Map" #name used in editor and/or game
        
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        size = self.size
        self.tileset = np.resize(self.tileset, size)
        self.tileref = np.resize(self.tileref, size)
        self.height = np.resize(self.height, size)
    
    @property
    def w(self):
        return self.size[0]
    @w.setter
    def w(self, w):
        self.size = (w, self.size[1])
    
    @property
    def h(self):
        return self.size[1]
    @h.setter
    def h(self, h):
        self.size = (self.size[0], h)

    def set_filename(self, filename):
        self.filename = filename
        
if __name__=='__main__':
    import pickle, os, sys
    sys.path.append('..')
    with open("../data/maps/map001.pxs", 'r') as f:
            data = pickle.load(f)
    
    
