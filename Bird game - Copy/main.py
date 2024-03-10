import pygame
import random

# Initialize Pygame
pygame.init()

# Get the screen info
screen_info = pygame.display.Info()

# Load music
pygame.mixer.music.load("music/background.ogg")

# Play music with loop set to -1 for infinite looping
pygame.mixer.music.play(-1)

# Set the volume (optional)
pygame.mixer.music.set_volume(0.5)  # Adjust the volume as needed (0.0 to 1.0)

multiplyer = 2

# Print the screen resolution
print("Screen Resolution:", screen_info.current_w, "x", screen_info.current_h)

# Set up the screen dimensions
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# Load background image
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load bird sprite sheet
bird_sheet = pygame.image.load("bird_sprite_sheet.png").convert_alpha()
bird_sheet = pygame.transform.flip(bird_sheet, True, False)  # Flip the bird to face right
bird_width = 100
bird_height = 606
num_bird_frames = 6
current_bird_frame = 0

# Define colors
WHITE = (255, 255, 255)
BLACK = (1, 0, 0)

# Define player attributes
bird_speed = 20

# Define obstacle attributes
obstacle_width = 50
obstacle_height = 50
obstacle_spacing = 395  # Increased spacing between obstacles
obstacle_x = SCREEN_WIDTH
obstacle_speed = 7
speed_increase = 1
pixels_moved = 0

# Define lists to keep track of obstacles
obstacles = []

# Score
score = 0
high_score = 0
font = pygame.font.Font(None, 36)

# Function to generate new obstacles in a column
def generate_obstacle_column():
    gap_start = random.randint(0, SCREEN_HEIGHT - obstacle_spacing)
    gap_end = gap_start + obstacle_spacing
    obstacles.append(pygame.Rect(SCREEN_WIDTH, 0, obstacle_width, gap_start))
    obstacles.append(pygame.Rect(SCREEN_WIDTH, gap_end, obstacle_width, SCREEN_HEIGHT - gap_end))

# Bird class for handling animation and drawing
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sheet = bird_sheet
        self.images = self.load_images()
        self.image = self.images[current_bird_frame]
        self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        bird_images = []
        for i in range(num_bird_frames):
            frame = pygame.Surface((bird_width, bird_height), pygame.SRCALPHA)
            frame.blit(self.sheet, (0, 0), (i * bird_width, 0, bird_width, bird_height))
            bird_images.append(frame)
        return bird_images

    def update_animation(self):
        global current_bird_frame
        current_bird_frame = (current_bird_frame + 1) % num_bird_frames
        self.image = self.images[current_bird_frame]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Create Bird instance
bird = Bird(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)

# Load high score from file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Reset high score
def reset_high_score():
    global high_score
    high_score = 0
    with open("high_score.txt", "w") as file:
        file.write("0")

# Load high score
high_score = load_high_score()

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_high_score()

    # Move bird
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        bird.rect.y -= bird_speed
    if keys[pygame.K_DOWN]:
        bird.rect.y += bird_speed

    # Check if bird is out of bounds
    if bird.rect.y < 0 or bird.rect.y > SCREEN_HEIGHT:
        if score > high_score:
            high_score = score
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
        print("Game Over! Out of bounds.")
        running = False

    # Update score
    score += bird_speed

    # Move obstacles and remove those off-screen
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
        if obstacle.x + obstacle_width < 0:
            obstacles.remove(obstacle)

    # Generate new obstacles
    if len(obstacles) == 0 or obstacles[-1].x < SCREEN_WIDTH - obstacle_spacing:
        generate_obstacle_column()

    # Update bird animation
    bird.update_animation()

    # Draw bird hitbox
    bird_hitbox_width = 70  # Adjust the width to match the bird's model
    bird_hitbox_height = 50  # Adjust the height to match the bird's model
    bird_hitbox = pygame.Rect(bird.rect.x + 15, bird.rect.y + 30, bird_hitbox_width, bird_hitbox_height)
    pygame.draw.rect(screen, (255, 0, 0), bird_hitbox, 2)  # Draw a red rectangle around the bird's hitbox

    # Draw bird
    bird.draw(screen)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

    # Check for collisions
    for obstacle in obstacles:
        if bird_hitbox.colliderect(obstacle):
            if score > high_score:
                high_score = score
                with open("high_score.txt", "w") as file:
                    file.write(str(high_score))
            print("Game Over! Hit obstacle.")
            running = False

    # Display score
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display high score
    high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
    screen.blit(high_score_text, (10, 50))

    # Increase obstacle speed every 1500 pixels moved
    pixels_moved += bird_speed
    if pixels_moved >= 1500:
        obstacle_speed += speed_increase
        pixels_moved -= 1500

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30 * multiplyer)

# Quit Pygame
pygame.quit()
