import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 300, 600   # Window size
BLOCK_SIZE = 30           # Size of each Tetris square
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE
FPS = 10

# Colors (R, G, B)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GRAY   = (128, 128, 128)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN   = (0, 255, 255)

# Shapes of the 7 Tetris pieces (in their 'default' orientation)
# Each shape is a list of coordinates relative to the pivot (top-left corner)
SHAPES = [
    [[1, 1, 1, 1]],                           # I
    [[1, 1],
     [1, 1]],                                # O
    [[1, 0, 0],
     [1, 1, 1]],                             # J
    [[0, 0, 1],
     [1, 1, 1]],                             # L
    [[0, 1, 1],
     [1, 1, 0]],                             # S
    [[1, 1, 0],
     [0, 1, 1]],                             # Z
    [[0, 1, 0],
     [1, 1, 1]]                              # T
]

COLORS = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE, CYAN]

# Define a function to rotate the shape clockwise
def rotate_shape(shape):
    # Transpose and reverse rows for clockwise rotation
    # shape is a list of lists representing the rows
    rotated = list(zip(*shape[::-1]))
    # Convert tuple of ints to list of ints
    return [list(row) for row in rotated]

# Check if the shape can be placed on the board
def can_place(shape, board, offset_x, offset_y):
    for r_idx, row in enumerate(shape):
        for c_idx, cell in enumerate(row):
            if cell:
                new_x = offset_x + c_idx
                new_y = offset_y + r_idx
                # Check boundaries and collision
                if (new_x < 0 or new_x >= COLS or 
                        new_y < 0 or new_y >= ROWS or 
                        board[new_y][new_x]):
                    return False
    return True

# Place the shape on the board
def place_shape(shape, board, offset_x, offset_y, color):
    for r_idx, row in enumerate(shape):
        for c_idx, cell in enumerate(row):
            if cell:
                board[offset_y + r_idx][offset_x + c_idx] = color

# Clear filled lines in the board
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    # Add empty rows at the top
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLS)
    return new_board, lines_cleared

def generate_shape():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return shape, color

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    
    # The game board is a 2D list; 0 indicates empty cell
    board = [[0]*COLS for _ in range(ROWS)]
    
    current_shape, current_color = generate_shape()
    current_x, current_y = COLS // 2 - len(current_shape[0]) // 2, 0
    
    game_over = False
    fall_time = 0
    fall_speed = 0.5
    score = 0

    running = True
    while running:
        screen.fill(BLACK)
        dt = clock.tick(FPS)
        fall_time += dt
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if can_place(current_shape, board, current_x - 1, current_y):
                        current_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if can_place(current_shape, board, current_x + 1, current_y):
                        current_x += 1
                elif event.key == pygame.K_DOWN:
                    # Move down faster
                    if can_place(current_shape, board, current_x, current_y + 1):
                        current_y += 1
                elif event.key == pygame.K_UP:
                    # Rotate
                    rotated = rotate_shape(current_shape)
                    if can_place(rotated, board, current_x, current_y):
                        current_shape = rotated
        
        # Automatic falling
        if fall_time / 1000 > fall_speed:
            if can_place(current_shape, board, current_x, current_y + 1):
                current_y += 1
            else:
                # Place the piece
                place_shape(current_shape, board, current_x, current_y, current_color)
                # Clear lines
                board, lines = clear_lines(board)
                score += lines * 10
                # Generate new piece
                current_shape, current_color = generate_shape()
                current_x, current_y = COLS // 2 - len(current_shape[0]) // 2, 0
                # If newly generated piece cannot be placed, it's game over
                if not can_place(current_shape, board, current_x, current_y):
                    game_over = True
            fall_time = 0
        
        # Draw board
        for r_idx, row in enumerate(board):
            for c_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        cell,
                        (c_idx * BLOCK_SIZE, r_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        (c_idx * BLOCK_SIZE, r_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        1
                    )

        # Draw current shape
        for r_idx, row in enumerate(current_shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        current_color,
                        ((current_x + c_idx) * BLOCK_SIZE, (current_y + r_idx) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE),
                        0
                    )
                    pygame.draw.rect(
                        screen,
                        GRAY,
                        ((current_x + c_idx) * BLOCK_SIZE, (current_y + r_idx) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE),
                        1
                    )

        # Display score
        font = pygame.font.SysFont("Arial", 18)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Game Over
        if game_over:
            over_text = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(over_text, (WIDTH // 2 - 90, HEIGHT // 2))
            pygame.display.update()
            # Wait for R or quit
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            # Reset game
                            board = [[0]*COLS for _ in range(ROWS)]
                            current_shape, current_color = generate_shape()
                            current_x, current_y = COLS // 2 - len(current_shape[0]) // 2, 0
                            score = 0
                            game_over = False
                            break
                if not game_over:
                    break
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()