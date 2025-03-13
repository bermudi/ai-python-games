import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Shape:
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.blocks = random.choice([
            [[1, 1, 1, 1]],  # I-Shape
            [[1, 1], [1, 1]],  # O-Shape
            [[1, 1, 1], [0, 1, 0]],  # T-Shape
            [[1, 1, 0], [0, 1, 1]],  # S-Shape
            [[0, 1, 1], [1, 1, 0]],  # Z-Shape
            [[1, 0, 0], [1, 1, 1]],  # J-Shape
            [[0, 0, 1], [1, 1, 1]],  # L-Shape
        ])

    def rotate(self):
        self.blocks = [list(reversed(x)) for x in zip(*self.blocks)]

    def image(self):
        return self.blocks

class Tetris:
    def __init__(self):
        pygame.init()
        self.width = 400
        self.height = 500
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.grid_width = 10
        self.grid_height = 20
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.shape = Shape()
        self.score = 0

    def draw_grid(self):
        block_size = self.width / self.grid_width
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                pygame.draw.rect(self.screen, GRAY, [j * block_size, i * block_size, block_size, block_size], 1)

    def draw_shape(self):
        block_size = self.width / self.grid_width
        for i in range(len(self.shape.image())):
            for j in range(len(self.shape.image()[i])):
                if self.shape.image()[i][j] == 1:
                    pygame.draw.rect(self.screen, self.shape.color, [(self.shape.x + j) * block_size, (self.shape.y + i) * block_size, block_size, block_size])

    def draw_grid_blocks(self):
        block_size = self.width / self.grid_width
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, WHITE, [j * block_size, i * block_size, block_size, block_size])

    def check_collision(self, x, y):
        for i in range(len(self.shape.image())):
            for j in range(len(self.shape.image()[i])):
                if self.shape.image()[i][j] == 1:
                    if x + j < 0 or x + j >= self.grid_width:
                        return True
                    if y + i < 0 or y + i >= self.grid_height:
                        return True
                    if y + i >= 0 and y + i < self.grid_height and x + j >= 0 and x + j < self.grid_width:
                        if self.grid[y + i][x + j] == 1:
                            return True
        return False

    def clear_rows(self):
        rows_cleared = 0
        for i in range(self.grid_height):
            if all(cell == 1 for cell in self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.grid_width)])
                rows_cleared += 1
        self.score += rows_cleared * rows_cleared

    def run(self):
        running = True
        move_down_time = pygame.time.get_ticks()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision(self.shape.x - 1, self.shape.y):
                            self.shape.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if not self.check_collision(self.shape.x + 1, self.shape.y):
                            self.shape.x += 1
                    elif event.key == pygame.K_DOWN:
                        if not self.check_collision(self.shape.x, self.shape.y + 1):
                            self.shape.y += 1
                    elif event.key == pygame.K_UP:
                        self.shape.rotate()
                        if self.check_collision(self.shape.x, self.shape.y):
                            for _ in range(3):
                                self.shape.rotate()

            self.screen.fill(BLACK)

            current_time = pygame.time.get_ticks()
            if current_time - move_down_time >= 500:
                move_down_time = current_time
                if not self.check_collision(self.shape.x, self.shape.y + 1):
                    self.shape.y += 1
                else:
                    for i in range(len(self.shape.image())):
                        for j in range(len(self.shape.image()[i])):
                            if self.shape.image()[i][j] == 1:
                                self.grid[self.shape.y + i][self.shape.x + j] = 1
                    self.clear_rows()
                    self.shape = Shape()

            self.draw_grid()
            self.draw_grid_blocks()
            self.draw_shape()
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
