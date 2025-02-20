import pygame
import random

# Built by Sonnet 3.5 with the COT of qwq-32b and a little help from deepseek-v3


# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra width for next piece and score
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

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
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 0], [1, 1, 1]]  # T
]
SHAPE_COLORS = [CYAN, YELLOW, RED, GREEN, BLUE, ORANGE, MAGENTA]

class Tetromino:
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.shape_index]]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        return [list(row) for row in zip(*self.shape[::-1])]

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 500
        self.level = 1

    def valid_move(self, piece, x, y, shape=None):
        if shape is None:
            shape = piece.shape

        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:
                    if not 0 <= x + col < GRID_WIDTH:
                        return False
                    if y + row >= GRID_HEIGHT:
                        return False
                    if y + row >= 0 and self.grid[y + row][x + col]:
                        return False
        return True

    def lock_piece(self, piece):
        for row in range(len(piece.shape)):
            for col in range(len(piece.shape[row])):
                if piece.shape[row][col]:
                    if piece.y + row >= 0:
                        self.grid[piece.y + row][piece.x + col] = piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for row in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[row]):
                lines_cleared += 1
                del self.grid[row]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        if lines_cleared:
            self.score += (lines_cleared * 100) * lines_cleared

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                if self.grid[row][col]:
                    pygame.draw.rect(self.screen, self.grid[row][col],
                                   (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw current piece
        if not self.game_over:
            for row in range(len(self.current_piece.shape)):
                for col in range(len(self.current_piece.shape[row])):
                    if self.current_piece.shape[row][col]:
                        pygame.draw.rect(self.screen, self.current_piece.color,
                                       ((self.current_piece.x + col) * BLOCK_SIZE,
                                        (self.current_piece.y + row) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw next piece
        next_piece_x = GRID_WIDTH * BLOCK_SIZE + 30
        next_piece_y = 50
        font = pygame.font.Font(None, 36)
        next_text = font.render("Next:", True, WHITE)
        self.screen.blit(next_text, (next_piece_x, 10))

        for row in range(len(self.next_piece.shape)):
            for col in range(len(self.next_piece.shape[row])):
                if self.next_piece.shape[row][col]:
                    pygame.draw.rect(self.screen, self.next_piece.color,
                                   (next_piece_x + col * BLOCK_SIZE,
                                    next_piece_y + row * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (next_piece_x, 150))

        # Draw game over
        if self.game_over:
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            restart_text = font.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                            SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
            self.screen.blit(restart_text,
                           (SCREEN_WIDTH//2 - restart_text.get_width()//2,
                            SCREEN_HEIGHT//2 + game_over_text.get_height()))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick(60)

            if not self.game_over:
                if self.fall_time >= self.fall_speed:
                    self.fall_time = 0
                    if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                        self.current_piece.y += 1
                    else:
                        self.lock_piece(self.current_piece)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, self.current_piece.x - 1, self.current_piece.y):
                                self.current_piece.x -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, self.current_piece.x + 1, self.current_piece.y):
                                self.current_piece.x += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                                self.current_piece.y += 1
                        elif event.key == pygame.K_UP:
                            rotated_shape = self.current_piece.rotate()
                            if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y, rotated_shape):
                                self.current_piece.shape = rotated_shape
                        elif event.key == pygame.K_SPACE:
                            while self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                                self.current_piece.y += 1
                            self.lock_piece(self.current_piece)

            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()