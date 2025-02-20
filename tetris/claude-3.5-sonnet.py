import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 240, 240),  # Cyan
    (0, 0, 240),    # Blue
    (240, 160, 0),  # Orange
    (240, 240, 0),  # Yellow
    (0, 240, 0),    # Green
    (160, 0, 240),  # Purple
    (240, 0, 0)     # Red
]

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1],      # L
     [1, 0, 0]],
    [[1, 1, 1],      # J
     [0, 0, 1]],
    [[1, 1],         # O
     [1, 1]],
    [[1, 1, 0],      # S
     [0, 1, 1]],
    [[1, 1, 1],      # T
     [0, 1, 0]],
    [[0, 1, 1],      # Z
     [1, 1, 0]]
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.game_over = False
        self.new_piece()
        self.fall_time = 0
        self.fall_speed = 500  # Start with 0.5 seconds
        self.level = 1

    def new_piece(self):
        # Choose random shape and color
        self.current_piece = SHAPES[random.randint(0, len(SHAPES) - 1)]
        self.current_color = random.randint(0, len(COLORS) - 1)
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0

    def valid_move(self, piece, x, y):
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j]:
                    if (y + i >= GRID_HEIGHT or
                        x + j < 0 or
                        x + j >= GRID_WIDTH or
                        y + i >= 0 and self.grid[y + i][x + j]):
                        return False
        return True

    def rotate_piece(self):
        rows = len(self.current_piece)
        cols = len(self.current_piece[0])
        rotated = [[self.current_piece[rows-1-j][i] for j in range(rows)] for i in range(cols)]
        if self.valid_move(rotated, self.current_x, self.current_y):
            self.current_piece = rotated

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2-1][:]
                self.grid[0] = [0] * GRID_WIDTH
            else:
                y -= 1
        if lines_cleared:
            self.score += (lines_cleared * 100) * lines_cleared

    def lock_piece(self):
        for i in range(len(self.current_piece)):
            for j in range(len(self.current_piece[0])):
                if self.current_piece[i][j]:
                    if self.current_y + i < 0:
                        self.game_over = True
                        return
                    self.grid[self.current_y + i][self.current_x + j] = self.current_color + 1
        self.clear_lines()
        self.new_piece()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    color = COLORS[self.grid[y][x] - 1]
                    pygame.draw.rect(self.screen, color,
                                   [x * BLOCK_SIZE, y * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1])

        # Draw current piece
        if not self.game_over:
            for i in range(len(self.current_piece)):
                for j in range(len(self.current_piece[0])):
                    if self.current_piece[i][j]:
                        color = COLORS[self.current_color]
                        pygame.draw.rect(self.screen, color,
                                       [(self.current_x + j) * BLOCK_SIZE,
                                        (self.current_y + i) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1])

        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 10, 10))

        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, WHITE)
            self.screen.blit(game_over_text, (GRID_WIDTH * BLOCK_SIZE + 10, 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(60)
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, self.current_x - 1, self.current_y):
                            self.current_x -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, self.current_x + 1, self.current_y):
                            self.current_x += 1
                    if event.key == pygame.K_UP:
                        self.rotate_piece()
                    if event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                            self.current_y += 1
                    if event.key == pygame.K_SPACE:
                        while self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                            self.current_y += 1
                        self.lock_piece()
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            if not self.game_over:
                # Handle automatic falling
                if current_time - self.fall_time > self.fall_speed:
                    if self.valid_move(self.current_piece, self.current_x, self.current_y + 1):
                        self.current_y += 1
                    else:
                        self.lock_piece()
                    self.fall_time = current_time

            self.draw()

if __name__ == '__main__':
    game = Tetris()
    game.run()
    pygame.quit()