import pygame
import random

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Shape:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.blocks = random.choice([
            [[0, 0], [1, 0], [0, 1], [1, 1]],  # O shape
            [[-1, 0], [0, 0], [1, 0], [2, 0]],  # I shape
            [[0, 0], [1, 0], [0, 1], [0, 2]],  # J shape
            [[0, 0], [1, 0], [1, 1], [1, 2]],  # L shape
            [[0, 0], [1, 0], [0, 1], [1, 1]],  # S shape
            [[0, 0], [1, 0], [1, 1], [2, 1]],  # Z shape
            [[0, 0], [1, 0], [2, 0], [1, 1]]   # T shape
        ])

    def rotate(self):
        new_blocks = [[-y, x] for x, y in self.blocks]
        self.blocks = new_blocks

class Tetris:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.shape = Shape()
        self.score = 0
        self.speed = 1
        self.screen = pygame.display.set_mode((300, 400))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        fall_time = 0
        while running:
            self.clock.tick(60)
            fall_time += 1 / 60
            if fall_time >= 1 / self.speed:
                fall_time = 0
                self.move_down()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_side(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move_side(1)
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_UP:
                        self.shape.rotate()
                        if not self.is_valid_position():
                            self.shape.rotate()
                            self.shape.rotate()
                            self.shape.rotate()
            self.draw()
        pygame.quit()

    def is_valid_position(self):
        for x, y in self.shape.blocks:
            grid_x = x + self.shape.x
            grid_y = y + self.shape.y
            if grid_x < 0 or grid_x >= self.width or grid_y >= self.height:
                return False
            if grid_y >= 0 and self.grid[grid_y][grid_x] is not None:
                return False
        return True

    def move_side(self, dx):
        self.shape.x += dx
        if not self.is_valid_position():
            self.shape.x -= dx

    def move_down(self):
        self.shape.y += 1
        if not self.is_valid_position():
            self.shape.y -= 1
            self.lock_shape()
            self.check_for_lines()
            self.shape = Shape()
            if not self.is_valid_position():
                print("Game Over")
                pygame.quit()
                quit()

    def lock_shape(self):
        for x, y in self.shape.blocks:
            grid_x = x + self.shape.x
            grid_y = y + self.shape.y
            if grid_y >= 0:
                self.grid[grid_y][grid_x] = self.shape.color

    def check_for_lines(self):
        lines_cleared = 0
        for y, row in enumerate(self.grid):
            if all(cell is not None for cell in row):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.width)])
                lines_cleared += 1
        self.score += lines_cleared * lines_cleared

    def draw(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell is not None:
                    pygame.draw.rect(self.screen, cell, (x * 20 + 50, y * 20 + 50, 20, 20), 0)
        for x, y in self.shape.blocks:
            grid_x = x + self.shape.x
            grid_y = y + self.shape.y
            if grid_y >= 0:
                pygame.draw.rect(self.screen, self.shape.color, (grid_x * 20 + 50, grid_y * 20 + 50, 20, 20), 0)
        pygame.draw.rect(self.screen, WHITE, (50, 50, self.width * 20, self.height * 20), 1)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

if __name__ == "__main__":
    game = Tetris()
    game.run()