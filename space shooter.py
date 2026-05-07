# Import necessary libraries
import pygame  # to handle graphics and player interactions
import sys    # This is a module used to exit the game when needed
import random  # This module is used to generate random positions and speeds for the enemies.

pygame.init() # Initialize Pygame

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player class      # Sprite used to to represent 2D images 
class Player(pygame.sprite.Sprite): # Player class is inheriting from another class called Sprite
    def __init__(self):  # Constructor method that initializes the player object
        super().__init__()  # Call the constructor of the parent class (pygame.sprite.Sprite)
        # Set up the player's appearance and initial position
        self.image = pygame.Surface((50, 40))
        self.image.fill(WHITE)   
        self.rect = self.image.get_rect()  # rectangular properties of the player's image
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        # Set player attributes
        self.speed = 5
        self.shoot_delay = 150
        self.last_shot = pygame.time.get_ticks()  # Record the time when the player last fired a shot
        self.lives = 3
        self.score = 0

    def update(self):
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: # ensures that moving left won't go beyond the screen
            self.rect.x -= self.speed  # moves the player's position to the left
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        # Handle player shooting
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # Create a bullet and add it to sprite groups
            bullet = Bullet(self.rect.centerx, self.rect.top)  # Create a bullet object
            all_sprites.add(bullet)
            bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Set up the bullet's appearance and initial position
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # rectangular properties of the bullet image
        self.rect.centerx = x
        self.rect.bottom = y
        # Set bullet attribute
        self.speed = -10

    def update(self):  
        # Move the bullet upward and remove it if it goes off-screen
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Set up the enemy's appearance and initial position
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()  # rectangular properties of the enemy image
        self.reset_position()

    def reset_position(self):
        # Reset the enemy's position above the screen and assign a random speed
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 5)  # Assign a random speed to the enemy

    def update(self):
        # Move the enemy downward and reset its position if it goes off-screen
        self.rect.y += self.speed
        if self.rect.top > HEIGHT + 10:
            self.reset_position()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Create sprite groups and player
all_sprites = pygame.sprite.Group()  # used for drawing of all sprites
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player) # player is included in the general group of all sprites for easy updating and drawing

# Create a list of enemies and add them to sprite groups
enemies_list = [Enemy() for _ in range(10)] # list comprehension
all_sprites.add(*enemies_list)
enemies.add(*enemies_list)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Check collisions with player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, True)  # True is used remove enemies involved in the collision from the enemies group
    if hits:
        # Reduce player lives and reset position after a collision
        player.lives -= 1
        if player.lives <= 0:
            running = False
        else:
            player.rect.centerx = WIDTH // 2
            player.rect.bottom = HEIGHT - 10

    # Check collisions between bullets and enemies
    bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    for hit in bullet_hits:
        # Increase player score and add a new enemy
        player.score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Draw the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw lives and score
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE) # The font.render function creates a surface 
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (WIDTH - 150, 10))

    # Update display
    pygame.display.flip()  # shows any changes you made to the screen

    # Set the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit()