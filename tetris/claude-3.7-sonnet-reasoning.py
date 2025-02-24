import pygame
import random
import time
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # for sound effects

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_OFFSET_Y = SCREEN_HEIGHT - (GRID_HEIGHT * BLOCK_SIZE) - 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# Tetromino shapes
SHAPES = [
    # I
    [
        ['.....',
         '.....',
         'XXXX.',
         '.....',
         '.....'],
        ['.....',
         '..X..',
         '..X..',
         '..X..',
         '..X..'],
        ['.....',
         '.....',
         'XXXX.',
         '.....',
         '.....'],
        ['.....',
         '..X..',
         '..X..',
         '..X..',
         '..X..']
    ],
    # J
    [
        ['.....',
         '.....',
         '.XXX.',
         '...X.',
         '.....'],
        ['.....',
         '..XX.',
         '..X..',
         '..X..',
         '.....'],
        ['.....',
         'X....',
         'XXX..',
         '.....',
         '.....'],
        ['.....',
         '..X..',
         '..X..',
         '.XX..',
         '.....']
    ],
    # L
    [
        ['.....',
         '.....',
         '.XXX.',
         '.X...',
         '.....'],
        ['.....',
         '..X..',
         '..X..',
         '..XX.',
         '.....'],
        ['.....',
         '...X.',
         '.XXX.',
         '.....',
         '.....'],
        ['.....',
         '.XX..',
         '..X..',
         '..X..',
         '.....']
    ],
    # O
    [
        ['.....',
         '.....',
         '.XX..',
         '.XX..',
         '.....'],
        ['.....',
         '.....',
         '.XX..',
         '.XX..',
         '.....'],
        ['.....',
         '.....',
         '.XX..',
         '.XX..',
         '.....'],
        ['.....',
         '.....',
         '.XX..',
         '.XX..',
         '.....']
    ],
    # S
    [
        ['.....',
         '.....',
         '..XX.',
         '.XX..',
         '.....'],
        ['.....',
         '..X..',
         '..XX.',
         '...X.',
         '.....'],
        ['.....',
         '.....',
         '..XX.',
         '.XX..',
         '.....'],
        ['.....',
         '..X..',
         '..XX.',
         '...X.',
         '.....']
    ],
    # T
    [
        ['.....',
         '.....',
         '.XXX.',
         '..X..',
         '.....'],
        ['.....',
         '..X..',
         '.XX..',
         '..X..',
         '.....'],
        ['.....',
         '..X..',
         '.XXX.',
         '.....',
         '.....'],
        ['.....',
         '..X..',
         '..XX.',
         '..X..',
         '.....']
    ],
    # Z
    [
        ['.....',
         '.....',
         '.XX..',
         '..XX.',
         '.....'],
        ['.....',
         '...X.',
         '..XX.',
         '..X..',
         '.....'],
        ['.....',
         '.....',
         '.XX..',
         '..XX.',
         '.....'],
        ['.....',
         '...X.',
         '..XX.',
         '..X..',
         '.....']
    ]
]

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

# Initialize clock
clock = pygame.time.Clock()

# Load sound effects
try:
    rotate_sound = pygame.mixer.Sound('rotate.wav')
    clear_sound = pygame.mixer.Sound('clear.wav')
    fall_sound = pygame.mixer.Sound('fall.wav')
    game_over_sound = pygame.mixer.Sound('gameover.wav')
    
    # Set volume
    rotate_sound.set_volume(0.5)
    clear_sound.set_volume(0.6)
    fall_sound.set_volume(0.5)
    game_over_sound.set_volume(0.7)
except:
    # If sound files are not found, create dummy sound objects
    class DummySound:
        def play(self):
            pass
        
        def set_volume(self, volume):
            pass
    
    rotate_sound = DummySound()
    clear_sound = DummySound()
    fall_sound = DummySound()
    game_over_sound = DummySound()

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation]
    
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                positions.append((piece.x + j, piece.y + i))
    
    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(GRID_WIDTH) if grid[y][x] == BLACK] for y in range(GRID_HEIGHT)]
    accepted_positions = [pos for sublist in accepted_positions for pos in sublist]
    
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 0:
            return True
    return False

def get_shape():
    return Piece(GRID_WIDTH // 2 - 2, 0, random.choice(SHAPES))

def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(
                surface, 
                grid[y][x], 
                (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                0
            )
    
    # Draw grid lines
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(
            surface, 
            GRAY, 
            (GRID_OFFSET_X, GRID_OFFSET_Y + y * BLOCK_SIZE),
            (GRID_OFFSET_X + GRID_WIDTH * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE)
        )
    
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(
            surface, 
            GRAY, 
            (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y),
            (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + GRID_HEIGHT * BLOCK_SIZE)
        )
    
    # Draw border
    pygame.draw.rect(
        surface, 
        GRAY, 
        (GRID_OFFSET_X, GRID_OFFSET_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE),
        1
    )

def draw_ghost_piece(surface, piece, grid):
    ghost_piece = Piece(piece.x, piece.y, piece.shape)
    ghost_piece.rotation = piece.rotation
    
    # Move the ghost piece down until it collides
    while valid_space(ghost_piece, grid):
        ghost_piece.y += 1
    
    ghost_piece.y -= 1
    
    # Draw the ghost piece
    formatted = convert_shape_format(ghost_piece)
    
    for pos in formatted:
        x, y = pos
        if y >= 0:
            pygame.draw.rect(
                surface, 
                (50, 50, 50),  # Light gray color for ghost piece
                (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )

def draw_piece(surface, piece, offset=(0, 0)):
    formatted = convert_shape_format(piece)
    
    for pos in formatted:
        x, y = pos
        if y >= 0:
            pygame.draw.rect(
                surface, 
                piece.color, 
                (GRID_OFFSET_X + (x + offset[0]) * BLOCK_SIZE, 
                 GRID_OFFSET_Y + (y + offset[1]) * BLOCK_SIZE, 
                 BLOCK_SIZE, BLOCK_SIZE),
                0
            )

def draw_next_shape(surface, piece):
    # Display text
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape:', 1, WHITE)
    
    # Position for the next piece preview
    start_x = SCREEN_WIDTH - 200
    start_y = SCREEN_HEIGHT // 2
    
    # Draw the label
    surface.blit(label, (start_x + 10, start_y - 40))
    
    # Draw the next piece
    formatted = piece.shape[piece.rotation]
    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == 'X':
                pygame.draw.rect(
                    surface, 
                    piece.color, 
                    (start_x + j * BLOCK_SIZE, start_y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                )

def animate_clear_rows(surface, grid, rows_to_clear):
    # Flash the rows white before clearing
    for flash in range(3):
        for row in rows_to_clear:
            for x in range(GRID_WIDTH):
                color = WHITE if flash % 2 == 0 else grid[row][x]
                pygame.draw.rect(
                    surface,
                    color,
                    (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0
                )
        
        pygame.display.update()
        pygame.time.delay(100)

def clear_rows(grid, locked, surface):
    inc = 0
    rows_to_clear = []
    
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            rows_to_clear.append(i)
    
    if rows_to_clear:
        # Animate clearing
        animate_clear_rows(surface, grid, rows_to_clear)
        clear_sound.play()
        
        # Remove the rows
        for row in rows_to_clear:
            inc += 1
            for j in range(GRID_WIDTH):
                try:
                    del locked[(j, row)]
                except:
                    continue
        
        # Sort the locked positions by y value and shift them down
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < min(rows_to_clear):
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc

def draw_score_and_level(surface, score, high_score, level):
    font = pygame.font.SysFont('comicsans', 30)
    
    # Current score
    score_label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(score_label, (30, 30))
    
    # High score
    high_score_label = font.render(f'High Score: {high_score}', 1, WHITE)
    surface.blit(high_score_label, (30, 70))
    
    # Level
    level_label = font.render(f'Level: {level}', 1, WHITE)
    surface.blit(level_label, (30, 110))

def draw_pause_screen(surface):
    # Semi-transparent overlay
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 128))
    surface.blit(s, (0, 0))
    
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('PAUSED', 1, WHITE)
    
    surface.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - label.get_height()//2))
    
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Press P to continue', 1, WHITE)
    
    surface.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 + 50))
    
    pygame.display.update()

def draw_game_over(surface, score):
    game_over_sound.play()
    
    # Semi-transparent overlay
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 180))
    surface.blit(s, (0, 0))
    
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('GAME OVER', 1, RED)
    
    surface.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 - 100))
    
    font = pygame.font.SysFont('comicsans', 40)
    score_label = font.render(f'Score: {score}', 1, WHITE)
    
    surface.blit(score_label, (SCREEN_WIDTH//2 - score_label.get_width()//2, SCREEN_HEIGHT//2))
    
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Press any key to restart', 1, WHITE)
    
    surface.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, SCREEN_HEIGHT//2 + 100))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def draw_window(surface, grid, score, high_score, level, next_piece=None, current_piece=None, ghost_mode=True):
    surface.fill(BLACK)
    
    # Draw score and level
    draw_score_and_level(surface, score, high_score, level)
    
    # Draw grid and pieces
    draw_grid(surface, grid)
    
    # Draw ghost piece
    if ghost_mode and current_piece:
        draw_ghost_piece(surface, current_piece, grid)
    
    # Draw current piece
    if current_piece:
        draw_piece(surface, current_piece)
    
    # Draw next piece
    if next_piece:
        draw_next_shape(surface, next_piece)
    
    pygame.display.update()

def get_high_score():
    try:
        with open('tetris_high_score.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open('tetris_high_score.txt', 'w') as f:
        f.write(str(score))

def calculate_level(score):
    return max(1, score // 1000 + 1)

def get_fall_speed(level):
    return max(0.1, 0.27 - (level - 1) * 0.02)

def main():
    global grid
    
    high_score = get_high_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0
    level = 1
    fall_speed = get_fall_speed(level)
    ghost_mode = True  # Enable ghost piece by default
    paused = False
    
    while run:
        grid = create_grid(locked_positions)
        
        if not paused:
            fall_time += clock.get_rawtime()
        clock.tick()
        
        # Update level based on score
        current_level = calculate_level(score)
        if current_level != level:
            level = current_level
            fall_speed = get_fall_speed(level)
        
        # Piece falling logic
        if not paused and fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
                fall_sound.play()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        draw_pause_screen(screen)
                
                if not paused:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    
                    elif event.key == pygame.K_UP:
                        # Rotate piece
                        old_rotation = current_piece.rotation
                        current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = old_rotation
                        else:
                            rotate_sound.play()
                    
                    elif event.key == pygame.K_SPACE:
                        # Hard drop
                        while valid_space(current_piece, grid):
                            current_piece.y += 1
                        current_piece.y -= 1
                        change_piece = True
                        fall_sound.play()
                    
                    elif event.key == pygame.K_g:
                        # Toggle ghost piece
                        ghost_mode = not ghost_mode
        
        # Add piece to the grid if it's locked
        piece_pos = convert_shape_format(current_piece)
        
        # Color the grid where the piece is
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        # If piece hit the ground
        if change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            
            # Clear rows and update score
            rows_cleared = clear_rows(grid, locked_positions, screen)
            if rows_cleared == 1:
                score += 40 * level
            elif rows_cleared == 2:
                score += 100 * level
            elif rows_cleared == 3:
                score += 300 * level
            elif rows_cleared == 4:
                score += 1200 * level
            
            # Update high score
            if score > high_score:
                high_score = score
                save_high_score(high_score)
        
        # Update the window
        if not paused:
            draw_window(screen, grid, score, high_score, level, next_piece, current_piece, ghost_mode)
        
        # Check if game over
        if check_lost(locked_positions):
            run = False
            draw_game_over(screen, score)
    
    return score, high_score

def draw_controls(surface):
    font = pygame.font.SysFont('comicsans', 30)
    controls = [
        "Controls:",
        "Left/Right Arrow: Move horizontally",
        "Down Arrow: Move down faster",
        "Up Arrow: Rotate piece",
        "Space: Hard drop",
        "G: Toggle ghost piece",
        "P: Pause game"
    ]
    
    y_offset = 400
    for text in controls:
        label = font.render(text, 1, WHITE)
        surface.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, y_offset))
        y_offset += 35

def main_menu():
    run = True
    while run:
        screen.fill(BLACK)
        font = pygame.font.SysFont('comicsans', 80)
        title = font.render('TETRIS', 1, CYAN)
        
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        font = pygame.font.SysFont('comicsans', 40)
        label = font.render('Press any key to begin', 1, WHITE)
        
        screen.blit(label, (SCREEN_WIDTH//2 - label.get_width()//2, 300))
        
        draw_controls(screen)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

if __name__ == '__main__':
    main_menu()  # start the game