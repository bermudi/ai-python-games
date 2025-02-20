import pygame
import random

# Prompt: can you write a game of Tetris in python?


# Game Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
WIDTH = BLOCK_SIZE * GRID_WIDTH
HEIGHT = BLOCK_SIZE * GRID_HEIGHT
SIDE_PANEL = 200
SCREEN_WIDTH = WIDTH + SIDE_PANEL
SCREEN_HEIGHT = HEIGHT
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),    # I - Cyan
    (0, 0, 255),      # J - Blue
    (255, 165, 0),    # L - Orange
    (255, 255, 0),    # O - Yellow
    (0, 255, 0),      # S - Green
    (255, 0, 0),      # Z - Red
    (128, 0, 128)     # T - Purple
]

SHAPES = [
    [[1, 1, 1, 1]],               # I
    [[1, 0, 0], [1, 1, 1]],       # J
    [[0, 0, 1], [1, 1, 1]],       # L
    [[1, 1], [1, 1]],             # O
    [[0, 1, 1], [1, 1, 0]],       # S
    [[1, 1, 0], [0, 1, 1]],       # Z
    [[0, 1, 0], [1, 1, 1]]        # T
]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def check_collision(self, grid, dx=0, dy=0, shape=None):
        shape = shape or self.shape
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if new_x < 0 or new_x >= GRID_WIDTH:
                        return True
                    if new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and grid[new_y][new_x] is not None:
                        return True
        return False

    def move(self, dx, dy, grid):
        self.x += dx
        self.y += dy
        if self.check_collision(grid):
            self.x -= dx
            self.y -= dy
            return False
        return True

    def rotate(self, grid):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        if not self.check_collision(grid, shape=rotated):
            self.shape = rotated
            return True
        return False

def new_piece():
    index = random.randint(0, 6)
    return Piece(SHAPES[index], COLORS[index])

def merge_piece(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                grid_y = piece.y + i
                grid_x = piece.x + j
                if grid_y >= 0:
                    grid[grid_y][grid_x] = piece.color

def clear_lines(grid):
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    for i in full_rows:
        del grid[i]
        grid.insert(0, [None]*GRID_WIDTH)
    return len(full_rows)

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                rect = (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE-1, BLOCK_SIZE-1)
                pygame.draw.rect(screen, cell, rect)

def draw_piece(screen, piece):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                x = (piece.x + j) * BLOCK_SIZE
                y = (piece.y + i) * BLOCK_SIZE
                if y >= 0:
                    rect = (x, y, BLOCK_SIZE-1, BLOCK_SIZE-1)
                    pygame.draw.rect(screen, piece.color, rect)

def draw_sidebar(screen, next_piece, score):
    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render("Next:", True, WHITE), (WIDTH+20, 20))
    
    # Draw next piece preview
    preview_x = WIDTH + 50
    preview_y = 60
    for i, row in enumerate(next_piece.shape):
        for j, cell in enumerate(row):
            if cell:
                rect = (preview_x + j*BLOCK_SIZE, preview_y + i*BLOCK_SIZE, 
                       BLOCK_SIZE-1, BLOCK_SIZE-1)
                pygame.draw.rect(screen, next_piece.color, rect)
    
    # Draw score
    screen.blit(font.render(f"Score: {score}", True, WHITE), (WIDTH+20, 200))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    grid = [[None]*GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_piece = new_piece()
    next_piece = new_piece()
    score = 0
    fall_time = 0
    game_over = False
    
    while True:
        screen.fill(BLACK)
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0, grid)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0, grid)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1, grid)
                elif event.key == pygame.K_UP:
                    current_piece.rotate(grid)
                elif event.key == pygame.K_SPACE:
                    while current_piece.move(0, 1, grid):
                        pass
                    merge_piece(current_piece, grid)
                    score += clear_lines(grid) * 100
                    current_piece, next_piece = next_piece, new_piece()
                    if current_piece.check_collision(grid):
                        game_over = True
        
        # Automatic falling
        if not game_over and current_time - fall_time > 500:
            if not current_piece.move(0, 1, grid):
                merge_piece(current_piece, grid)
                score += clear_lines(grid) * 100
                current_piece, next_piece = next_piece, new_piece()
                if current_piece.check_collision(grid):
                    game_over = True
            fall_time = current_time
        
        draw_grid(screen, grid)
        draw_piece(screen, current_piece)
        draw_sidebar(screen, next_piece, score)
        
        if game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.wait(3000)
            return
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()