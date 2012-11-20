#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame import Rect, Surface
from cache import load_windowskin


WLH = 24                  # Window Line Height
class Window(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((width, height)).convert(32, pygame.RLEACCEL)
        self._windowskin = None
        self.rect = Rect(x, y, width, height)
        self.selected_rect = None
        self.widgets = []
        
    @property
    def offset(self):
        return 16

    @property
    def screen_pos(self):
        pos = self.rect.topleft
        return (pos[0] + self.offset, pos[1] + self.offset)
    
    @property
    def font(self):
        if not hasattr(self, '_font'):
            self._font = pygame.font.Font(None, 24)
        return self._font
    @font.setter
    def font(self, value):
        self._font = value
        
    def create_contents(self):
        w, h = self.rect.inflate(-2*self.offset, -2*self.offset).size
        self.contents = Surface((w, h)).convert_alpha()
        self.font_color = (255,255,255)

    def draw_text(self, x, y, text):
        bmp = self.font.render(text, 1, self.font_color)
        self.contents.blit(bmp, (x,y))

    def draw_selected(self, destsurf):
        if self.selected_rect:
            rect = self.selected_rect.move(self.rect.topleft)
            selected_surf = destsurf.subsurface(rect)
            pygame.transform.scale(self._select_src, self.selected_rect.size,
                                   selected_surf)
            
    @property
    def windowskin(self):
        return self._windowskin

    @windowskin.setter
    def windowskin(self, value):
        self._windowskin = value
        self._background = self._windowskin.subsurface(0,0,64,64)
        self._cadre = self._windowskin.subsurface(64,0,64,64)
        self._select_src = self._windowskin.subsurface(64,64,32,32)
        w, h = self.rect.size
        pygame.transform.scale(self._background, (w, h), self.image)
        #draw the four corners on the window
        for src, dest in [[(0, 0), (0,0)],
                     [(48, 0), (w-16, 0)],
                     [(0, 48), (0, h-16)],
                     [(48, 48), (w-16, h-16)]]:
            src_rect = Rect(src, (16, 16))
            dest_rect = Rect(dest, (16, 16))
            self.image.blit(self._cadre.subsurface(src_rect), dest)

    def draw(self, destsurf):
        destsurf.blit(self.image, self.rect)
        self.draw_selected(destsurf)
        destsurf.blit(self.contents, self.rect.move(self.offset, self.offset),
                                      self.contents_src)
        
    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.parent = self
        widget.parent_offset = self.offset

    @property
    def contents_size(self):
        width, height = self.rect.inflate(-2*self.offset, -2*self.offset).size
        return width, height
    @property
    def contents_rect(self):
        "return the visible rect of contents"
        return self.rect.inflate(-2*self.offset, -2*self.offset)
    @property
    def contents_src(self):
        return self.contents.get_rect()

    
class WindowUser(Window):
    """super class for WindowInput and WindowConfirm"""
    def __init__(self, contents_w, contents_h):
        #center the window on the screen
        screen = pygame.display.get_surface()
        screen_w, screen_h = screen.get_size()
        w, h = contents_w+32, contents_h+32
        x = (screen_w - w)//2
        y = (screen_h - h)//2
        Window.__init__(self, x, y, w, h)
        self.windowskin = load_windowskin('editor.png')
        self.create_contents()
        self.contents.fill((0,0,0,0))
        self.cancel_allowed = True
        
    def create_valid_cancel(self):
        "create Valid and Cancel buttons"
        width, height = self.contents_size
        self.valider = Surface((100, 26))
        valider = self.font.render("Valider", 1, (0,0,0))
        w, h = valider.get_size()
        self.valider.fill((35, 131, 56))
        pygame.draw.lines(self.valider, (0,0,0), 0, [(0,25),(99,25),(99,0)])
        self.valider.blit(valider, ((100-w)//2, (32-h)//2))

        self.annuler = Surface((100, 26))
        annuler = self.font.render("Annuler", 1, (0,0,0))
        w, h = annuler.get_size()
        self.annuler.fill((255, 60, 83))
        pygame.draw.lines(self.annuler, (0,0,0), 0, [(0,25),(99,25),(99,0)]) 
        self.annuler.blit(annuler, ((100-w)//2, (32-h)//2))

        self.annuler_rect = Rect(10, height-32, 100, 26)
        self.valider_rect = Rect(width-100-10, height-32, 100, 26)
        self.contents.blit(self.annuler, self.annuler_rect)
        self.contents.blit(self.valider, self.valider_rect)
    
    @property
    def offsettext(self):
        return 10

    @property
    def margintext(self):
        return 2

    def check_valid(self, event):
        if event.type == pygame.KEYDOWN and\
           event.key == pygame.K_RETURN:
            return  True #get Cancel
        elif event.type == pygame.MOUSEBUTTONDOWN and\
             event.button == 1:
            rel_pos = (event.pos[0]-self.rect.x-self.offset,
                       event.pos[1]-self.rect.y-self.offset)
            if self.valider_rect.collidepoint(rel_pos):
                #Cancel and return
                return  True

    def check_cancel(self, event):
        if event.type == pygame.QUIT:
            pygame.event.post(event)
            return  True
        elif self.cancel_allowed:
            if event.type == pygame.KEYDOWN and\
               event.key == pygame.K_ESCAPE:
                return  True #get Cancel
            elif event.type == pygame.MOUSEBUTTONDOWN and\
                 event.button == 1:
                rel_pos = (event.pos[0]-self.rect.x-self.offset,
                           event.pos[1]-self.rect.y-self.offset)
                if self.annuler_rect.collidepoint(rel_pos):
                    #Cancel and return
                    return  True
        return False

    def update(self, event):
        if self.check_cancel(event):
            return False
        elif self.check_valid(event):
            return True
        for widget in self.widgets:
            widget.update(event)
        return None
