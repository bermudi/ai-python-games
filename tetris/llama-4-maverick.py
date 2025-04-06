import pygame
import random

pygame.init()

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GRAY     = ( 128, 128, 128)
RED      = ( 255,   0,   0)

size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

class Shape:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)])
        self.blocks = random.choice([
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[0, 1, 0], [1, 1, 1]],  # T
            [[1, 0, 0], [1, 1, 1]],  # J
            [[0, 0, 1], [1, 1, 1]],  # L
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]]   # Z
        ])

    def rotate(self):
        self.blocks = [list(reversed(x)) for x in zip(*self.blocks)]

class Grid:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(width)] for _ in range(height)]

    def draw(self):
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, [x * 20 + 100, y * 20 + 50, 20, 20], 0)

    def is_collision(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape.blocks):
            for x, val in enumerate(row):
                if val:
                    cell_x = x + offset_x
                    cell_y = y + offset_y
                    if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height or self.cells[cell_y][cell_x]:
                        return True
        return False

    def place_shape(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape.blocks):
            for x, val in enumerate(row):
                if val:
                    cell_x = x + offset_x
                    cell_y = y + offset_y
                    self.cells[cell_y][cell_x] = shape.color

    def check_and_clear_rows(self):
        to_remove = []
        for i, row in enumerate(self.cells):
            if all(row):
                to_remove.append(i)
        if to_remove:
            for i in sorted(to_remove, reverse=True):
                del self.cells[i]
                self.cells.insert(0, [None for _ in range(self.width)])
        return len(to_remove)

grid = Grid()
current_shape = Shape()
score = 0
fall_time = 0
fall_rate = 500  # lower is faster

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not grid.is_collision(current_shape, current_shape.x - 1, current_shape.y):
                    current_shape.x -= 1
            elif event.key == pygame.K_RIGHT:
                if not grid.is_collision(current_shape, current_shape.x + 1, current_shape.y):
                    current_shape.x += 1
            elif event.key == pygame.K_DOWN:
                if not grid.is_collision(current_shape, current_shape.x, current_shape.y + 1):
                    current_shape.y += 1
            elif event.key == pygame.K_SPACE:
                while not grid.is_collision(current_shape, current_shape.x, current_shape.y + 1):
                    current_shape.y += 1
            elif event.key == pygame.K_UP:
                current_shape.rotate()
                if grid.is_collision(current_shape, current_shape.x, current_shape.y):
                    current_shape.rotate()
                    current_shape.rotate()
                    current_shape.rotate()  # revert

    # --- Game logic should go here
    fall_time += clock.get_time()
    if fall_time >= fall_rate:
        fall_time = 0
        if not grid.is_collision(current_shape, current_shape.x, current_shape.y + 1):
            current_shape.y += 1
        else:
            grid.place_shape(current_shape, current_shape.x, current_shape.y)
            lines_cleared = grid.check_and_clear_rows()
            if lines_cleared == 1:
                score += 100
            elif lines_cleared == 2:
                score += 300
            elif lines_cleared == 3:
                score += 500
            elif lines_cleared == 4:
                score += 800
            current_shape = Shape()

    # --- Screen-clearing code goes here
    screen.fill(WHITE)

    # --- Drawing code should go here
    grid.draw()
    for y, row in enumerate(current_shape.blocks):
        for x, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, current_shape.color, [(current_shape.x + x) * 20 + 100, (current_shape.y + y) * 20 + 50, 20, 20], 0)

    pygame.draw.rect(screen, GRAY, [100, 50, 200, 400], 1)  # grid outline
    font = pygame.font.SysFont('arial', 24)
    text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(text, [120, 20])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()