
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

# Set up the screen dimensions


# Load background image
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Define colors
WHITE = (255, 255, 255)
BLACK = (1, 0, 0)
RED = (255, 0, 0)

# Define player attributes
player_radius = 15
player_x = SCREEN_WIDTH // 4
player_y = SCREEN_HEIGHT // 2
player_speed = 22

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

# Function to draw a circle
def draw_circle(x, y, radius):
    pygame.draw.circle(screen, WHITE, (x, y), radius)

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

high_score = load_high_score()

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    print(f"Current Coordinates: x = {player_x}, y = {player_y}")

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_high_score()

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Check if player is out of bounds
    if player_y < 0 or player_y > SCREEN_HEIGHT:
        if score > high_score:
            high_score = score
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
        print("Game Over! Out of bounds.")
        running = False

    # Update score
    score += player_speed

    # Move obstacles and remove those off-screen
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
        if obstacle.x + obstacle_width < 0:
            obstacles.remove(obstacle)

    # Generate new obstacles
    if len(obstacles) == 0 or obstacles[-1].x < SCREEN_WIDTH - obstacle_spacing:
        generate_obstacle_column()

    # Draw player
    draw_circle(player_x, player_y, player_radius)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

    # Check for collisions
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
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

    # Increase obstacle speed every 500 pixels moved
    pixels_moved += player_speed
    if pixels_moved >= 1500:
        obstacle_speed += speed_increase
        pixels_moved -= 1500

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30 * multiplyer)