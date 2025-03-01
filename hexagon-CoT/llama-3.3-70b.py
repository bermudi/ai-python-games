import pygame
import math

# Initialize Pygame
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the width and height of the screen (width, height).
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2
        self.vx = 5
        self.vy = 5
        self.radius = 10

    def update(self):
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius < 0 or self.x + self.radius > size[0]:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > size[1]:
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

class Hexagon:
    def __init__(self):
        self.x = size[0] // 2
        self.y = size[1] // 2
        self.radius = 100
        self.angle = 0

    def update(self):
        self.angle += 1

    def draw(self):
        points = []
        for i in range(6):
            angle = self.angle + i * math.pi / 3
            px = self.x + self.radius * math.cos(angle)
            py = self.y + self.radius * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, WHITE, points, 2)

ball = Ball()
hexagon = Hexagon()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    hexagon.update()
    hexagon.draw()

    ball.update()
    ball.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()