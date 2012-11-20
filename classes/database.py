import numpy as np
import pickle, os, sys, re

class DataBase(object):
    "Main database"
    maps = []
    tilesets = []
    heros = []
    enemies = []
    enemysquad = []
    spells = []
    states = []
    classes = []
    items = []

    @staticmethod
    def get_all(cls):
        if cls in [DataMap]:
            return get_all_datafiles(cls)
        elif cls in [Tileset]:
            return get_unique_datafile(cls)
        
    @staticmethod
    def get_all_datafiles(cls):
        #get all files
        list_dir = os.listdir(cls.data)
        #get only choosed type
        pattern = '^%s[0-9]{3}\.pxs$'%cls.pattern
        list_type = []
        for file_ in list_dir:
            if re.match(pattern, file_):
                list_type.append(os.path.join(cls.data,file_))
        all_files = sorted(list_type)
        result = []
        for data in all_files:
            with open(data, 'r') as f:
                result.append(pickle.load(f))
        return result

    @classmethod
    def init(cls):
        if hasattr(cls, '_initialised') and cls._initialised: return
        cls._initialized = True
        #initialize maps
        cls.maps = DataMap.get_all()
        #initialize maps
        cls.tilesets = Tileset.get_all()

class GameData(object):
            
    @classmethod
    def get_all_datafiles(cls):
        #get all files
        list_dir = os.listdir(cls.data)
        #get only choosed type
        pattern = '^%s[0-9]{3}\.pxs$'%cls.pattern
        list_type = []
        for file_ in list_dir:
            if re.match(pattern, file_):
                list_type.append(os.path.join(cls.data,file_))
        all_files = sorted(list_type)
        result = []
        for data in all_files:
            with open(data, 'r') as f:
                result.append(pickle.load(f))
        return result

    @classmethod
    def get_unique_datafile(cls):
        data = os.path.join('data', cls.data)
        with open(data, 'r') as f:
            result = pickle.load(f)
        return result

    
class DataMap(GameData):
    "Data class for map"
    
    data = os.path.join('data', 'maps')
    pattern = 'map'
    
    @classmethod
    def get_all(cls):
        return cls.get_all_datafiles()
    
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
        "set size and resize all arrays"
        self._size = size
        self.tileset = np.resize(self.tileset, size)
        self.tileref = np.resize(self.tileref, size)
        self.height = np.resize(self.height, size)
    
    @property
    def w(self):
        return self.size[0]
    @w.setter
    def w(self, w):
        self.size = (w, self.size[1]) #do resize
    
    @property
    def h(self):
        return self.size[1]
    @h.setter
    def h(self, h):
        self.size = (self.size[0], h) #do resize

    def set_filename(self, filename):
        self.filename = filename
        
    def get_filename(self):
        if hasattr(self, 'filename'):
            filename = self.filename
        else:
            #map.data n'a pas enregistré de nom de fichier
            old_maps = os.listdir(DataMap.data)
            n = 0
            while 1:
                pattern = '^%s[0-9]{3}\.pxs$'%DataMap.pattern
                filename = pattern%n
                if not (filename in old_maps):
                    break
                n += 1
            self.filename = filename
        return filename

    def save(self):
        filename = os.path.join(DataMap.data, self.get_filename())
        with open(filename, 'w') as f:
            pickle.dump(self, f)
            
class Tileset(GameData):
    
    data = os.path.join('data', 'tilesets')
    pattern = 'set'
    
    @classmethod
    def get_all(cls):
        return cls.get_all_datafiles()
    
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
    

class Hero(object):
    
    data = os.path.join('data', 'heros')
    pattern = 'hero'
    pass


class Enemy(object):
    
    data = os.path.join('data', 'enemies')
    pattern = 'enemy'
    pass


class EnemySquad(object):
    
    data = os.path.join('data', 'troups')
    pattern = 'troup'
    pass


class Spell(object):
    
    data = os.path.join('data', 'spells')
    pattern = 'spell'
    pass


class State(object):
    
    data = os.path.join('data', 'states')
    pattern = 'state'
    pass


class HeroClass(object):
    
    data = os.path.join('data', 'heroclass')
    pattern = 'class'
    pass


class Item(object):
    
    data = os.path.join('data', 'items')
    pattern = 'item'
    pass

DataBase.init()
if __name__=='__main__':
##    import pickle, os, sys
    t=os.path.join('..')
    sys.path.append(t)
    os.chdir('..')
    import classes.database
##    with open("../data/maps/map001.pxs", 'r') as f:
##            data = pickle.load(f)
    
    
