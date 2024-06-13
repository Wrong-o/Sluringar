import pygame
import random
import sys
import os
from collections import Counter

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

def load_images(directory, name):
    """Load images and flip them horizontally to face right."""
    loaded_images = []
    for i in range(1, 18):
        file_path = os.path.join(directory, f"{name}{i}.png")
        image = pygame.image.load(file_path).convert_alpha()
        image_flipped = pygame.transform.flip(image, True, False)  # Flip horizontally, not vertically
        loaded_images.append(image_flipped)
    return loaded_images

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, images, results, state=0, facing_right=True, species="sluringar"):
        self.counter = 0
        super(AnimatedSprite, self).__init__()
        self.images = images
        self.index = 0
        self.image = self.flip_image(self.images[self.index], facing_right)
        self.rect = self.image.get_rect(midbottom=position)
        self.animation_time = 0.03
        self.current_time = 0
        self.state = state
        self.facing_right = facing_right
        self.is_jumping = False
        self.vx = screen_scaler *  0.0015 # Horizontal velocity
        self.gravity = screen_scaler * 0.00025  # Gravity effect
        self.vy = 0  # Vertical velocity
        self.alive = True
        self.results = results
        self.species = species
        self.landed = False
        

    def flip_image(self, image, facing_right):
        return pygame.transform.flip(image, not facing_right, False)

    def update(self, dt):
        if self.rect.bottom >= height: 
            self.landed = True
            self.rect.bottom = height

        if self.landed == False:
            self.rect.y += self.vy
            self.vy += self.gravity 
        else:
            """Update sprite animation, position, and jump if on frame 10."""
            self.current_time += dt
            if self.current_time >= self.animation_time:
                self.current_time = 0
                old_bottom = self.rect.bottom
                old_centerx = self.rect.centerx
                self.index = (self.index + 1) % len(self.images)
                self.image = self.flip_image(self.images[self.index], self.facing_right)
                self.rect = self.image.get_rect(midbottom=(old_centerx, old_bottom))
                if self.index == 11 and self.alive:  # Trigger jump on frame 10
                    if random.random() < 0.8:
                        self.is_jumping = True
                        self.counter += 1
                        self.vy = -5  # Initial vertical velocity for the jump (negative for upwards motion)
                    else:
                        self.alive = False
                        self.results[self.species].append(self.counter)
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


class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, position, images, state=0, facing_right=True, species="sluringar"):
        super(StaticSprite, self).__init__()
        self.images = images
        self.index = 0
        self.image = self.flip_image(self.images[self.index], facing_right)
        self.rect = self.image.get_rect(midbottom=position)
        self.animation_time = 0.03
        self.current_time = 0
        self.state = state
        self.facing_right = facing_right
        self.species = species

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            old_bottom = self.rect.bottom
            old_centerx = self.rect.centerx
            self.index = (self.index + 1) % len(self.images)
            self.image = self.flip_image(self.images[self.index], self.facing_right)
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom
            self.rect.centerx = old_centerx

    def flip_image(self, image, facing_right):
        return image if facing_right else pygame.transform.flip(image, True, False)


StaticSprite()

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
        pygame.draw.line(self.screen, blue, (self.x, self.y + self.h // 2), (self.x + self.w, self.y + self.h // 2), 5)
        pygame.draw.rect(self.screen, red, (self.slider_x, self.y, self.h, self.h))
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

def draw_histogram(screen, sorted_results, species, x_mod, y_mod):
    # Calculate dimensions and positions
    bar_width = width / 160
    margin = width / 120
    max_height = height / 2
    bar_color = (0, 255, 0, 128) if species == "sluringar" else (255, 0, 255, 128)
    label_color = (255, 255, 255)
    value_label_font_size = round(height / 40)
    count_label_font_size = round(height / 40)
    max_count = max(count for value, count in sorted_results) if sorted_results else 1
    x_offset = width / x_mod
    y_offset = height / y_mod
    value_label_font = pygame.font.Font(None, value_label_font_size)
    count_label_font = pygame.font.Font(None, count_label_font_size)

    for i, (value, count) in enumerate(sorted_results):
        bar_height = int((count / max_count) * max_height)
        x = x_offset + i * (bar_width + margin)
        y = y_offset - bar_height
        pygame.draw.rect(screen, bar_color, (x, y, bar_width, bar_height))

        # Draw value labels below bars
        value_label = value_label_font.render(str(value), True, label_color)
        screen.blit(value_label, (x, y_offset + 5))

        # Draw count labels above bars
        count_label = count_label_font.render(str(count), True, label_color)
        screen.blit(count_label, (x, y - 20))

    # Add axis labels
    axis_font = pygame.font.Font(None, 24)
    x_axis_label = axis_font.render('Value', True, label_color)
    y_axis_label = axis_font.render('Count', True, label_color)

    # Draw x-axis label
    screen.blit(x_axis_label, (width // 2, height - 30))

    # Draw y-axis label rotated 90 degrees
    y_axis_label_rotated = pygame.transform.rotate(y_axis_label, 90)
    screen.blit(y_axis_label_rotated, (10, height // 2))

def exp_dist():
    paused = True
    start_button_clicked = False
    sluring_images = load_images("./img/sluring_small", "sluring")
    bluring_images = load_images("./img/bluring_small", "bluring")
    all_sprites = pygame.sprite.Group()

    # Define the Start button action
    def start_game():
        nonlocal start_button_clicked
        start_button_clicked = True

    slider_left = Slider(screen, 1, 10, width // 5 , height // 2 , 300, 40)
    slider_sluring = StaticSprite()
    slider_right = Slider(screen, 1, 10, width // 5*3 , height // 2, 300, 40)
    slider_bluring = 

    # Pause menu loop
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            slider_left.handle_event(event)
            slider_right.handle_event(event)

        screen.fill((0, 0, 0))  # Clear screen
        draw_button("Start", width // 2 - 100, height // 2 - 50, 200, 100, green, start_game)
        slider_left.draw()
        slider_right.draw()
        pygame.display.update()

        if start_button_clicked:
            paused = False  # Exit pause menu loop to resume the game

    # Load images once, reuse for all sprites


    # Variables to manage timed spawning
    num_slurings = 500  # Number of slurings to spawn
    num_bluring = 500
    sluring_spawned_count = 0
    bluring_spawned_count = 0
    last_sluring_spawn_time = pygame.time.get_ticks()
    last_bluring_spawn_time = pygame.time.get_ticks()
    sluring_spawn_interval = 5  # milliseconds
    bluring_spawn_interval = 5
    results = {"sluringar": [], "bluringar": []}
    results_found = {"sluringar": False, "bluringar": False}
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        # Spawn sprites with a delay
        if sluring_spawned_count < num_slurings and current_time - last_sluring_spawn_time >= sluring_spawn_interval:
            spawn_x = width / 25
            spawn_y = height
            jump_prob = slider_left.get_value()  
            sluring_sprite = AnimatedSprite((int(random.gauss(width / 25, width / 100)), int(random.gauss(height/19*18, height / 20))), sluring_images, results, jump_prob, species="sluringar")
            all_sprites.add(sluring_sprite)
            last_sluring_spawn_time = current_time
            sluring_spawned_count += 1

        if bluring_spawned_count < num_bluring and current_time - last_bluring_spawn_time >= bluring_spawn_interval:
            spawn_x = width / 25
            spawn_y = height
            jump_prob = slider_right.get_value()  
            bluring_sprite = AnimatedSprite((int(random.gauss(width / 25, width / 100)), int(random.gauss(height/19*18, height / 20))), bluring_images, results, jump_prob, species="bluringar")
            all_sprites.add(bluring_sprite)
            last_bluring_spawn_time = current_time
            bluring_spawned_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu() 

        dt = clock.tick(60) / 1000.0  # Get delta time and limit frame rate
        all_sprites.update(dt)
        screen.blit(bg_main_menu, (0, 0))
        all_sprites.draw(screen)

        # Check if all sprites are dead and display the frequency table
        if sluring_spawned_count == num_slurings and bluring_spawned_count == num_bluring and all(sprite.alive == False for sprite in all_sprites):
            if not results_found["sluringar"]:
                freq_table_sluringar = Counter(results["sluringar"])
                min_value_sluringar = min(results["sluringar"]) if results["sluringar"] else 0
                max_value_sluringar = max(results["sluringar"]) if results["sluringar"] else 0
                sorted_result_sluringar = [(value, freq_table_sluringar.get(value, 0)) for value in range(min_value_sluringar, max_value_sluringar + 1)]
                results_found["sluringar"] = True

            if not results_found["bluringar"]:
                freq_table_bluringar = Counter(results["bluringar"])
                min_value_bluringar = min(results["bluringar"]) if results["bluringar"] else 0
                max_value_bluringar = max(results["bluringar"]) if results["bluringar"] else 0
                sorted_result_bluringar = [(value, freq_table_bluringar.get(value, 0)) for value in range(min_value_bluringar, max_value_bluringar + 1)]
                results_found["bluringar"] = True

        # Draw histograms if results are found
        if results_found["sluringar"]:
            draw_histogram(screen, sorted_result_sluringar, "sluringar", 30, 1.2)

        if results_found["bluringar"]:
            draw_histogram(screen, sorted_result_bluringar, "bluringar", 25, 1.2)

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
                exit_action()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_action()

        screen.blit(bg_main_menu, (0, 0))
        draw_button("Exponential", width * 0.20, height / 2, 300, 100, green, exp_dist)
        draw_button("Normal", width * 0.50, height / 2, 300, 100, green, normal_action)
        draw_button("Poisson", width * 0.80, height / 2, 300, 100, green, poisson_action)
        draw_button("Exit", 50, 50, 100, 50, red, exit_action)
        pygame.display.update()

main_menu()
