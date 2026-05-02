import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class PygameRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Raycasting Engine")
        self.clock = pygame.time.Clock()
        
        # Define some colors for different wall types
        self.wall_colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Purple
            (0, 255, 255),  # Cyan
        ]

    def render_frame(self, scanlines: list[dict]):
        # Clear screen with dark gray (ceiling/floor)
        self.screen.fill((50, 50, 50))

        for line in scanlines:
            # Calculate line height based on distance
            line_height = int(SCREEN_HEIGHT / line['dist']) if line['dist'] > 0 else SCREEN_HEIGHT
            
            # Calculate start and end positions for vertical line
            start_y = (SCREEN_HEIGHT - line_height) // 2
            end_y = start_y + line_height
            
            # Get color based on color_id, with darker shade for side walls
            color_id = line['color_id'] - 1  # Convert to 0-based index
            if 0 <= color_id < len(self.wall_colors):
                base_color = self.wall_colors[color_id]
                # Darken color for side walls (EW walls)
                if line['side'] == 1:
                    dark_color = (
                        max(0, base_color[0] // 2),
                        max(0, base_color[1] // 2),
                        max(0, base_color[2] // 2)
                    )
                    pygame.draw.line(self.screen, dark_color, (line['x'], start_y), (line['x'], end_y))
                else:
                    pygame.draw.line(self.screen, base_color, (line['x'], start_y), (line['x'], end_y))
            else:
                # Default color if color_id is invalid
                pygame.draw.line(self.screen, (200, 200, 200), (line['x'], start_y), (line['x'], end_y))

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True