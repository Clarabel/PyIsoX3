__all__ = ["WindowInput", "WindowConfirm", "WindowConfirm", "WindowChoices"]

import pygame
from pygame import Rect, Surface
import itertools
from cache import load_windowskin

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
    def contents_size(self):
        width, height = self.rect.inflate(-2*self.offset, -2*self.offset).size
        return width, height
    @property
    def contents_rect(self):
        return self.rect.inflate(-2*self.offset, -2*self.offset)
    
    @property
    def offsettext(self):
        return 10

    @property
    def margintext(self):
        return 2
    
class WindowInput(WindowUser):

    def __init__(self, text=""):
        WindowUser.__init__(self, 440, 90)
        self.create_cadre_text()
        self.pretext = text
        self.posttext = ""
        self.draw_text()
        self.create_valid_cancel()
        
    @property
    def text(self):
        return self.pretext + self.posttext
    
    @text.setter
    def text(self, value):
        self.pretext = value
        self.posttext = ""

    def create_cadre_text(self):
        width, height = self.contents_size
        mt = self.offsettext
        self.contents.fill((0,0,0), ((mt,10), (width-2*mt, 40)))
        self.cadre_rect = Rect((mt,10), (200, 40))

    def draw_text(self):
        width, height = self.contents_size
        mt = self.offsettext
        self.contents.fill((255,255,255), ((mt+2,12), (width-2*mt-4, 36)))
        y = 34 - self.font.get_linesize()
        text = self.font.render(self.text, 1, (46, 77, 106))
        self.contents.blit(text, (mt+2+self.margintext, 10+y))
        
    def get_pos(self, x):
        """return (n, pos) where
n is the index of the closed letter
pos the pixel position of curseur"""
        if self.text == "": return 0, 0
        pos = 0
        n = 0
        for metric in self.font.metrics(self.text):
            (minx, maxx, miny, maxy, advance) = metric
            if pos + advance/2 < x:
                n += 1
                pos += advance
            else:
                return n, pos
        return n, pos
        
    def main(self):
        screen = pygame.display.get_surface()
        last_text = None
        n, pos = self.get_pos(1000)
        pos = None
        continuer = True
        cursor_flip = itertools.cycle([0,0,0,0,0,0,0,0,0,0,
                             1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
        while continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    self.text = ""
                    pygame.event.post(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #like Cancel, return ""
                        continuer = False
                        self.text = ""
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        #like Valid, return self.text
                        continuer = False
                    elif event.key == pygame.K_DELETE:
                        #supprime le premier caractere de posttext"
                        self.posttext = self.posttext[1:]
                    elif event.key == pygame.K_BACKSPACE:
                        #supprime le dernier caractere de pretext"
                        self.pretext = self.pretext[:-1]
                    elif event.key == pygame.K_LEFT:
                        if self.pretext:
                            self.pretext, l = self.pretext[:-1], self.pretext[-1]
                            self.posttext = l + self.posttext
                    elif event.key == pygame.K_RIGHT:
                        if self.posttext:
                            self.posttext, l = self.posttext[1:], self.posttext[0]
                            self.pretext = self.pretext + l
                        
                    else:
                        self.pretext += event.dict['unicode']
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        rel_pos = (event.pos[0]-self.rect.x-self.offset,
                                   event.pos[1]-self.rect.y-self.offset)                                       
                        if self.valider_rect.collidepoint(rel_pos):
                            #Valid, return self.text
                            continuer = False
                        elif self.annuler_rect.collidepoint(rel_pos):
                            #Cancel and return empty self.text
                            continuer = False
                            self.text = ""
                        elif self.cadre_rect.collidepoint(rel_pos):
                            #set cursor at mouse pos
                            x = rel_pos[0] - self.offsettext - 2-self.margintext
                            n, pos = self.get_pos(x)
                            pos = None
                            text = self.text
                            self.pretext, self.posttext = text[:n], text[n:]
            if 1 or last_text != self.text or pos == None:
                last_text = self.text
                last_pos = pos
                self.draw_text()
                pos = self.font.size(self.pretext)[0]
                y0 = 10+34 - self.font.get_linesize()
                y1 = 10+34
            if next(cursor_flip):
                mt = self.offsettext+2+self.margintext
                pygame.draw.line(self.contents, (0,0,0),
                             (mt+pos,y0) , (mt+pos, y1))
            self.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return self.text

class WindowConfirm(WindowUser):

    def __init__(self, text):
        WindowUser.__init__(self, 240, 90)
        self.create_valid_cancel()
        self.draw_text(text)
        
    def draw_text(self, text):
        width, height = self.contents_size
        mt = self.offsettext
        y = 34 - self.font.get_linesize()
        text_rd = self.font.render(text, 1, (46, 77, 106))
        self.contents.blit(text_rd, (mt+2+self.margintext, 10+y))
        self.create_valid_cancel()

    def loop(self):
        screen = pygame.display.get_surface()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.event.post(event)
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #like Cancel, return 
                        return  False
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        #like Valid, return 
                        return  True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        rel_pos = (event.pos[0]-self.rect.x-self.offset,
                                   event.pos[1]-self.rect.y-self.offset)                                       
                        if self.valider_rect.collidepoint(rel_pos):
                            #Valid, return 
                            return  True
                        elif self.annuler_rect.collidepoint(rel_pos):
                            #Cancel and return 
                            return  False

            self.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)


class WindowChoices(WindowUser):

    def __init__(self, choices, cancel_allowed=False):
        texts, max_leng = self.create_buttons(choices)
        w = max(240, max_leng + 2*self.offsettext)
        h = len(choices)*40+2*10
        WindowUser.__init__(self, w, h)
        self.draw_buttons(texts)
        self.cancel_allowed = cancel_allowed
        self.index = 0
        
    def draw_buttons(self, texts):
        y = 10+(40-self.font.get_linesize())/2
        width, height = self.contents_size
        for text in texts:
            w = text.get_width()
            x = (width - w)/2
            self.contents.blit(text, (x, y))
            y += 40
        
    def create_buttons(self, choices):
        text_list = []
        leng = 0
        for item in choices:
            text = self.font.render(item, 1, (46, 77, 106))
            leng = max(text.get_width(), leng)
            text_list.append(text)
        return text_list, leng

    def set_index(self, event):
        if self.contents_rect.inflate(0, -2*10).collidepoint(event.pos):
            y = event.pos[1]-self.rect.y - 10 - self.offset
            self.index = y // 40
            
    def loop(self):
        "return the index the selected choice, return None if canceled"
        
        screen = pygame.display.get_surface()
        self.selected_rect = Rect(self.offset, 10+self.offset, self.contents_rect.width, 40)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.event.post(event)
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.cancel_allowed:
                        #like Cancel, return 
                        return  None
                elif event.type == pygame.MOUSEBUTTONDOWN and\
                     self.contents_rect.collidepoint(event.pos) and\
                     event.button == 1:
                        y = event.pos[1]-self.rect.y-self.offset - 10
                        choice = y // 40
                        return choice
                elif event.type == pygame.MOUSEMOTION and\
                     self.contents_rect.collidepoint(event.pos):
                    self.set_index(event)
            self.selected_rect.y = self.index*40+10+self.offset
            self.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
