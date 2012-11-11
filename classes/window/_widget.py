import pygame
from pygame import Rect
import itertools

WLH = 40

class Widget(object):

    def __init__(self, x, y, w, h, parent=None):
        "initialise Widget at (x, y) with size = (w, h)"
        self.active = False
        self.rect = Rect(x, y, w, h)
        self.image = pygame.Surface((w, h)).convert_alpha()
        self.font = pygame.font.Font(None, 24)
        self.parent = parent
        
    def draw(self, destsurf):
        destsurf.blit(self.image, self.rect)

    def update(self, *args, **kwargs):
        pass

    
class InputText(Widget):

    def __init__(self, x, y, text="", width=None, max_carac=20, parent=None):
        self.text = text
        self.margintext = 2
        if width:
            w = width
            self.max_carac = width / 10
        else:
            w = max_carac * 10
            self.max_carac = max_carac
        h = WLH
        Widget.__init__(self, x, y, w, h, parent=parent)
        self.image.fill((0, 0, 0))
        self.draw_text()
        self.cursor_flip = itertools.cycle(i//16 for i in xrange(48))
        
    @property
    def text(self):
        return self.pretext + self.posttext
    
    @text.setter
    def text(self, value):
        self.pretext = value
        self.posttext = ""

    @property
    def index(self):
        return len(self.pretext)
    @index.setter
    def index(self, n):
        text = self.text
        if n > 0:
            self.pretext = text[:n]
            self.posttext = text[n:]
        elif n > len(text):
            self.pretext = text
            self.posttext = ""
        else:
            self.pretext = ""
            self.posttext = text
            
    def draw_text(self):
        width = self.rect.width
        self.image.fill((255,255,255), ((2,2), (width-4, WLH-4)))
        y = (WLH - self.font.get_linesize())//2
        text = self.font.render(self.text, 1, (46, 77, 106))
        self.image.blit(text, (2+self.margintext, y))

    def draw_cursor(self):
        pos = self.font.size(self.pretext)[0]
        y = (WLH - self.font.get_linesize())//2
        y0 = y + self.font.get_ascent()#self.font.get_linesize()
        y1 = WLH / 2
        mt = 2+self.margintext
        pygame.draw.line(self.image, (0,0,0), (mt+pos,y) , (mt+pos, y0))
        
    def get_pos(self, x):
        """return (n, pos) where
n is the index of the closed letter
pos the pixel position of curseur"""
        if self.text == "": return 0
        pos = 0
        n = 0
        for metric in self.font.metrics(self.text):
            (minx, maxx, miny, maxy, advance) = metric
            if pos + advance/2 < x:
                n += 1
                pos += advance
            else:
                return n
        return n

    def update(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            key = event.key
            if key == pygame.K_DELETE:
                #supprime le premier caractere de posttext"
                self.posttext = self.posttext[1:]
            elif key == pygame.K_BACKSPACE:
                #supprime le dernier caractere de pretext"
                self.pretext = self.pretext[:-1]
            elif key == pygame.K_LEFT:
                self.index -= 1
            elif key == pygame.K_RIGHT:
                self.index += 1
            else:
                self.pretext += event.dict['unicode']
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rel_pos = (event.pos[0] - self.parent.rect.x-self.parent.offset,
                       event.pos[1] - self.parent.rect.y-self.parent.offset)
            if self.rect.collidepoint(rel_pos):
                self.active = True
                self.set_cursor_at(rel_pos[0])
            else:
                self.active = False
                
    def set_cursor_at(self, x):
        text_x = x - self.rect.x - self.margintext - 2
        self.index = self.get_pos(text_x)
        
    def draw(self, destsurf):
        self.draw_text()
        if self.active and next(self.cursor_flip):
            self.draw_cursor()
        Widget.draw(self, destsurf)

        
class InputNumber(Widget):

    def __init__(self, x, y, number=0, digit=3, parent=None):
        w = digit * 10 + 2 + 12
        h = WLH
        Widget.__init__(self, x, y, w, h, parent=parent)
        self._number = number
        self.digit = digit
        self.format = "%%0%dd"%digit
        self.margintext = 2
        self.image.fill((0, 0, 0))
        self.draw_number()
        self.cursor_flip = itertools.cycle(i//16 for i in xrange(48))
    
    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, n):
        self._number = min(max(0, n), (10**self.digit-1))
            
    def draw_number(self):
        mt = 2 + self.margintext
        width = self.rect.width
        self.image.fill((114,224,114), ((2,2), (width-4, WLH-4)))
        y = (WLH - self.font.get_linesize())//2
        x = mt
        for d in self.format%(self.number):
            text = self.font.render(d, 1, (46, 77, 106))
            self.image.blit(text, (x, y))
            x += 10
        
    def update(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            key = event.key
            if key == pygame.K_KP_MINUS:
                #supprime le premier caractere de posttext"
                self.number -= 1
            elif key == pygame.K_KP_PLUS:
                #supprime le premier caractere de posttext"
                self.number += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rel_pos = (event.pos[0] - self.parent.rect.x-self.parent.offset,
                       event.pos[1] - self.parent.rect.y-self.parent.offset)
            if self.rect.collidepoint(rel_pos):
                if event.button == 4:#molette haut
                    self.number += 1
                elif event.button == 5:
                    self.number -= 1
                else:
                    self.active = True
            else:
                self.active = False
                
    def draw(self, destsurf):
        self.draw_number()
        Widget.draw(self, destsurf)

class TextBox(Widget):

    def __init__(self, x, y, w, h, text="", align='center'):
        Widget.__init__(self, x, y, w, h, parent=None)
        self.align = align
        self.background_color = (0,0,0,0)
        self.text = text

    @property    
    def align(self):
        return self._align
    @align.setter
    def align(self, align):
        "define the align option: vertical then horizontal alignement"
        ref = {'center':4,
               'centerleft':1,
               'centerright':7,
               'topleft':0,
               'topright':6,
               'topcenter':3,
               'bottomleft':2,
               'bottomright':8,
               'bottomcenter':5}
        self._align = ref.get(align, 0)
        
    @property
    def text(self):
        "text getter"
        return self.__dict__.get('_text', None)

    @text.setter
    def text(self, text):
        "change the text and redraw the box text"
        if self.text != text:
            self._text = text
            self.draw_text()
        
    def draw_text(self):
        "draw self.text on self.contents"
        render = self.font.render(self.text, 1, (46, 77, 106))
        size = render.get_size()
        v, h = self.align%3, self.align// 3
        if v == 0:
            y = 2
        elif v == 1:
            y = 2+(self.rect.h - size[1])//2
        else:
            y = self.rect.h - size[1] - 2
        if h == 0:
            x = 2
        elif h == 1:
            x = 2+(self.rect.w - size[0])//2
        else:
            x = self.rect.h - size[0] - 2
        self.image.fill(self.background_color)
        self.image.blit(render, (x, y))
