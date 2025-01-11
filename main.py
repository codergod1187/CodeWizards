#Libraries
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

clock = pygame.time.Clock()
FPS = 60

moving_left = False
moving_right = False
BG = (50,50,50)
def draw_bg():
    screen.fill(BG)
#Player Class

class EthicalHacker(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale , speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation = []
        self.index = 0
        for i in range(5):
            img = pygame.image.load(f'img/{self.char_type}/Idle/0.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()  # Fixed this line
        self.rect.center = (x, y)
    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        self.rect.x += dx
        self.rect.y += dy
            
         
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip , False), self.rect)

player = EthicalHacker('player',200, 200, 2 , 5)
virus = EthicalHacker('virus',400, 200, 2 , 5)

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    player.draw()
    virus.draw()
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
