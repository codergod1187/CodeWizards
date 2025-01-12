import pygame
import button
import csv
import pickle

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor for Firewall Frenzy')

# Game Variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 12
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1 

# Load Images
Background = pygame.image.load('img/Level Editor/background.png')
Building = pygame.image.load('img/Level Editor/buildings.png')


# List for Tiles
tiles_list = []
for x in range(TILE_TYPES):
    imgs = pygame.image.load(f'img/Tiles/{x}.png')
    imgs = pygame.transform.scale(imgs, (TILE_SIZE, TILE_SIZE))
    tiles_list.append(imgs)

save_img = pygame.image.load('img/Buttons/Save_Button.png').convert_alpha()
load_img = pygame.image.load('img/Buttons/Load_Button.png').convert_alpha()

# Scale the images once
scaled_bg = pygame.transform.scale(Background, (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
scaled_building = pygame.transform.scale(Building, (SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN))

# Define Colors
GREEN = (170, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


# Define Font
font = pygame.font.SysFont('Futura', 30)
# Function for Text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# Create Function for Drawing the Background
def draw_bg():
    screen.fill(GREEN)
    width = scaled_bg.get_width()
    for x in range(2):
        screen.blit(scaled_bg, ((x * width) - scroll, 0))  # Draw background at (0,0)
        screen.blit(scaled_building, ((x * width) - scroll, 0))  # Position building at the top of the screen

# Grid Function
def draw_grid():
    # Vertical Lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # Horizontal Lines
for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tiles_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# Create Buttons

save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)




# Buttons
button_list = []
button_col = 0
button_row = 0
for i in range(len(tiles_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, tiles_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0
run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or Down to change the level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN -50)

    # Save and Load 
    if save_button.draw(screen):
        # Save level data
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):  # Check if the load button is pressed
        scroll = 0
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile) 

        
    save_button.draw(screen)
    load_button.draw(screen)

    # Tile Panel 
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))


    # Tiles
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # Selected Tile Highlighted
    pygame.draw.rect(screen, RED, button_list[current_tile])


    # Scroll the background
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed 
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # Adding new tiles to screen
    # Get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # Check if cordinates are within tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # Update Tile Value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile 

        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Keyboard Presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
