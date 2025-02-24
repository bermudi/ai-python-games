import pygame
import random

pygame.init()

# Initialize Pygame
pygame.display.set_caption("Tetris")
pygame.mixer.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Tetris:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.size = 30
        self.board_width = 10
        self.board_height = 20
        self.drop_interval = 1000  # milliseconds
        self.score = 0
        self.level = 1
        self.lines = 0

        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 30)
        self.clock = pygame.time.Clock()

        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.current_piece = None
        self.next_piece = None

        self.shapes = {
            'I': [[1, 6], [[1, 1, 1, 1]], [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]],
            'J': [[2, 6], [[1, 1, 0], [0, 1, 0], [0, 1, 0]]],
            'L': [[3, 6], [[0, 0, 1], [0, 0, 1], [1, 1, 1]]],
            'O': [[4, 6], [[1, 1], [1, 1]]],
            'S': [[5, 6], [[0, 1, 1], [1, 1, 0]]],
            'T': [[6, 6], [[0, 1, 0], [1, 1, 1]]],
            'Z': [[7, 6], [[1, 1, 0], [0, 1, 1]]]
        }

        self.spawn_piece()

    def create_matrix(self, shape):
        matrix = [[0 for _ in range(len(shape[1]))] for _ in range(len(shape[0]))]
        for y, row in enumerate(shape[1]):
            for x, value in enumerate(row):
                if value:
                    matrix[y][x] = shape[0][1]
        return matrix

    def spawn_piece(self):
        shape = random.choice(list(self.shapes.values()))
        self.current_piece = {
            'matrix': self.create_matrix(shape),
            'x': (self.board_width - len(self.current_piece['matrix'][0])) // 2,
            'y': 0
        }
        self.next_piece = random.choice(list(self.shapes.values()))

    def rotate(self, matrix):
        return [[matrix[len(matrix) - 1 - i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

    def check_collision(self, matrix, x, y):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    new_x = x + j
                    new_y = y + i
                    if new_x < 0 or new_x >= self.board_width or new_y >= self.board_height:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x] != 0:
                        return True
        return False

    def merge(self, matrix, x, y):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    self.board[y + i][x + j] = matrix[i][j]

    def sweep(self):
        rows_to_remove = []
        for row in self.board:
            if all(cell != 0 for cell in row):
                rows_to_remove.append(row)
        self.lines += len(rows_to_remove)
        self.score += len(rows_to_remove) * 100
        self.level = (self.lines // 10) + 1
        self.drop_interval = max(1000 - (self.level - 1) * 100, 100)
        for _ in range(len(rows_to_remove)):
            self.board.pop()
            self.board.insert(0, [0 for _ in range(self.board_width)])

    def draw_board(self):
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y][x] != 0:
                    pygame.draw.rect(self.screen, (self.board[y][x] * 255 // 8, self.board[y][x] * 255 // 8, 255 - self.board[y][x] * 50),
                                     (x * self.size + 100, y * self.size + 100, self.size, self.size), 0)

    def draw_piece(self, piece, x, y):
        for i in range(len(piece['matrix'])):
            for j in range(len(piece['matrix'][i])):
                if piece['matrix'][i][j] != 0:
                    pygame.draw.rect(self.screen, (piece['matrix'][i][j] * 255 // 8, piece['matrix'][i][j] * 255 // 8, 255 - piece['matrix'][i][j] * 50),
                                     ((x + j) * self.size + 100, (y + i) * self.size + 100, self.size, self.size), 0)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        if self.current_piece:
            self.draw_piece(self.current_piece, self.current_piece['x'], self.current_piece['y'])
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Lines: {self.lines}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 40))
        self.screen.blit(lines_text, (10, 70))
        pygame.display.flip()

    def game_loop(self):
        last_drop = pygame.time.get_ticks()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece['x'] -= 1
                        if self.check_collision(self.current_piece['matrix'], self.current_piece['x'], self.current_piece['y']):
                            self.current_piece['x'] += 1
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece['x'] += 1
                        if self.check_collision(self.current_piece['matrix'], self.current_piece['x'], self.current_piece['y']):
                            self.current_piece['x'] -= 1
                    elif event.key == pygame.K_DOWN:
                        self.current_piece['y'] += 1
                        if self.check_collision(self.current_piece['matrix'], self.current_piece['x'], self.current_piece['y']):
                            self.current_piece['y'] -= 1
                    elif event.key == pygame.K_UP:
                        rotated = self.rotate(self.current_piece['matrix'])
                        if not self.check_collision(rotated, self.current_piece['x'], self.current_piece['y']):
                            self.current_piece['matrix'] = rotated

            current_time = pygame.time.get_ticks()
            if current_time - last_drop >= self.drop_interval:
                last_drop = current_time
                self.current_piece['y'] += 1
                if self.check_collision(self.current_piece['matrix'], self.current_piece['x'], self.current_piece['y']):
                    self.current_piece['y'] -= 1
                    self.merge(self.current_piece['matrix'], self.current_piece['x'], self.current_piece['y'])
                    self.sweep()
                    self.spawn_piece()
                    if self.check_collision(self.current_piece['matrix'], self.current_piece['x'], self.current_piece['y']):
                        running = False

            self.draw()
            self.clock.tick(60)

        pygame.quit()

def main_menu():
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 50)
    running = True
    while running:
        screen.fill(BLACK)
        text = font.render("Tetris", True, WHITE)
        text_rect = text.get_rect(center=(400, 300))
        screen.blit(text, text_rect)
        text = font.render("Press SPACE to Start", True, WHITE)
        text_rect = text.get_rect(center=(400, 400))
        screen.blit(text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game = Tetris()
                    game.game_loop()
                    running = False

        pygame.time.delay(100)
    pygame.quit()

if __name__ == "__main__":
    main_menu()