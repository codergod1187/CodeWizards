import pygame

# Initialize Pygame
pygame.init()

# Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor for Firewall Frenzy')


# Game Variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1 


# Load Images
Background = pygame.image.load('img/Level Editor/background.png')
Building = pygame.image.load('img/Level Editor/buildings.png')

# Scale the images once
scaled_bg = pygame.transform.scale(Background, (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
scaled_building = pygame.transform.scale(Building, (SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN))

# Define Colors
GREEN = (170, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Create Function for Drawing the Background
def draw_bg():
    screen.fill(GREEN)
    width = scaled_bg.get_width()
    for x in range(4):
        screen.blit(scaled_bg, ((x * width) - scroll, 0))  # Draw background at (0,0)
        screen.blit(scaled_building, ((x * width) - scroll, 0))  # Position building at the top of the screen

run = True
while run:
    draw_bg()
    # Scroll the background
    if scroll_left == True and scroll > 0:
        scroll -= 5
    if scroll_right == True:
        scroll += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Keyboard Presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False

    pygame.display.update()

pygame.quit()