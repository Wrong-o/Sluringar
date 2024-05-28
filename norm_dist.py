import pygame
import random
import sys

# Pygame initialization
pygame.init()

# Frame rate control
base_frame_rate = 60  # Normal frame rate
current_frame_rate = base_frame_rate

# Screen dimensions
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)  # Color for the finish line and text
green = (0, 255, 0)  # Color for the bars

# Points
mid_x, mid_y = width // 2, height // 10
# Define all decision points based on height fractions
decision_points = [height * i // 10 for i in range(1, 10)]  # Decision points at 1/10 to 9/10 of the height
finish_line_y = decision_points[-1]  # The last decision point as the finish line

# Finish line points for actors to cross
finish_line_points = [width * (i-1) // 10 for i in range(1, 11)]
finish_counters = [0] * 10  # Counter for each finish line point

# Actor settings
actors = []
spawn_interval = 200  # milliseconds (100 ms = 0.1 seconds)
last_spawn_time = 0

# Load the actor image
actor_image_path = '/home/jayb/Desktop/Scripts/simulationer/img/sluring1.png'
actor_image = pygame.image.load(actor_image_path)
# Optionally, scale the image
actor_image = pygame.transform.scale(actor_image, (50, 50))  # You can adjust the size as needed


# Clock to control the frame rate
clock = pygame.time.Clock()

def spawn_actor(current_time):
    global last_spawn_time
    if current_time - last_spawn_time >= spawn_interval:
        actor = {'x': mid_x, 'y': 0, 'direction': random.choice([-1, 1]), 'finished_at': 0}
        # Initialize flags for each decision point
        for i in range(len(decision_points)):
            actor[f'reached_point_{i}'] = False
        actors.append(actor)
        last_spawn_time = current_time

def move_actors():
    current_time = pygame.time.get_ticks()
    to_remove = []
    for actor in actors:
        if actor['finished_at'] and current_time - actor['finished_at'] > 50:
            to_remove.append(actor)
            continue
        for i, point_y in enumerate(decision_points):
            if actor['y'] < point_y:
                # Move actor to the next decision point
                actor['x'] += actor['direction']
                actor['y'] += 1
                break
            elif not actor[f'reached_point_{i}']:
                # Decide at this decision point
                actor[f'reached_point_{i}'] = True
                if random.choice([True, False]):
                    actor['direction'] *= -1
            if i == len(decision_points) - 1 and actor['y'] == finish_line_y and not actor['finished_at']:
                actor['finished_at'] = current_time
                update_finish_counters(actor['x'])

    for actor in to_remove:
        actors.remove(actor)


def update_finish_counters(x_pos):
    # Determine the nearest finish line point
    nearest_point_index = min(range(len(finish_line_points)), key=lambda i: abs(finish_line_points[i] - x_pos))
    finish_counters[nearest_point_index] += 1


def draw_actors():
    for actor in actors:
        image_rect = actor_image.get_rect(center=(int(actor['x']), int(actor['y'])))
        screen.blit(actor_image, image_rect)

def draw_finish_line():
    # Draw a finish line at the last decision point
    pygame.draw.line(screen, red, (0, finish_line_y), (width, finish_line_y), 5)

def display_finish_counts():
    font = pygame.font.Font(None, 24)
    total_finishers = sum(finish_counters)
    bar_height = 800  # Maximum height for the bars
    bar_width = 23  # Width for each bar
    base_x = 48  # Starting x-coordinate for the bars
    base_y = 543  # Y-coordinate for the bottom of all bars

    # Display total at the finish line
    total_text = font.render(f'Total at the finish line: {total_finishers}', True, red)
    screen.blit(total_text, (base_x, base_y + 10))  # Display above the bars

    for i, count in enumerate(finish_counters):
        percentage = count / total_finishers if total_finishers > 0 else 0
        scaled_bar_height = percentage * bar_height  # Scale the bar height by the percentage
        label = font.render(f'P{i+1}: {count}', True, red)

        # Calculate x position for each bar based on its index
        bar_x = base_x + i * (bar_width + 97)  # Each bar is 40 units apart

        # Draw label above each bar
        screen.blit(label, (bar_x, base_y + 30))

        # Calculate the top y-coordinate of the bar to make it grow upwards
        bar_top_y = base_y - scaled_bar_height

        # Draw horizontal bar
        pygame.draw.rect(screen, green, (bar_x, bar_top_y, bar_width, scaled_bar_height))

# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    spawn_actor(current_time)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Double the frame rate to speed up the game
                if current_frame_rate == base_frame_rate:
                    current_frame_rate *= 5
                else:
                    current_frame_rate = base_frame_rate  # Reset to normal on second press

    screen.fill(black)
    draw_finish_line()
    display_finish_counts()
    move_actors()
    draw_actors()

    pygame.display.flip()
    clock.tick(current_frame_rate)  # Use dynamic frame rate

pygame.quit()
sys.exit()

