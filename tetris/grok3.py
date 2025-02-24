import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_X = (WIDTH - GRID_WIDTH * BLOCK_SIZE) // 2
GRID_Y = (HEIGHT - GRID_HEIGHT * BLOCK_SIZE) // 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return {
            'shape': SHAPES[shape_idx],
            'color': COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }

    def valid_move(self, piece, x, y):
        for i in range(len(piece['shape'])):
            for j in range(len(piece['shape'][0])):
                if piece['shape'][i][j]:
                    new_x = x + j
                    new_y = y + i
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def merge_piece(self):
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    y = self.current_piece['y'] + i
                    x = self.current_piece['x'] + j
                    if y >= 0:
                        self.grid[y][x] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for i in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
        self.score += lines_cleared * 100

    def rotate_piece(self):
        original_shape = self.current_piece['shape']
        n = len(original_shape)
        m = len(original_shape[0])
        rotated = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(n):
            for j in range(m):
                rotated[m-1-j][i] = original_shape[i][j]
        
        original_x = self.current_piece['x']
        self.current_piece['shape'] = rotated
        if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
            self.current_piece['shape'] = original_shape
            return False
        return True

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j]:
                    pygame.draw.rect(self.screen, self.grid[i][j],
                                   [GRID_X + j * BLOCK_SIZE, GRID_Y + i * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1])

        # Draw current piece
        for i in range(len(self.current_piece['shape'])):
            for j in range(len(self.current_piece['shape'][0])):
                if self.current_piece['shape'][i][j]:
                    pygame.draw.rect(self.screen, self.current_piece['color'],
                                   [GRID_X + (self.current_piece['x'] + j) * BLOCK_SIZE,
                                    GRID_Y + (self.current_piece['y'] + i) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1])

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def run(self):
        fall_time = 0
        fall_speed = 50  # Lower is faster

        while not self.game_over:
            fall_time += 1
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_piece['x'] - 1, self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_piece['x'] + 1, self.current_piece['y']):
                            self.current_piece['x'] += 1
                    if event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                            self.current_piece['y'] += 1
                    if event.key == pygame.K_UP:
                        self.rotate_piece()

            if fall_time >= fall_speed:
                fall_time = 0
                if self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y'] + 1):
                    self.current_piece['y'] += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    self.current_piece = self.new_piece()
                    if not self.valid_move(self.current_piece, self.current_piece['x'], self.current_piece['y']):
                        self.game_over = True

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        # Game over screen
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('Game Over!', True, WHITE)
        self.screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)

if __name__ == '__main__':
    game = Tetris()
    game.run()
    pygame.quit()