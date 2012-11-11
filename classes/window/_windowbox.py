__all__ = ["WindowInput",
           "WindowConfirm",
           "WindowConfirm",
           "WindowChoices"]

import pygame
from pygame import Rect, Surface
import itertools
from _windowbase import Window, WindowUser
from _widget import InputText

class WindowInput(WindowUser):

    def __init__(self, text=""):
        WindowUser.__init__(self, 440, 90)
        self.create_cadre_text(text)
        self.create_valid_cancel()
    
    def create_cadre_text(self, text):
        width, height = self.contents_size
        mt = self.offsettext
        self.widget = InputText(mt, 0, text, width=width-2*mt, parent = self)
        self.widget.active = True
        
        
    def update(self, event):
        result = WindowUser.update(self, event)
        if result != None:
            pygame.event.clear()
            if result:
                return self.widget.text
            else:
                return ""
        else:
            self.widget.update(event)
            return None
    
    def draw(self, surf):
        self.widget.draw(self.contents)
        WindowUser.draw(self, surf)
        
    def loop(self, screen):
        while True:
            self.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                result = self.update(event)
                if result != None:
                    return result

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
        result = None
        while result == None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.event.post(event)
                    return False
                result = self.update(event)
            self.draw(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(30)
        return result

    
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
