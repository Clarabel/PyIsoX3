
class Tileset:
    def __init__(self, name):
        #filename in './images/tilesets/'
        self.filename = name
        #sol, bloc, autotile, decoration
        self.type = ""
        #pygame.Surface
        self.image = None
        #numer of tile
        self.number = 0
        
