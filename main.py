# Libraries
import pygame

# Initialize Pygame
pygame.init()

# Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Image Variables
pygame_icon = pygame.image.load('img/firewall_icon.png')

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Firewall Frenzy")
pygame.display.set_icon(pygame_icon)

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.1
TILE_SIZE = 32

moving_left = False
moving_right = False
shoot = False

bullet_img = pygame.image.load('img/bullet.png').convert_alpha()
shield_box_img = pygame.image.load('img/Collectables/Shield.png').convert_alpha()
key_box_img = pygame.image.load('img/Collectables/Key.png').convert_alpha()
speed_box_img = pygame.image.load('img/Collectables/Speed.png').convert_alpha()

item_boxes = {
    'Shield': shield_box_img,
    'Key': key_box_img,
    'Speed': speed_box_img
}

BG = (50, 50, 50)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

# Player Class
class EthicalHacker(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.base_speed = speed  # Store the base speed for resetting after boost
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = 100
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.speed_boost_steps = 0  # Tracks remaining speed boost increments

        img = pygame.image.load(f'img/{self.char_type}/Idle/0.png').convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.animation_list.append(img)

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        if char_type == 'virus':
            virus_group.add(self)

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
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

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.2 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        self.image = self.animation_list[self.frame_index]

    def check_alive(self):
        if self.health <= 0 and self.char_type == "player":
            draw_bg()
            self.health = 0
            self.speed = 0
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Item Box Class
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Speed':
                # Gradual speed boost: increase speed by 0.5 every 100ms for 5 seconds
                pygame.time.set_timer(pygame.USEREVENT + 1, 100)  # Trigger every 100ms
                player.speed_boost_steps = 10  # Total increments (5 seconds total)

# Bullet Class
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
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()

        if pygame.sprite.spritecollide(virus, bullet_group, False):
            if virus.alive:
                virus.health -= 25
                self.kill()

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Groups
bullet_group = pygame.sprite.Group()
virus_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

# Item Boxes
item_box = ItemBox('Shield', 100, 268)
item_box_group.add(item_box)
item_box = ItemBox('Key', 400, 268)
item_box_group.add(item_box)
item_box = ItemBox('Speed', 500, 268)
item_box_group.add(item_box)

# Player and Virus
player = EthicalHacker('player', 200, 200, 2, 5, 50)
virus = EthicalHacker('virus', 400, 200, 2, 5, 0)

# Main Game Loop
run = True
while run:
    clock.tick(FPS)

    draw_bg()

    player.update()
    bullet_group.update()
    item_box_group.update()
    player.draw()
    bullet_group.draw(screen)
    virus.draw()
    item_box_group.draw(screen)

    for bullet in bullet_group:
        bullet.draw(screen)

    if player.alive:
        if shoot:
            player.shoot()
        player.move(moving_left, moving_right)

    # Check for player-virus collision
    collided_viruses = pygame.sprite.spritecollide(player, virus_group, False)
    if collided_viruses:
        if player.alive:
            player.health -= 100
            if player.health <= 0:
                player.health = 0
                player.alive = False

    # Event handling
    for event in pygame.event.get():
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
        if event.type == pygame.USEREVENT + 1:
            # Gradually increase speed
            if player.speed_boost_steps > 0:
                player.speed += 0.5  # Increment speed slowly
                player.speed_boost_steps -= 1
            else:
                # Reset the timer when the boost is complete
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                player.speed = player.base_speed  # Reset to base speed

    pygame.display.update()

pygame.quit()
