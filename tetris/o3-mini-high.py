import pygame
import random

# Initialize pygame fonts
pygame.font.init()

# GLOBAL VARIABLES
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
PLAY_WIDTH = 300   # 10 columns * 30 px
PLAY_HEIGHT = 600  # 20 rows * 30 px
BLOCK_SIZE = 30

TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT

# SHAPE FORMATS (each shape is a list of rotations, each rotation is a list of 5 strings)
S = [
    [
        ".....",
        ".....",
        "..00.",
        ".00..",
        "....."
    ],
    [
        ".....",
        "..0..",
        "..00.",
        "...0.",
        "....."
    ]
]

Z = [
    [
        ".....",
        ".....",
        ".00..",
        "..00.",
        "....."
    ],
    [
        ".....",
        "..0..",
        ".00..",
        ".0...",
        "....."
    ]
]

I = [
    [
        "..0..",
        "..0..",
        "..0..",
        "..0..",
        "....."
    ],
    [
        ".....",
        "0000.",
        ".....",
        ".....",
        "....."
    ]
]

O = [
    [
        ".....",
        ".....",
        ".00..",
        ".00..",
        "....."
    ]
]

J = [
    [
        ".....",
        ".0...",
        ".000.",
        ".....",
        "....."
    ],
    [
        ".....",
        "..00.",
        "..0..",
        "..0..",
        "....."
    ],
    [
        ".....",
        ".....",
        ".000.",
        "...0.",
        "....."
    ],
    [
        ".....",
        "..0..",
        "..0..",
        ".00..",
        "....."
    ]
]

L = [
    [
        ".....",
        "...0.",
        ".000.",
        ".....",
        "....."
    ],
    [
        ".....",
        "..0..",
        "..0..",
        "..00.",
        "....."
    ],
    [
        ".....",
        ".....",
        ".000.",
        ".0...",
        "....."
    ],
    [
        ".....",
        ".00..",
        "..0..",
        "..0..",
        "....."
    ]
]

T = [
    [
        ".....",
        "..0..",
        ".000.",
        ".....",
        "....."
    ],
    [
        ".....",
        "..0..",
        "..00.",
        "..0..",
        "....."
    ],
    [
        ".....",
        ".....",
        ".000.",
        "..0..",
        "....."
    ],
    [
        ".....",
        "..0..",
        ".00..",
        "..0..",
        "....."
    ]
]

# List of shapes and their corresponding colors
shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (0, 255, 0),      # S - Green
    (255, 0, 0),      # Z - Red
    (0, 255, 255),    # I - Cyan
    (255, 255, 0),    # O - Yellow
    (0, 0, 255),      # J - Blue
    (255, 165, 0),    # L - Orange
    (128, 0, 128)     # T - Purple
]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x  # grid position x (column index)
        self.y = y  # grid position y (row index)
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    """
    Create a grid of 20 rows x 10 columns.
    Each cell is a color (tuple). Empty cells are black.
    """
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


def convert_shape_format(piece):
    """
    Convert the piece's shape from its string format into a list of (x, y) positions on the grid.
    Adjust by subtracting 2 from x and 4 from y to center the shape.
    """
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((piece.x + j - 2, piece.y + i - 4))

    return positions


def valid_space(piece, grid):
    """
    Check if the piece's current position is valid (i.e. not out of bounds or overlapping locked positions).
    """
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [pos for sub in accepted_positions for pos in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        x, y = pos
        if pos not in accepted_positions:
            if y > -1:
                return False
    return True


def check_lost(locked_positions):
    """
    Check if any locked position is above the top of the play area.
    """
    for pos in locked_positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    """
    Return a random new piece.
    """
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    """
    Draw text in the middle of the given surface.
    """
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(
        label,
        (
            TOP_LEFT_X + PLAY_WIDTH / 2 - label.get_width() / 2,
            TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2,
        ),
    )


def draw_grid(surface, grid):
    """
    Draw grid lines on the play area.
    """
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    for i in range(len(grid)):
        # Horizontal lines
        pygame.draw.line(
            surface, (128, 128, 128), (sx, sy + i * BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE)
        )
        for j in range(len(grid[i])):
            # Vertical lines
            pygame.draw.line(
                surface, (128, 128, 128), (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT)
            )


def clear_rows(grid, locked):
    """
    Check for and clear full rows.
    For each full row, remove the locked positions and shift everything above down.
    Returns the number of rows cleared.
    """
    inc = 0
    # Iterate over grid rows from bottom to top
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        # If there is no black cell in the row, then the row is full
        if (0, 0, 0) not in row:
            inc += 1
            # Remove the blocks from the locked positions
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except KeyError:
                    continue

    if inc > 0:
        # Shift every locked position above the cleared row(s) down
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_window(surface, grid, score=0):
    """
    Draw the main game window, including the grid, borders, title, and score.
    """
    surface.fill((0, 0, 0))

    # Tetris Title
    font = pygame.font.SysFont("comicsans", 40)
    label = font.render("Tetris", 1, (255, 255, 255))
    surface.blit(
        label,
        (TOP_LEFT_X + PLAY_WIDTH / 2 - label.get_width() / 2, 30),
    )

    # Current Score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score: " + str(score), 1, (255, 255, 255))
    sx = TOP_LEFT_X + PLAY_WIDTH + 20
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    surface.blit(label, (sx, sy))

    # Draw the grid blocks
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                0,
            )

    # Draw the grid lines and borders
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


def draw_next_shape(piece, surface):
    """
    Draw the next piece preview on the side of the play area.
    """
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape:", 1, (255, 255, 255))

    sx = TOP_LEFT_X + PLAY_WIDTH + 20
    sy = TOP_LEFT_Y + PLAY_HEIGHT / 2 - 100
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        for j, char in enumerate(line):
            if char == "0":
                pygame.draw.rect(
                    surface,
                    piece.color,
                    (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    0,
                )
    surface.blit(label, (sx, sy - 30))


def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27  # Adjust fall speed (lower is faster)
    level_time = 0

    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Increase difficulty over time
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # Piece falling logic
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        shape_positions = convert_shape_format(current_piece)

        # Draw the piece on the grid
        for i in range(len(shape_positions)):
            x, y = shape_positions[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # If piece hit the ground or another piece, lock it in place
        if change_piece:
            for pos in shape_positions:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("YOU LOST", 80, (255, 255, 255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False


def main_menu(win):
    """
    Main menu loop which waits for a key press to start the game.
    """
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle("Press Any Key To Play", 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()


if __name__ == "__main__":
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    main_menu(win)
