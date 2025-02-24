import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GAME_AREA_LEFT = (SCREEN_WIDTH - GRID_WIDTH * GRID_SIZE) // 2
GAME_AREA_TOP = SCREEN_HEIGHT - GRID_HEIGHT * GRID_SIZE - 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # J
    [[1, 1, 1], [0, 0, 1]],  # L
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Colors for each shape
SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, BLUE, ORANGE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        
        self.reset_game()
        
    def reset_game(self):
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.new_piece()
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        
    def new_piece(self):
        # Choose a random shape
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = {
            'shape': SHAPES[shape_idx],
            'color': SHAPE_COLORS[shape_idx],
            'x': GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2,
            'y': 0
        }
        
        # Check if the new piece collides immediately (game over)
        if self.check_collision():
            self.game_over = True
    
    def rotate_piece(self):
        # Create a rotated version of the current piece
        rotated = list(zip(*reversed(self.current_piece['shape'])))
        previous = self.current_piece['shape']
        
        # Try to rotate
        self.current_piece['shape'] = rotated
        
        # If rotation causes collision, revert back
        if self.check_collision():
            self.current_piece['shape'] = previous
    
    def check_collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    
                    # Check if piece is outside the board or collides with another piece
                    if (board_x < 0 or board_x >= GRID_WIDTH or 
                        board_y >= GRID_HEIGHT or 
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False
    
    def move_piece(self, dx, dy):
        # Save the current position
        previous_x = self.current_piece['x']
        previous_y = self.current_piece['y']
        
        # Try to move
        self.current_piece['x'] += dx
        self.current_piece['y'] += dy
        
        # If the move causes a collision, revert back
        if self.check_collision():
            self.current_piece['x'] = previous_x
            self.current_piece['y'] = previous_y
            
            # If it was a downward move that caused the collision, place the piece
            if dy > 0:
                self.place_piece()
                self.clear_lines()
                self.new_piece()
            
            return False
        return True
    
    def place_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    
                    # If the piece is at least partially on the board
                    if board_y >= 0:
                        # Store the color index + 1 (0 means empty cell)
                        self.board[board_y][board_x] = SHAPE_COLORS.index(self.current_piece['color']) + 1
    
    def clear_lines(self):
        lines_to_clear = []
        
        for y in range(GRID_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        # Remove the completed lines and add new empty lines at the top
        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Update score
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            
            # Different scoring based on number of lines cleared at once
            line_score = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += line_score.get(len(lines_to_clear), 0) * self.level
            
            # Increase level every 10 lines
            self.level = self.lines_cleared // 10 + 1
            
            # Increase speed with level
            self.fall_speed = max(100, 500 - (self.level - 1) * 40)
    
    def hard_drop(self):
        # Move the piece down until it collides
        while self.move_piece(0, 1):
            pass
    
    def draw_board(self):
        # Draw the game area background
        pygame.draw.rect(self.screen, WHITE, 
                        (GAME_AREA_LEFT - 1, GAME_AREA_TOP - 1, 
                         GRID_WIDTH * GRID_SIZE + 2, GRID_HEIGHT * GRID_SIZE + 2), 1)
        
        # Draw the placed blocks
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x]:
                    color_idx = self.board[y][x] - 1
                    pygame.draw.rect(self.screen, SHAPE_COLORS[color_idx],
                                    (GAME_AREA_LEFT + x * GRID_SIZE, 
                                     GAME_AREA_TOP + y * GRID_SIZE,
                                     GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(self.screen, BLACK,
                                    (GAME_AREA_LEFT + x * GRID_SIZE, 
                                     GAME_AREA_TOP + y * GRID_SIZE,
                                     GRID_SIZE, GRID_SIZE), 1)
        
        # Draw the current piece
        if not self.game_over:
            for y, row in enumerate(self.current_piece['shape']):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, self.current_piece['color'],
                                        (GAME_AREA_LEFT + (self.current_piece['x'] + x) * GRID_SIZE, 
                                         GAME_AREA_TOP + (self.current_piece['y'] + y) * GRID_SIZE,
                                         GRID_SIZE, GRID_SIZE))
                        pygame.draw.rect(self.screen, BLACK,
                                        (GAME_AREA_LEFT + (self.current_piece['x'] + x) * GRID_SIZE, 
                                         GAME_AREA_TOP + (self.current_piece['y'] + y) * GRID_SIZE,
                                         GRID_SIZE, GRID_SIZE), 1)
    
    def draw_info(self):
        # Draw score, level, and lines cleared
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        level_text = self.font.render(f'Level: {self.level}', True, WHITE)
        lines_text = self.font.render(f'Lines: {self.lines_cleared}', True, WHITE)
        
        self.screen.blit(score_text, (50, 50))
        self.screen.blit(level_text, (50, 100))
        self.screen.blit(lines_text, (50, 150))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render('GAME OVER - Press R to restart', True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(game_over_text, text_rect)
    
    def run(self):
        running = True
        
        # For handling continuous key presses
        move_left = False
        move_right = False
        move_down = False
        
        while running:
            # Handle falling
            current_time = pygame.time.get_ticks()
            if current_time - self.fall_time > self.fall_speed and not self.game_over:
                self.fall_time = current_time
                self.move_piece(0, 1)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if not self.game_over:
                        if event.key == K_LEFT:
                            move_left = True
                        elif event.key == K_RIGHT:
                            move_right = True
                        elif event.key == K_DOWN:
                            move_down = True
                        elif event.key == K_UP:
                            self.rotate_piece()
                        elif event.key == K_SPACE:
                            self.hard_drop()
                    
                    if event.key == K_r:
                        self.reset_game()
                
                elif event.type == KEYUP:
                    if event.key == K_LEFT:
                        move_left = False
                    elif event.key == K_RIGHT:
                        move_right = False
                    elif event.key == K_DOWN:
                        move_down = False
            
            # Handle continuous movement
            if not self.game_over:
                if move_left:
                    self.move_piece(-1, 0)
                if move_right:
                    self.move_piece(1, 0)
                if move_down:
                    self.move_piece(0, 1)
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_info()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == '__main__':
    game = Tetris()
    game.run()