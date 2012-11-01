
import os, sys, pygame
import menu



BUTTON_CLICK = pygame.USEREVENT+1

SCREEN_SIZE = (800, 600)

def main():
    """boucle principale"""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    background = pygame.image.load(os.path.join('images', 'splash.jpg'))
    background = background.convert()
    screen.blit(background, (0, 0))
    start_menu = menu.Menu((400,300), 'menu.jpg')
    start_menu.rect.move_ip(200, 150)
    rect = pygame.Rect(0, 0, 200, 150)
    start_button = menu.ButtonImg(rect.copy(), img='start.gif')
    start_button.set_image_over('start2.gif')
    start_menu.add(start_button)
    options_button = menu.ButtonImg(rect.copy(), img='Options.gif')
    options_button.set_image_over('Options2.gif')
    start_menu.add(options_button)
    quitter_button = menu.ButtonImg(rect.copy(), img='Quitter.gif')
    quitter_button.set_image_over('Quitter2.gif')
    start_menu.add(quitter_button)
    
    #début de la boucle principale
    continuer = True
    horloge = pygame.time.Clock()
    pygame.event.clear()
    while continuer:
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            pygame.quit()
            return
        for event in pygame.event.get():
            start_menu.update_event(event)
            if event.type == pygame.QUIT:
                continuer = False
            elif event.type == BUTTON_CLICK:
                if event.button == start_button:
                    print("C'EST PARTI !!!!!!!!!")
                elif event.button == options_button:
                    print("Rien à paramétrer")
                elif event.button == quitter_button:
                    print("Au revoir :-(")
        start_menu.update()
        start_menu.image.fill((0,255,0), pygame.Rect(100, 300, 200, 150))
        screen.blit(start_menu.image, start_menu.rect)
        pygame.display.flip()
        horloge.tick(60)
        
    pygame.quit()


if __name__ == '__main__':
    main()
    sys.exit()



