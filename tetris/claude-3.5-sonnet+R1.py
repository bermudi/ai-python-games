import pygame
import random
from typing import List, Tuple
import time

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)    # I piece
YELLOW = (255, 255, 0)  # O piece
PURPLE = (128, 0, 128)  # T piece
BLUE = (0, 0, 255)      # J piece
ORANGE = (255, 165, 0)  # L piece
GREEN = (0, 255, 0)     # S piece
RED = (255, 0, 0)       # Z piece

# Game dimensions
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SIDEBAR_WIDTH = 200
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH + SIDEBAR_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Tetromino shapes - second block in each shape list is the rotation center
SHAPES = {
    'I': [[(0, 1), (1, 1), (2, 1), (3, 1)], CYAN],
    'O': [[(0, 0), (0, 1), (1, 0), (1, 1)], YELLOW],
    'T': [[(0, 1), (1, 1), (1, 0), (2, 1)], PURPLE],
    'J': [[(0, 1), (1, 1), (2, 1), (2, 0)], BLUE],
    'L': [[(0, 1), (1, 1), (2, 1), (0, 0)], ORANGE],
    'S': [[(0, 1), (1, 1), (1, 0), (2, 0)], GREEN],
    'Z': [[(0, 0), (1, 0), (1, 1), (2, 1)], RED]
}

# Wall kick data (based on SRS - Super Rotation System)
# These values represent counter-clockwise wall kicks.
WALL_KICKS = {
    'JLSTZ': [  # For J, L, S, T, Z pieces
        [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],  # from state 0 -> 1
        [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],     # from state 1 -> 2
        [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],       # from state 2 -> 3
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],   # from state 3 -> 0
    ],
    'I': [  # I piece has different wall kick data
        [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
        [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
        [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
        [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    ]
}

class Tetromino:
    def __init__(self, shape_name: str):
        self.shape_name = shape_name
        self.shape = SHAPES[shape_name][0]  # List of block positions
        self.color = SHAPES[shape_name][1]
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        self.rotation_state = 0  # 0-3 representing the current rotation state

    def rotate(self, clockwise: bool = True) -> List[Tuple[int, int]]:
        # O piece does not rotate
        if self.color == YELLOW:
            return self.shape

        # Use the second block as the rotation center
        cx, cy = self.shape[1]
        rotated = []
        for x, y in self.shape:
            # Translate block relative to the center of rotation
            dx = x - cx
            dy = y - cy
            # Rotate 90 degrees clockwise or counter-clockwise
            if clockwise:
                new_dx = dy
                new_dy = -dx
            else:
                new_dx = -dy
                new_dy = dx
            # Translate back
            rotated.append((new_dx + cx, new_dy + cy))
        return rotated

    def get_positions(self) -> List[Tuple[int, int]]:
        return [(x + self.x, y + self.y) for x, y in self.shape]

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 0.5  # Time in seconds between automatic drops
        self.game_over = False

    def new_piece(self) -> Tetromino:
        return Tetromino(random.choice(list(SHAPES.keys())))

    def valid_move(self, piece: Tetromino, x: int, y: int) -> bool:
        positions = [(px + x, py + y) for px, py in piece.shape]
        return all(
            0 <= px < GRID_WIDTH and
            0 <= py < GRID_HEIGHT and
            (py < 0 or self.grid[py][px] == BLACK)
            for px, py in positions
        )

    def try_rotate(self, clockwise: bool = True) -> bool:
        if self.current_piece.color == YELLOW:  # O piece doesn't rotate
            return False

        # Select appropriate wall kick data
        kick_data = WALL_KICKS['I'] if self.current_piece.shape_name == 'I' else WALL_KICKS['JLSTZ']
        # Get the rotated shape
        rotated_shape = self.current_piece.rotate(clockwise=clockwise)

        # Determine the next rotation state based on rotation direction
        if clockwise:
            next_rotation = (self.current_piece.rotation_state + 1) % 4
        else:
            next_rotation = (self.current_piece.rotation_state - 1) % 4

        # Use current rotation state's wall kick offsets
        kicks = kick_data[self.current_piece.rotation_state]

        for kick_x, kick_y in kicks:
            # Create a temporary piece with the new shape and adjusted position
            temp_piece = Tetromino(self.current_piece.shape_name)
            temp_piece.shape = rotated_shape
            temp_piece.x = self.current_piece.x + kick_x
            temp_piece.y = self.current_piece.y - kick_y  # Subtracting y for Tetris coordinate system
            if self.valid_move(temp_piece, temp_piece.x, temp_piece.y):
                # Apply the successful rotation and wall kick
                self.current_piece.shape = rotated_shape
                self.current_piece.x = temp_piece.x
                self.current_piece.y = temp_piece.y
                self.current_piece.rotation_state = next_rotation
                return True

        return False

    def lock_piece(self) -> None:
        for x, y in self.current_piece.get_positions():
            if 0 <= y < GRID_HEIGHT:
                self.grid[y][x] = self.current_piece.color
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if not self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y):
            self.game_over = True

    def clear_lines(self) -> None:
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(color != BLACK for color in self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
            else:
                y -= 1
        
        # Score calculation
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

    def draw(self) -> None:
        self.screen.fill(BLACK)
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(
                    self.screen,
                    self.grid[y][x],
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                )

        # Draw current piece
        for x, y in self.current_piece.get_positions():
            if y >= 0:  # Only draw the visible part of the piece
                pygame.draw.rect(
                    self.screen,
                    self.current_piece.color,
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                )

        # Draw sidebar (score and next piece preview)
        sidebar_x = GRID_WIDTH * CELL_SIZE + 10
        font = pygame.font.Font(None, 36)
        
        # Draw score
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (sidebar_x, 20))

        # Draw next piece label
        next_text = font.render('Next:', True, WHITE)
        self.screen.blit(next_text, (sidebar_x, 100))
        
        # Draw the next piece preview
        for x, y in self.next_piece.shape:
            pygame.draw.rect(
                self.screen,
                self.next_piece.color,
                (sidebar_x + x * CELL_SIZE, 150 + y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
            )

        pygame.display.flip()

    def run(self) -> None:
        last_fall = time.time()
        
        while not self.game_over:
            current_time = time.time()
            delta_time = current_time - last_fall

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.KEYDOWN:
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
                        # Rotate clockwise
                        self.try_rotate(clockwise=True)
                    elif event.key == pygame.K_z:
                        # Rotate counter-clockwise
                        self.try_rotate(clockwise=False)

            # Handle automatic falling
            if delta_time > self.fall_speed:
                if self.valid_move(self.current_piece, self.current_piece.x, self.current_piece.y + 1):
                    self.current_piece.y += 1
                else:
                    self.lock_piece()
                last_fall = current_time

            self.draw()
            self.clock.tick(60)

        # Game over screen
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('Game Over!', True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        
        # Wait before closing
        pygame.time.wait(2000)

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
    pygame.quit()