import os, pygame
import cache

pygame.font.init()
MENU_FONT = pygame.font.SysFont("arial.ttf",12)
BUTTON_CLICK = pygame.USEREVENT+1

class Menu:

    def __init__(self, size, img):
        self.size = size
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.sprite = pygame.sprite.Sprite()
        self.buttons = []
        self.set_image(img)
        
    def set_image(self, img):
        self.image = cache.load(img)
                
    def add(self, button):
        self.buttons.append(button)
        button.rect.topleft = (100, 70*len(self.buttons))
        button.rect.move_ip(self.rect.topleft)

    def update_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            result = pygame.event.Event(pygame.QUIT, {})
            pygame.event.post(result)
        for button in self.buttons:
            button.update_event(event)
            
    def update(self):
        for button in self.buttons:
            button.update()
            self.image.blit(button.image,
                            button.rect.move(-self.rect.x, -self.rect.y))
            
        
class ButtonImg(pygame.sprite.Sprite):

    def __init__(self, rect, img=''):
        self.rect = rect
        pygame.sprite.Sprite.__init__(self)
        self.draw_image(img)
        self.default_image = self.image
        self.image_over = None
        
    def draw_image(self, img):
        self.image = cache.load(img)
        self.rect.size = self.image.get_size()
        
    def set_image_over(self, img):
        self.image_over = cache.load(img)
        
    def update_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and\
           self.rect.collidepoint(event.pos):
            result = pygame.event.Event(BUTTON_CLICK, {'button':self})
            pygame.event.post(result)

    def update(self):
        if self.image_over:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.image = self.image_over
            else:
                self.image = self.default_image

class ButtonText(pygame.sprite.Sprite):

    def __init__(self, rect, text=''):
        self.text = text
        self.rect = rect
        pygame.sprite.Sprite.__init__(self)
        self.draw_image(text)
        
    def draw_image(self):
        w, h = 128, 64
        self.image = pygame.Surface((w, h))
        text_bmp = MENU_FONT.render(self.text, 1, (255,255,255))
        text_h = text_bmp.get_height()
        text_w = text_bmp.get_width()
        x = (w-text_w)//2
        y = (h-text_h)//2
        self.image.blit(text_bmp, (x, y))


