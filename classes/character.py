#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import cache
import Current
from itertools import cycle
import time
class Character:
    FRAME_PER_ANIM = 4
    
    def __init__(self):
        self.x = 0
        self.y = 0
        #real position on the map
        self.real_x = 16 * self.x
        self.real_y = 16 * self.y
        self.moving_h = None
        self.name = ""
        self.pattern = 1
        #crée la boucle des animations walk
        self.walk = cycle([0, 1, 2, 3, 4, 3, 2, 1])
        self.priority_type = 8
        self.direction = 1
        self.walk_anime = True
        self.step_anime = False
        self.anim_count = 1
        self.anim_speed = 1
        self.dirty = 2
        self.last_x, self.last_y = self.x, self.y
        
    @property
    def pos(self):
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, value):
        self, x, self, y = value

    @property
    def screen_x(self):
        "Get Screen X-Coordinates"
        return 2*(self.real_x-self.real_y) + Current.Game_Map.startx
        
    @property
    def screen_y(self):
        "Get Screen Y-Coordinates"
        return (self.real_x+self.real_y) - self.real_h

    @property
    def real_h(self):
        if self.moving_h != None: return self.moving_h
        return 8 * Current.Game_Map.get_h(self.x, self.y)
    
    @property
    def screen_layer(self):
        "Get Screen layer"
        x = ((self.real_x + 15)//16)
        y = ((self.real_y + 15)//16)
        tile = Current.Game_Map.get_tile_at(x, y)
        layer = tile._layer + self.priority_type
        tile_h = Current.Game_Map.get_h(x, y)
        h = self.real_h
        #if character is on the top tile
        if self.real_h // 8 < tile_h:
            layer -= 16
        return layer
    screen_z=screen_layer
    def create_sprite(self, filename):
        self.name = filename
        self.sprite = pygame.sprite.DirtySprite()
        self.sprite_img = cache.load_character(self.name)
        self.sprite.image = self.sprite_img
        self.sprite.source_rect = pygame.Rect(0, 0, 32, 40)
        self.sprite.rect = pygame.Rect(100, 100, 32, 40)
        
    def move(self, dx, dy):
        #no new move until finish
        if self.moving(): return
        self.direction = self.get_dir(dx, dy)
        self.start_move(dx, dy)
        

    def start_move(self, dx, dy, max_frame=20):
        if (dx, dy) == (0, 0): return
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            dx *= 2
            dy *= 2
        elif pygame.key.get_pressed()[pygame.K_LCTRL]:
            dx *= 3
            dy *= 3
        if not self.passable(dx, dy): return
        dist = max(abs(dx), abs(dy))
        #number of frame for animation
        f = max_frame * dist
        #sx, sy, sh = start Coordinates
        #dx, dy, dh = movement vector
        #fx, fy, fh = final Coordinates        
        sx, sy, sh = self.x, self.y, Current.Game_Map.get_h(self.x, self.y)
        self.x += dx
        self.y += dy
        fx, fy, fh = self.x, self.y, Current.Game_Map.get_h(self.x, self.y)
        dh = fh - sh
        #function for jump
        vx = 16*dx #real dx
        vy = 16*dy #real dy
        #tile's width
        sp_width = 64#self.sprite.source_rect.width
        #real width of the the character sprite
        clip_width = 18
        self.anim_count = 10000
        if dist == 1 and dh == 0:
            self.anim_speed = 1.0
            L = lambda i:0
        else:
            #points de contrôle
            vu = (dx//dist, dy//dist)#(1,0) or (0,1)
            #width of the sprite
            sp_w = f/(2*dist)*(sp_width-clip_width)/(2*sp_width)
            squares = []
            for i in range(dist+1):
                squares.append((sx+i*vu[0], sy+i*vu[1]))
            #peeks to control
            peeks = []
            for i in range(1, dist+1):
                [sq0, sq1] = squares[i-1:i+1]
                [h0, h1] = map(lambda pos: Current.Game_Map.get_h(pos[0], pos[1]), [sq0, sq1])
                #first peek
                m0 = (2*i-1)*f/(2*dist)- sp_w
                m1 = (2*i-1)*f/(2*dist)+ sp_w
                h1 = 8*max(h0-sh, h1-sh, min(1, fh-sh+1))
                peeks += [(m0, h1), (m1, h1)]
            L = lambda t: t*(h*f*(f-t) + 8*dh*m*(t-m))/(m*f*(f-m))
            m, h = f//2, 0
            for m1, h1 in peeks:
                while L(m1) < h1:
                    h += 1
            
            #g = 9.8 m/s²
            g = 9.8 * 16/(30**2)
            liste_g = []
            a=(L(2.0)-L(0.0))/2-(L(1.0)-L(0.0))
            if a > -g/2.0:
                for nf in range(f,0,-1):
                    nm=nf/2.0
                    P= lambda t: t*(h*nf*(nf-t) + 8*dh*nm*(t-nm))/(nm*nf*(nf-nm))
                    a=(P(2.0)-P(0.0))/2-(P(1.0)-P(0.0))
                    liste_g.append((a > -g/2.0, ("f=%s"%f,a,-g/2.0)))
                    if a < -g/2.0:
                        f, m = nf, nm
                        break
        self.move_path = iter((16*sx+i*vx//f,#real_x
                               16*sy+i*vy//f,#real_y
                               8*sh+L(i))\
                              for i in xrange(1,f+1))
        
    def passable(self, dx, dy):
        if (self.x + dx >= Current.Game_Map.width) or self.x + dx < 0:
            return False
        elif self.y + dy >= Current.Game_Map.height or self.y + dy < 0:
            return False
        return True
        
    def update_move(self):
        try:
            self.real_x, self.real_y, self.moving_h = next(self.move_path)
        except StopIteration:
            self.moving_h = None
            self.anim_speed = 1
            
    def moving(self):
        return (self.real_x != 16*self.x) or (self.real_y != 16*self.y)
    
    def get_dir(self, dx, dy):
        if dx > 0: return 3
        elif dx < 0: return 7
        elif dy > 0: return 1
        else: return 9
        
    def update(self):
        self.update_position()
        self.update_animation()
            
    def update_position(self):
        if self.moving():
            self.update_move()
        else:
            self.anim_speed = 1
            self.moving_h = None
        self.sprite.rect.topleft = (self.screen_x, self.screen_y)
        self.sprite.rect.move_ip((64 - self.sprite.source_rect.width)//2,
                                 -16,)
        
    def update_animation(self):
        self.anim_count += 1
        if self.anim_count > Character.FRAME_PER_ANIM/self.anim_speed:
            self.anim_count = 0
            pattern =  next(self.walk)
            x = pattern * self.sprite.source_rect.width
            y = self.sprite.source_rect.height * self.lineofdir(self.direction)
            self.sprite.source_rect.topleft = (x, y)
            
    def lineofdir(self, direction):
        "direction=1,3,7,9 => 0,1,2,3"
        return [0, 0, 0, 1, 0, 0, 0, 2, 0, 3][direction]
    
