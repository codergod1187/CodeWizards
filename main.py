#Libraries

import pygame

#Initialize Pygame
pygame.init()

#Variables

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)


#Image Variables

pygame_icon = pygame.image.load('img/firewall_icon.png')

#Screen

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Firewall Frenzy")
pygame.display.set_icon(pygame_icon)


#Player Class

class EthicalHacker(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/player/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()  # Fixed this line
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

player = EthicalHacker(200, 200, 3)
player2 = EthicalHacker(400, 200, 3)

run = True
while run:
    player.draw()
    player2.draw()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
