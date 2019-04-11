

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

offset = 0




# Setup
pygame.init()


# Set the width and height of the screen [width,height]
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# Speed in pixels per frame
x_speed = 0
y_speed = 0

color = WHITE

# Current position
x_coord = 0
y_coord = 10

def draw_rect(screen, x, y, color):
    # Head

    pygame.draw.rect(screen, color, [x%700, y, 5, 5], 0)


screen.fill(BLACK)
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            # User pressed down on a key

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_SPACE:
                x_speed = 1
                color = GREEN

        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            color = BLACK
            #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #    x_speed = 0
            #elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #    y_speed = 0

    # --- Game Logic

    # Move the object according to the speed vector.
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed

    # --- Drawing Code

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    #screen.fill(WHITE)
    if x_coord > 699:
        y_coord += 20
        x_coord %= 700
    if y_coord > 499:
        y_coord %= 500

    draw_rect(screen, x_coord, y_coord, color)


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit frames per second
    clock.tick(50)

# Close the window and quit.
pygame.quit()
