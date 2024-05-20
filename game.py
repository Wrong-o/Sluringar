import pygame
import random
import sys
import os

# Pygame initialization
pygame.init()

# Frame rate control
base_frame_rate = 60
current_frame_rate = base_frame_rate
clock = pygame.time.Clock()


# Change screen scale to change size
screen_scaler = 1800
width, height = screen_scaler, screen_scaler // 2
screen = pygame.display.set_mode((int(width), int(height)))
dflt_img_sz = (screen_scaler, screen_scaler/2)
sluring_img_sz = (screen_scaler/ 25, screen_scaler/ 25)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#Images
bg_main_menu = pygame.image.load('./img/main_menu.png')
bg_main_menu = pygame.transform.scale(bg_main_menu, dflt_img_sz)

def load_images(directory, size):
    """Load and scale images from the specified directory."""
    images = []
    for i in range(1, 18):  # Assuming there are exactly four images named sluring1 to sluring4
        file_path = os.path.join(directory, f"sluring{i}.png")
        image = pygame.image.load(file_path).convert_alpha()  # Load and support transparency
        images.append(image)
        print(f"Loaded and scaled {file_path}")
    return images

    
 
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, images):
        super(AnimatedSprite, self).__init__()
        self.images = images
        self.index = 0
        self.image = images[self.index]  # Initial image
        self.rect = self.image.get_rect()
        self.animation_time = 0.05  # Time between frames
        self.current_time = 0
        # Set the initial position with an adjustment to the right
        x_adjustment = 30  # Adjust this value as needed to move sprite to the right
        self.rect.midbottom = (position[0] + x_adjustment, position[1])

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx
            self.rect = self.image.get_rect()
            self.rect.midbottom = (old_centerx, old_bottom)



# Font
font = pygame.font.Font(None, screen_scaler // 24)


def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()  # Perform an action if the button is clicked
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

def exponential_action():
    exp_dist()

def normal_action():
    normal_dist()

def poisson_action():
    pois_dist()

def exit_action():
    pygame.quit()
    sys.exit()

def escape_action():
    main_menu()

def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(bg_main_menu,(0, 0))
        
        draw_button("Exponential", width * 0.20 - width* 0.1 , height / 10 * 4, width* 0.2, height * 0.2, green, exponential_action)
        draw_button("Normal", width * 0.5 - width * 0.1, height / 10 * 4, width * 0.2 , height * 0.2, green, normal_action)
        draw_button("Poisson", width * 0.80 - width * 0.1, height / 10 * 4, width* 0.2, height * 0.2, green, poisson_action)
        draw_button("Exit", 0, 0, width* 0.2, height * 0.2, red, exit_action)
        
        pygame.display.update()


def normal_dist():
    norm = True
    while norm:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
     
        pygame.display.update()

def pois_dist():
    pois = True
    while pois:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
     
        screen.blit(bg_main_menu,(0, 0))
        pygame.display.update()

def exp_dist():
    clock = pygame.time.Clock()
    sluring_img_sz = (int(screen_scaler / 5), int(screen_scaler / 5))
    sluring_images = load_images("./img/sluring", sluring_img_sz)
    spawn_x, spawn_y = 1000, height / 9 * 8
    sluring_sprite = AnimatedSprite((spawn_x, spawn_y), sluring_images)
    all_sprites = pygame.sprite.Group(sluring_sprite)

    exp = True
    while exp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        dt = clock.tick(base_frame_rate) / 1000.0

        screen.blit(bg_main_menu, (0, 0))  # Redraw the background
        all_sprites.update(dt)
        all_sprites.draw(screen)

        pygame.display.update()

main_menu()

