import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_ACTORS = 50
ACTOR_SIZE = 10
SIMULATION_TIME = 10000  # 10 seconds in milliseconds
FPS = 60
DIRECTION_CHANGE_TIME = 1000  # Change direction every 1000 milliseconds

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Actor class
class Actor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.change_direction()

    def change_direction(self):
        self.dx = random.randint(-2, 2)
        self.dy = random.randint(-2, 2)

    def move(self):
        self.x += self.dx*0.3
        self.y += self.dy*0.3
        # Boundary conditions
        if self.x < 0 or self.x > WIDTH - ACTOR_SIZE:
            self.dx = -self.dx
        if self.y < 0 or self.y > HEIGHT - ACTOR_SIZE:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, ACTOR_SIZE, ACTOR_SIZE))

# Generate initial actors
actors = [Actor(random.randint(0, WIDTH - ACTOR_SIZE), HEIGHT - ACTOR_SIZE) for _ in range(NUM_ACTORS)]

start_time = pygame.time.get_ticks()
last_direction_change = start_time

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update and draw actors
    for actor in actors:
        actor.move()
        actor.draw()

    pygame.display.flip()
    clock.tick(FPS)

    # Change direction every second
    if current_time - last_direction_change > DIRECTION_CHANGE_TIME:
        for actor in actors:
            actor.change_direction()
        last_direction_change = current_time

    # Check simulation time
    if current_time - start_time > SIMULATION_TIME:
        # Sort actors based on lowest y-value (higher up is better)
        actors.sort(key=lambda x: x.y)
        actors = actors[:10]  # Select top 10 actors
        # Breeding logic, simplifying by random mutation here
        new_actors = []
        for _ in range(NUM_ACTORS // len(actors)):
            for actor in actors:
                new_x = actor.x + random.randint(-10, 10)
                new_y = actor.y + random.randint(-10, 10)
                new_actors.append(Actor(new_x % WIDTH, new_y % HEIGHT))
        actors = new_actors
        start_time = pygame.time.get_ticks()

pygame.quit()
sys.exit()

