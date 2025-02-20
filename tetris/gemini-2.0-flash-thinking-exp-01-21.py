import pygame
import random


############
# Comments #
############
#
# Took two tries.
# Model had to fix 
# File "/home/daniel/build/tetris/gemini-2.0-flash-thinking-exp-01-21.py", line 49, in get_random_piece
#    return PIECES[piece_index], PIECE_COLORS[piece_index + 1] # +1 because index 0 is black
# IndexError: list index out of range
# End result lacks "gravity", meaning the pieces do not fall
#

# --- Constants ---
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 30
FALL_SPEED = 0.5  # Blocks per second

COLORS = [
    (0, 0, 0),       # 0: Black (Empty)
    (255, 0, 0),     # 1: Red
    (0, 255, 0),     # 2: Green
    (0, 0, 255),     # 3: Blue
    (255, 255, 0),   # 4: Yellow
    (255, 165, 0),   # 5: Orange
    (128, 0, 128),   # 6: Purple
    (0, 255, 255)    # 7: Cyan
]

PIECES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1],         # O
     [1, 1]],
    [[0, 1, 1],      # S
     [1, 1, 0]],
    [[1, 1, 0],      # Z
     [0, 1, 1]],
    [[1, 1, 1],      # T
     [0, 1, 0]],
    [[1, 1, 1],      # L
     [1, 0, 0]],
    [[1, 1, 1],      # J
     [0, 0, 1]]
]

PIECE_COLORS = [0, 7, 4, 2, 6, 5, 3] # Colors corresponding to PIECES indices


# --- Functions ---
def create_grid():
    return [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

def get_random_piece():
    piece_index = random.randint(0, len(PIECES) - 1)
    return PIECES[piece_index], PIECE_COLORS[piece_index]  # Removed the +1

def rotate_piece(piece):
    rotated_piece = list(zip(*piece[::-1])) # Clever rotation using zip and reverse
    return [list(row) for row in rotated_piece]

def is_valid_position(piece, grid, offset_x, offset_y):
    piece_height = len(piece)
    piece_width = len(piece[0])

    for y in range(piece_height):
        for x in range(piece_width):
            if piece[y][x]:  # If it's a block in the piece
                grid_x = offset_x + x
                grid_y = offset_y + y

                if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT: # Out of bounds
                    return False
                if grid_y >= 0 and grid[grid_y][grid_x] != 0: # Collision with existing block
                    return False
    return True

def place_piece(piece, grid, offset_x, offset_y, color):
    piece_height = len(piece)
    piece_width = len(piece[0])

    for y in range(piece_height):
        for x in range(piece_width):
            if piece[y][x]:
                grid[offset_y + y][offset_x + x] = color

def clear_lines(grid):
    lines_cleared = 0
    full_rows = []
    for y in range(GRID_HEIGHT):
        if all(grid[y]): # Check if all cells in a row are non-zero (filled)
            full_rows.append(y)

    if full_rows:
        lines_cleared = len(full_rows)
        for row_index in full_rows:
            del grid[row_index] # Remove the full row
            grid.insert(0, [0] * GRID_WIDTH) # Insert a new empty row at the top
    return lines_cleared


def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] != 0:
                pygame.draw.rect(screen, COLORS[grid[y][x]],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0) # Filled rect
                pygame.draw.rect(screen, (100, 100, 100), # Dark gray border
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1) # Border

def draw_piece(screen, piece, color, offset_x, offset_y):
    piece_height = len(piece)
    piece_width = len(piece[0])
    for y in range(piece_height):
        for x in range(piece_width):
            if piece[y][x]:
                pygame.draw.rect(screen, COLORS[color],
                                 ((offset_x + x) * BLOCK_SIZE, (offset_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, (100, 100, 100),
                                 ((offset_x + x) * BLOCK_SIZE, (offset_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def game_over_screen(screen):
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", 1, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000) # Wait for 2 seconds


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Tetris")
    clock = pygame.time.Clock()

    grid = create_grid()
    current_piece, current_color = get_random_piece()
    piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
    piece_y = 0
    fall_time = 0
    score = 0
    game_active = True

    font = pygame.font.Font(None, 36)


    running = True
    while running:
        if not game_active:
            game_over_screen(screen)
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if is_valid_position(current_piece, grid, piece_x - 1, piece_y):
                        piece_x -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid_position(current_piece, grid, piece_x + 1, piece_y):
                        piece_x += 1
                elif event.key == pygame.K_DOWN:
                    if is_valid_position(current_piece, grid, piece_x, piece_y + 1):
                        piece_y += 1
                elif event.key == pygame.K_UP: # Rotate
                    rotated = rotate_piece(current_piece)
                    if is_valid_position(rotated, grid, piece_x, piece_y):
                        current_piece = rotated


        # --- Game Logic ---
        fall_time += clock.get_rawtime() / 1000.0 # Convert milliseconds to seconds
        if fall_time > FALL_SPEED:
            fall_time -= FALL_SPEED
            if is_valid_position(current_piece, grid, piece_x, piece_y + 1):
                piece_y += 1
            else:
                place_piece(current_piece, grid, piece_x, piece_y, current_color)
                lines = clear_lines(grid)
                score += lines * lines * 100 # Simple scoring system
                current_piece, current_color = get_random_piece()
                piece_x = GRID_WIDTH // 2 - len(current_piece[0]) // 2
                piece_y = 0
                if not is_valid_position(current_piece, grid, piece_x, piece_y):
                    game_active = False


        # --- Drawing ---
        screen.fill((0, 0, 0)) # Black background
        draw_grid(screen, grid)
        draw_piece(screen, current_piece, current_color, piece_x, piece_y)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()