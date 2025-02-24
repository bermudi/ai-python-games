import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = BLOCK_SIZE * 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
    (0, 255, 0),    # Green
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (255, 127, 0)   # Orange
]

# Tetromino shapes
TETROMINOES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

# Setup game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.spawn_piece()
        
    def spawn_piece(self):
        shape = random.randint(0, len(TETROMINOES) - 1)
        self.current_piece = {
            'shape': TETROMINOES[shape],
            'color': COLORS[shape],
            'x': GRID_WIDTH // 2 - len(TETROMINOES[shape][0]) // 2,
            'y': 0
        }
        
        if self.check_collision():
            self.game_over = True

    def check_collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece['x'] + x
                    new_y = self.current_piece['y'] + y
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return True
        return False

    def rotate_piece(self):
        original_shape = self.current_piece['shape']
        self.current_piece['shape'] = list(zip(*reversed(self.current_piece['shape'])))
        if self.check_collision():
            self.current_piece['shape'] = original_shape

    def move_piece(self, dx, dy):
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy
        if self.check_collision():
            self.current_piece['x'] -= dx
            self.current_piece['y'] -= dy
            if dy > 0:  # If moving down, lock the piece
                self.lock_piece()
                self.clear_lines()
                self.spawn_piece()
                return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        cleared = len(lines_to_clear)
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += [0, 100, 300, 500, 800][cleared]
            self.level = self.lines_cleared // 10 + 1

    def draw(self):
        screen.fill(BLACK)
        
        # Draw game border
        pygame.draw.rect(screen, WHITE, 
                        (GAME_AREA_LEFT - 2, 0, GRID_WIDTH * BLOCK_SIZE + 4, GRID_HEIGHT * BLOCK_SIZE), 2)

        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x],
                                   (GAME_AREA_LEFT + x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw current piece
        if self.current_piece:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece['color'],
                                       (GAME_AREA_LEFT + (self.current_piece['x'] + x) * BLOCK_SIZE,
                                        (self.current_piece['y'] + y) * BLOCK_SIZE,
                                        BLOCK_SIZE - 1, BLOCK_SIZE - 1))

        # Draw score and level
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        screen.blit(score_text, (GAME_AREA_LEFT + GRID_WIDTH * BLOCK_SIZE + 20, 50))
        screen.blit(level_text, (GAME_AREA_LEFT + GRID_WIDTH * BLOCK_SIZE + 20, 100))

        if self.game_over:
            game_over_text = font.render('GAME OVER', True, WHITE)
            screen.blit(game_over_text, (GAME_AREA_LEFT + GRID_WIDTH * BLOCK_SIZE // 4, GRID_HEIGHT * BLOCK_SIZE // 2))

        pygame.display.flip()

def main():
    game = Tetris()
    fall_speed = 1000  # Time in milliseconds
    fall_timer = 0
    last_fall_time = pygame.time.get_ticks()
    
    while True:
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_fall_time
        fall_timer += delta_time
        last_fall_time = current_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    while not game.move_piece(0, 1):
                        pass

        # Handle automatic falling
        if not game.game_over:
            fall_speed = max(50, 1000 - (game.level - 1) * 100)  # Increase speed with level
            if fall_timer >= fall_speed:
                game.move_piece(0, 1)
                fall_timer = 0

        game.draw()
        clock.tick(60)

if __name__ == '__main__':
    main()