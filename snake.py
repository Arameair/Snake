import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 400

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# FPS controller
clock = pygame.time.Clock()

# Snake properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
block_size = 10
speed = 15

# Food properties
food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
food_spawn = True

# Score
score = 0
font = pygame.font.SysFont('arial', 25)

# Game loop control
running = True
ai_playing = False  # Set to True when using an AI to control the game

def game_step(action=None):
    global running, direction, change_to, score, food_spawn, snake_pos, snake_body, food_pos
    # AI Control: Map action to direction
    if ai_playing:
        action_map = {0: 'UP', 1: 'RIGHT', 2: 'DOWN', 3: 'LEFT'}
        if action is not None:
            change_to = action_map[action]




    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Update direction based on AI action or player input
    direction = change_to

    # Move snake
    if direction == 'UP':
        snake_pos[1] -= block_size
    elif direction == 'DOWN':
        snake_pos[1] += block_size
    elif direction == 'LEFT':
        snake_pos[0] -= block_size
    elif direction == 'RIGHT':
        snake_pos[0] += block_size

    # Game over conditions
    if snake_pos[0] < 0 or snake_pos[0] >= screen_width or snake_pos[1] < 0 or snake_pos[1] >= screen_height or snake_pos in snake_body[1:]:
        running = False
        return -10, True  # Return a negative reward for hitting the wall and game over status

    # Snake eats food
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
        reward = 10  # Positive reward for eating food
    else:
        snake_body.pop()
        reward = 0

    # Generate new food if needed
    if not food_spawn:
        food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True

    # Add new position to snake body
    snake_body.insert(0, list(snake_pos))

    # Drawing
    screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], block_size, block_size))
    pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], block_size, block_size))

    # Display score
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, [0, 0])

    pygame.display.flip()
    clock.tick(speed)

    return reward, False  # Return the reward and game over status (False if game is still running)

if __name__ == "__main__":
    while running:
        game_step()
        
# Quit Pygame
pygame.quit()
sys.exit()
