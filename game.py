import pygame
import random
import sys
import os
import enum
import math
import time
pygame.init()

# Frame rate control
base_frame_rate = 60
clock = pygame.time.Clock()

# Screen dimensions
screen_scaler = 1800
width, height = screen_scaler, screen_scaler // 2
screen = pygame.display.set_mode((int(width), int(height)))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Load and scale main menu background image
bg_main_menu = pygame.image.load('./img/main_menu.png')
bg_main_menu = pygame.transform.scale(bg_main_menu, (width, height))


def load_images(directory):
    """Load images and flip them horizontally to face right."""
    loaded_images = []
    for i in range(1, 18):
        file_path = os.path.join(directory, f"sluring{i}.png")
        image = pygame.image.load(file_path).convert_alpha()
        image_flipped = pygame.transform.flip(image, True, False)  # Flip horizontally, not vertically
        loaded_images.append(image_flipped)
    return loaded_images


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, images, state=0, facing_right=True):
        self.counter = 0
        super(AnimatedSprite, self).__init__()
        self.images = images
        self.index = 0
        self.image = self.flip_image(self.images[self.index], facing_right)
        self.rect = self.image.get_rect(midbottom=position)
        self.animation_time = 0.05
        self.current_time = 0
        self.state = state
        self.facing_right = facing_right
        self.is_jumping = False
        self.vx = screen_scaler *  0.001 # Horizontal velocity
        self.vy = 0  # Vertical velocity
        self.gravity = screen_scaler * 0.00017  # Gravity effect
        self.alive = True

    def flip_image(self, image, facing_right):
        return pygame.transform.flip(image, not facing_right, False)

    def update(self, dt):
        """Update sprite animation, position, and jump if on frame 10."""
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx
            self.index = (self.index + 1) % len(self.images)
            self.image = self.flip_image(self.images[self.index], self.facing_right)
            self.rect = self.image.get_rect(midbottom=(old_centerx, old_bottom))
            if self.index == 11 and self.alive == True:  # Trigger jump on frame 10
                if random.random() < 0.8:
                    self.is_jumping = True
                    self.counter = self.counter + 1
                    self.vy = -5  # Initial vertical velocity for the jump (negative for upwards motion)
                else:
                    self.alive = False
        if self.is_jumping:
            self.jump()

    def jump(self):
        """Handle jumping physics."""
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += self.gravity  # Apply gravity to vertical velocity

        if self.rect.bottom >= height:  
            self.rect.bottom = height
            self.is_jumping = False
            self.vy = 0  # Stop vertical motion once back on ground


        # Optionally handle moving off the screen horizontally
        if self.rect.left > width:
            self.rect.right = 0  # Wrap around to the left side


# Font for text in buttons
font = pygame.font.Font(None, int(screen_scaler // 24))

def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    text_surf = font.render(text, True, black)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)

class Slider:
    def __init__(self, screen, min_val, max_val, x, y, w, h):
        self.screen = screen
        self.min_val = min_val
        self.max_val = max_val
        self.val = min_val  # Starting value
        self.x, self.y, self.w, self.h = x, y, w, h
        self.slider_x = x + (self.val - self.min_val) / (self.max_val - self.min_val) * self.w  # Calculate initial handle position
        self.dragging = False
        self.font = pygame.font.Font(None, 36)  # Define the font

    def draw(self):
        # Draw the line
        pygame.draw.line(self.screen, blue, (self.x, self.y + self.h // 2), (self.x + self.w, self.y + self.h // 2), 5)
        # Draw the slider handle
        pygame.draw.rect(self.screen, red, (self.slider_x, self.y, self.h, self.h))
        # Draw the value text
        self.draw_value()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x < event.pos[0] < self.x + self.w and self.y < event.pos[1] < self.y + self.h:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.slider_x = max(self.x, min(event.pos[0], self.x + self.w))
            self.val = int((self.slider_x - self.x) / self.w * (self.max_val - self.min_val) + self.min_val)

    def draw_value(self):
        value_text = self.font.render(f'Value: {self.val}', True, green)
        text_rect = value_text.get_rect(center=(self.x + self.w // 2, self.y + self.h + 30))
        self.screen.blit(value_text, text_rect)

    def get_value(self):
        return self.val


def exp_dist():
    paused = True
    start_button_clicked = False

    # Define the Start button action
    def start_game():
        nonlocal start_button_clicked
        start_button_clicked = True

    slider = Slider(screen, 1, 10, width // 2 - 150, height // 2 + 50, 300, 40)

    # Pause menu loop
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            slider.handle_event(event)

        screen.fill((0, 0, 0))  # Clear screen
        draw_button("Start", width // 2 - 100, height // 2 - 50, 200, 100, green, start_game)
        slider.draw()
        pygame.display.update()

        if start_button_clicked:
            paused = False  # Exit pause menu loop to resume the game

    # Load images once, reuse for all sprites
    sluring_images = load_images("./img/sluring_small")
    all_sprites = pygame.sprite.Group()

    # Variables to manage timed spawning
    num_slurings = 100  # Number of slurings to spawn
    spawned_count = 0
    last_spawn_time = pygame.time.get_ticks()
    spawn_interval = 5  # milliseconds

    running = True
    while running:
        current_time = pygame.time.get_ticks()

        # Spawn sprites with a delay
        if spawned_count < num_slurings and current_time - last_spawn_time >= spawn_interval:
            spawn_x = width / 25
            spawn_y = height
            jump_prob = slider.get_value()  # Example of using slider value for jump probability
            sluring_sprite = AnimatedSprite((spawn_x, spawn_y), sluring_images, jump_prob)
            all_sprites.add(sluring_sprite)
            last_spawn_time = current_time
            spawned_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True  
                exp_dist()  

        dt = clock.tick(60) / 1000.0  # Get delta time and limit frame rate
        all_sprites.update(dt)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.update()





def normal_action():
    print("Normal action selected")
    # Implement the functionality for the normal distribution here

def poisson_action():
    print("Poisson action selected")
    # Implement the functionality for the poisson distribution here

def exit_action():
    pygame.quit()
    sys.exit()

def main_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg_main_menu, (0, 0))
        draw_button("Exponential", width * 0.20, height / 2, 200, 100, green, exp_dist)
        draw_button("Normal", width * 0.50, height / 2, 200, 100, green, normal_action)
        draw_button("Poisson", width * 0.80, height / 2, 200, 100, green, poisson_action)
        draw_button("Exit", 50, 50, 100, 50, red, exit_action)
        pygame.display.update()
main_menu()