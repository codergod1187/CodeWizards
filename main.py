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

moving_left = False
moving_right = False


#Player Class

class EthicalHacker(pygame.sprite.Sprite):
    def __init__(self, x, y, scale , speed):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/player/Idle/0.png')
        self.speed = speed
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()  # Fixed this line
        self.rect.center = (x, y)
    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed
        self.rect.x += dx
        self.rect.y += dy
            
         
    def draw(self):
        screen.blit(self.image, self.rect)

player = EthicalHacker(200, 200, 2 , 5)
player2 = EthicalHacker(400, 200, 2 , 5)

run = True
while run:
    player.draw()
    player.move(moving_left,moving_right)
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True    
            if event.key == pygame.K_ESCAPE:
                run = False  

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False            
           

    pygame.display.update()

pygame.quit()

