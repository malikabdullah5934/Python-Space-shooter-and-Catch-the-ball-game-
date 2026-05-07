import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600  # Set the dimensions of the game window
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))#it display the size of display
pygame.display.set_caption("Tower Defense")  # Set the window title

# Clock to control the frame rate
clock = pygame.time.Clock()

# Tower class
class Tower(pygame.sprite.Sprite): # Tower class is inheriting from another class called Sprite which is usedd to show the 2d object
    def __init__(self, width, height, screen_width):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)  # Set the color of the tower
        self.rect = self.image.get_rect(midbottom=(screen_width // 2, HEIGHT))  # Set initial position

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= 5

    def move_right(self, screen_width):
        if self.rect.right < screen_width:
            self.rect.x += 5

# FallingBlock class
class FallingBlock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(15, 35)  # Set a random radius for the falling block provided the range
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)  # Draw a circle on the surface
        self.rect = self.image.get_rect(midtop=(random.randint(0, WIDTH - self.radius * 2), 0))  # Set initial position of falling blocks

    def update(self):
        self.rect.y += 5  # Move the falling block down

# Groups for sprites
all_sprites = pygame.sprite.Group()  # Group to hold all sprites
towers = pygame.sprite.Group()  # Group to hold tower sprites
falling_blocks = pygame.sprite.Group()  # Group to hold falling block sprites

# Create a tower
tower = Tower(width=100, height=20, screen_width=WIDTH)
all_sprites.add(tower)

# Game variables
score = 0  # Player's score
missed_balls = 0  # Number of falling blocks missed by the tower
font = pygame.font.Font(None, 36)  # Font for displaying text we considered the font 0 and the size is 36

# Variables to control block spawning and scoring
spawn_timer = 15  # Timer to control when to spawn a new falling block
spawn_interval = 100  # Time between spawning blocks
score_increment_interval = 30  # Time between score increments
missed_ball_limit = 5  # Maximum number of missed blocks before game over

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tower.move_left()
    if keys[pygame.K_RIGHT]:
        tower.move_right(WIDTH)

    all_sprites.update()

    # Spawn new falling block
    spawn_timer += 1
    if spawn_timer >= spawn_interval:
        block = FallingBlock()
        all_sprites.add(block)
        falling_blocks.add(block)
        spawn_timer = 0

    # Check for collisions (tower catches falling block)
    collisions = pygame.sprite.spritecollide(tower, falling_blocks, True)
    for block in collisions:
        # Adjust block position to align with the tower's top
        block.rect.y = tower.rect.top - block.radius
        falling_blocks.add(block)

    # Increment score
    if spawn_timer % score_increment_interval == 0:
        score += 1

    # Check for missed balls
    for block in falling_blocks:
        if block.rect.y > HEIGHT:
            missed_balls += 1
            falling_blocks.remove(block)

    # Check for game over
    if missed_balls >= missed_ball_limit:
        running = False

    # Draw
    screen.fill((0, 0, 0))  # Fill the screen with black
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display missed balls
    missed_text = font.render(f"Missed: {missed_balls}/{missed_ball_limit}", True, WHITE)
    screen.blit(missed_text, (WIDTH - 150, 10))

    # Refresh the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Game over message
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
pygame.display.flip()

# Pause for a moment before quitting
pygame.time.delay(2000)

# Quit Pygame
pygame.quit()
sys.exit()