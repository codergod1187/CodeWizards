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

GRAVITY = 0.75


moving_left = False
moving_right = False
shoot = False

bullet_img = pygame.image.load('img/bullet.png').convert_alpha()


BG = (50,50,50)
RED = (255,0,0)
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen,RED,(0,300),(SCREEN_WIDTH,300)) 
#Player Class

class EthicalHacker(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale , speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
        img = pygame.image.load(f'img/{self.char_type}/Idle/0.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.animation_list.append(img)
        
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()  
        self.rect.center = (x, y)
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
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
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False 
            self.in_air = True
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y 

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        self.rect.x += dx
        self.rect.y += dy
    def update(self):
        self.update_animation()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    def shoot(self):
        if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
                bullet_group.add(bullet)
    def update_animation(self):

        ANIMATION_COOLDOWN = 100
        
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        self.image = self.animation_list[self.frame_index]        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip , False), self.rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img       
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.flip = direction < 0
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.x <0 or self.rect.x > SCREEN_WIDTH:
            self.kill()  
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image, self.flip , False), self.rect)
bullet_group = pygame.sprite.Group()

player = EthicalHacker('player',200, 200, 2 , 5)
virus = EthicalHacker('virus',400, 200, 2 , 5)

run = True
while run:
    clock.tick(FPS)

    draw_bg()

    player.draw()

    player.update()

    virus.draw()

    bullet_group.update()
    for bullet in bullet_group:
        bullet.draw(screen)
    if player.alive :
        if shoot:
            player.shoot()
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
            if event.key == pygame.K_SPACE:
                shoot = True 
            if event.key == pygame.K_w and player.alive:
                player.jump = True 
            if event.key == pygame.K_ESCAPE:
                run = False  
            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False       
            if event.key == pygame.K_SPACE:
                shoot = False     
           

    pygame.display.update()

pygame.quit()
