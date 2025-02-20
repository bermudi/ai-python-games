import pygame
import random
import math
import heapq
from PIL import Image, ImageDraw

# ----------------------------
# GLOBAL CONSTANTS & SETTINGS
# ----------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CELL_SIZE = 40  # grid cell size (for environment and path/heat map)
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# ----------------------------
# SPRITE FACTORY: PIL-based Sprite Generation with Caching
# ----------------------------
class SpriteFactory:
    def __init__(self):
        self.cache = {}

    def pil_to_pygame(self, image):
        mode = image.mode
        size = image.size
        data = image.tobytes()
        return pygame.image.fromstring(data, size, mode)

    def get_tower_sprite(self, tower_type, level=1, frame=0):
        key = ("tower", tower_type, level, frame)
        if key in self.cache:
            return self.cache[key]
        # Create a transparent image
        image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        # Draw different tower designs based on the tower type
        if tower_type == "basic":
            draw.rectangle([10, 10, 30, 30], fill=(100 + level * 20, 100, 200))
            draw.ellipse([15, 5, 25, 15], fill=(255, 255, 0))
        elif tower_type == "splash":
            draw.rectangle([8, 8, 32, 32], fill=(200, 50, 50))
            draw.ellipse([0, 0, 40, 40], outline="orange", width=2)
        elif tower_type == "slow":
            draw.rectangle([10, 10, 30, 30], fill=(50, 200, 200))
            draw.line([10, 10, 30, 30], fill="blue", width=2)
        elif tower_type == "buffer":
            draw.rectangle([8, 8, 32, 32], fill=(150, 150, 150))
            draw.line([8, 32, 32, 8], fill="green", width=3)
        else:
            draw.rectangle([10, 10, 30, 30], fill=(100, 100, 100))
        # Simple pulsing border to simulate animation frames
        radius = 20 + int(5 * math.sin(frame / 10))
        draw.ellipse([20 - radius, 20 - radius, 20 + radius, 20 + radius], outline=(255, 255, 255, 150))
        sprite = self.pil_to_pygame(image)
        self.cache[key] = sprite
        return sprite

    def get_enemy_sprite(self, enemy_type, variant=0, frame=0):
        key = ("enemy", enemy_type, variant, frame)
        if key in self.cache:
            return self.cache[key]
        image = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if enemy_type == "basic":
            draw.ellipse([5, 5, 25, 25], fill=(0, 200, 0))
        elif enemy_type == "flying":
            draw.polygon([(15, 0), (30, 15), (15, 30), (0, 15)], fill=(200, 200, 50))
        elif enemy_type == "armored":
            draw.rectangle([5, 5, 25, 25], fill=(100, 100, 100))
            draw.rectangle([10, 10, 20, 20], fill=(50, 50, 50))
        elif enemy_type == "healer":
            draw.ellipse([5, 5, 25, 25], fill=(50, 200, 50))
            draw.line([5, 15, 25, 15], fill="white", width=2)
            draw.line([15, 5, 15, 25], fill="white", width=2)
        elif enemy_type == "boss":
            draw.ellipse([0, 0, 30, 30], fill=(200, 0, 0))
            draw.text((5, 5), "B", fill="white")
        else:
            draw.ellipse([5, 5, 25, 25], fill=(150, 150, 150))
        sprite = self.pil_to_pygame(image)
        self.cache[key] = sprite
        return sprite

    def get_projectile_sprite(self, projectile_type="default", frame=0):
        key = ("projectile", projectile_type, frame)
        if key in self.cache:
            return self.cache[key]
        image = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse([2, 2, 8, 8], fill=(255, 165, 0))
        sprite = self.pil_to_pygame(image)
        self.cache[key] = sprite
        return sprite

    def get_environment_sprite(self, env_type, frame=0):
        key = ("environment", env_type, frame)
        if key in self.cache:
            return self.cache[key]
        image = Image.new("RGBA", (CELL_SIZE, CELL_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if env_type == "grass":
            draw.rectangle([0, 0, CELL_SIZE, CELL_SIZE], fill=(34, 139, 34))
        elif env_type == "road":
            draw.rectangle([0, 0, CELL_SIZE, CELL_SIZE], fill=(128, 128, 128))
        else:
            draw.rectangle([0, 0, CELL_SIZE, CELL_SIZE], fill=(100, 100, 100))
        sprite = self.pil_to_pygame(image)
        self.cache[key] = sprite
        return sprite

    def get_ui_sprite(self, ui_type, text="", frame=0):
        key = ("ui", ui_type, text, frame)
        if key in self.cache:
            return self.cache[key]
        width, height = 120, 40
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        if ui_type == "button":
            draw.rectangle([0, 0, width, height], fill=(70, 130, 180), outline="white")
            draw.text((10, 10), text, fill="white")
        else:
            draw.rectangle([0, 0, width, height], fill=(50, 50, 50), outline="white")
            draw.text((10, 10), text, fill="white")
        sprite = self.pil_to_pygame(image)
        self.cache[key] = sprite
        return sprite

# ----------------------------
# TOWER CLASS: Advanced Tower Mechanics with Upgrades, Multiple Attacks, and Synergy
# ----------------------------
class Tower:
    def __init__(self, pos, tower_type, sprite_factory):
        self.pos = pos  # (x, y) in pixels
        self.tower_type = tower_type
        self.level = 1
        self.sprite_factory = sprite_factory
        self.attack_range = 100
        self.attack_damage = 10
        self.attack_speed = 1.0  # shots per second
        self.cooldown = 0
        # Each tower randomly selects one of three targeting strategies
        self.targeting_strategy = random.choice(["closest", "lowest_health", "fastest"])
        # Buff multiplier for synergy (modified by buffer towers)
        self.damage_multiplier = 1.0
        # Buff radius is applicable only for buffer towers
        self.buff_radius = 80 if tower_type == "buffer" else 0

    def upgrade(self):
        if self.level < 3:
            self.level += 1
            self.attack_damage += 5
            self.attack_range += 10
            self.attack_speed *= 1.1

    def update(self, dt, enemies, towers, projectiles):
        # Buffer towers buff nearby towers
        if self.tower_type == "buffer":
            for tower in towers:
                if tower != self:
                    dist = math.hypot(self.pos[0] - tower.pos[0], self.pos[1] - tower.pos[1])
                    if dist < self.buff_radius:
                        tower.damage_multiplier = 1.2
        # Tower shooting cooldown
        self.cooldown -= dt
        if self.cooldown <= 0:
            target = self.select_target(enemies)
            if target:
                # Create a projectile with damage modified by synergy
                projectile = Projectile(self.pos, target, self.attack_damage * self.damage_multiplier, self.sprite_factory)
                projectiles.append(projectile)
                self.cooldown = 1 / self.attack_speed

    def select_target(self, enemies):
        valid = []
        for enemy in enemies:
            dist = math.hypot(self.pos[0] - enemy.pos[0], self.pos[1] - enemy.pos[1])
            if dist <= self.attack_range:
                valid.append(enemy)
        if not valid:
            return None
        if self.targeting_strategy == "closest":
            valid.sort(key=lambda e: math.hypot(self.pos[0] - e.pos[0], self.pos[1] - e.pos[1]))
        elif self.targeting_strategy == "lowest_health":
            valid.sort(key=lambda e: e.health)
        elif self.targeting_strategy == "fastest":
            valid.sort(key=lambda e: e.speed, reverse=True)
        return valid[0]

    def get_sprite(self, frame):
        return self.sprite_factory.get_tower_sprite(self.tower_type, self.level, frame)

# ----------------------------
# ENEMY CLASS: Including State Machine and A*–Based Path Following
# ----------------------------
class Enemy:
    def __init__(self, enemy_type, path, sprite_factory, variant=0, health=50, speed=50):
        self.enemy_type = enemy_type
        self.path = path  # list of pixel coordinate waypoints
        self.sprite_factory = sprite_factory
        self.variant = variant
        self.health = health
        self.max_health = health
        self.speed = speed  # pixels per second
        self.state = "moving"
        self.path_index = 0
        # Start at the first waypoint
        self.pos = list(self.path[0])

    def update(self, dt):
        if self.state == "moving":
            if self.path_index < len(self.path) - 1:
                target = self.path[self.path_index + 1]
                dx = target[0] - self.pos[0]
                dy = target[1] - self.pos[1]
                dist = math.hypot(dx, dy)
                if dist != 0:
                    dx, dy = dx / dist, dy / dist
                self.pos[0] += dx * self.speed * dt
                self.pos[1] += dy * self.speed * dt
                if math.hypot(target[0] - self.pos[0], target[1] - self.pos[1]) < 5:
                    self.path_index += 1
            else:
                self.state = "attack_base"  # enemy reached the goal
        elif self.state == "healing":
            # Additional behaviors (e.g., healing allies) can be implemented here.
            pass

    def get_sprite(self, frame):
        return self.sprite_factory.get_enemy_sprite(self.enemy_type, self.variant, frame)

# ----------------------------
# PROJECTILE CLASS: Handles Movement Toward Targets and Particle Effect Animation
# ----------------------------
class Projectile:
    def __init__(self, pos, target, damage, sprite_factory):
        self.pos = list(pos)
        self.target = target
        self.damage = damage
        self.speed = 300  # pixels per second
        self.sprite_factory = sprite_factory
        self.alive = True
        self.frame = 0

    def update(self, dt):
        if not self.alive or self.target.health <= 0:
            self.alive = False
            return
        dx = self.target.pos[0] - self.pos[0]
        dy = self.target.pos[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 0.0001
        dx, dy = dx / dist, dy / dist
        self.pos[0] += dx * self.speed * dt
        self.pos[1] += dy * self.speed * dt
        self.frame += dt * 10
        # Check collision
        if math.hypot(self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1]) < 10:
            self.target.health -= self.damage
            self.alive = False

    def get_sprite(self):
        return self.sprite_factory.get_projectile_sprite("default", int(self.frame) % 4)

# ----------------------------
# A* PATHFINDING: Computes a Path on the Grid (used for Enemy Movement)
# ----------------------------
def a_star(start, goal, grid):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            data.reverse()
            # Convert grid cells to pixel positions (center of cell)
            path = [(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2) for x, y in data]
            return path
        close_set.add(current)
        for i, j in neighbors:
            neighbor = (current[0] + i, current[1] + j)
            tentative_g_score = gscore[current] + 1
            if 0 <= neighbor[0] < GRID_WIDTH and 0 <= neighbor[1] < GRID_HEIGHT:
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue  # blocked cell (obstacle)
            else:
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return []

# ----------------------------
# WAVE GENERATOR: Uses a Simple Genetic Algorithm-Inspired Approach
# ----------------------------
class WaveGenerator:
    def __init__(self, sprite_factory):
        self.wave_number = 0
        self.sprite_factory = sprite_factory

    def generate_wave(self, path):
        self.wave_number += 1
        enemies = []
        count = 5 + self.wave_number  # Increase enemy count with each wave
        for i in range(count):
            r = random.random()
            if self.wave_number >= 5 and r < 0.1:
                enemy_type = "boss"
                health = 200 + self.wave_number * 20
                speed = 30
            elif r < 0.2:
                enemy_type = "flying"
                health = 40 + self.wave_number * 5
                speed = 70
            elif r < 0.4:
                enemy_type = "armored"
                health = 80 + self.wave_number * 10
                speed = 40
            elif r < 0.6:
                enemy_type = "healer"
                health = 50 + self.wave_number * 8
                speed = 50
            else:
                enemy_type = "basic"
                health = 50 + self.wave_number * 5
                speed = 50
            enemy = Enemy(enemy_type, path, self.sprite_factory, health=health, speed=speed)
            enemies.append(enemy)
        return enemies

# ----------------------------
# HEAT MAP GENERATION: Calculates Frequency Along the Enemy Path
# ----------------------------
def generate_heatmap(path):
    heatmap = {}
    for pos in path:
        cell = (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE)
        if cell in heatmap:
            heatmap[cell] += 1
        else:
            heatmap[cell] = 1
    return heatmap

# ----------------------------
# MAIN GAME LOOP
# ----------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Advanced Tower Defense")
    clock = pygame.time.Clock()

    # Initialize the sprite generator
    sprite_factory = SpriteFactory()

    # Create a simple grid map.
    # For this example, we create a “road” by ensuring the middle row is walkable.
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for x in range(GRID_WIDTH):
        grid[GRID_HEIGHT // 2][x] = 0  # road cells (0 means free/walkable)

    # Compute a path from the left to the right end of the grid along the middle row
    start_cell = (0, GRID_HEIGHT // 2)
    goal_cell = (GRID_WIDTH - 1, GRID_HEIGHT // 2)
    path = a_star(start_cell, goal_cell, grid)
    heatmap = generate_heatmap(path)

    # Initialize wave generator and generate the first wave
    wave_gen = WaveGenerator(sprite_factory)
    enemies = wave_gen.generate_wave(path)

    towers = []
    projectiles = []

    # Pre-place towers for demonstration (each tower type shows distinct behavior)
    towers.append(Tower((200, SCREEN_HEIGHT // 2 - 60), "basic", sprite_factory))
    towers.append(Tower((300, SCREEN_HEIGHT // 2 + 40), "splash", sprite_factory))
    towers.append(Tower((400, SCREEN_HEIGHT // 2 - 40), "slow", sprite_factory))
    towers.append(Tower((500, SCREEN_HEIGHT // 2), "buffer", sprite_factory))

    font = pygame.font.SysFont("arial", 18)
    frame_count = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update towers (including synergy buffs and attacking enemies)
        for tower in towers:
            tower.update(dt, enemies, towers, projectiles)

        # Update enemies (state machine and path following)
        for enemy in enemies:
            enemy.update(dt)
        # Remove enemies that have been destroyed or reached the base
        enemies = [e for e in enemies if e.health > 0 and e.state != "attack_base"]

        # Update projectiles (movement and collision)
        for projectile in projectiles:
            projectile.update(dt)
        projectiles = [p for p in projectiles if p.alive]

        # If the wave is cleared, generate the next wave (dynamic difficulty adjustment can be added here)
        if not enemies:
            enemies = wave_gen.generate_wave(path)

        # ----------------------------
        # RENDERING
        # ----------------------------
        # Draw the environment grid (road and grass)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (x, y) in heatmap:
                    sprite = sprite_factory.get_environment_sprite("road")
                else:
                    sprite = sprite_factory.get_environment_sprite("grass")
                screen.blit(sprite, cell_rect)

        # Render heatmap overlay for tower placement efficiency
        heat_overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        for (x, y), heat in heatmap.items():
            heat_overlay.fill((255, 0, 0, min(heat * 20, 150)))
            screen.blit(heat_overlay, (x * CELL_SIZE, y * CELL_SIZE))

        # Draw towers with their animated sprites
        for tower in towers:
            sprite = tower.get_sprite(frame_count)
            rect = sprite.get_rect(center=tower.pos)
            screen.blit(sprite, rect)

        # Draw enemies with health bar
        for enemy in enemies:
            sprite = enemy.get_sprite(frame_count)
            rect = sprite.get_rect(center=enemy.pos)
            screen.blit(sprite, rect)
            hp_ratio = enemy.health / enemy.max_health
            hp_bar_width = 30
            hp_bar_rect = pygame.Rect(enemy.pos[0] - 15, enemy.pos[1] - 20, hp_bar_width * hp_ratio, 4)
            pygame.draw.rect(screen, (255, 0, 0), hp_bar_rect)

        # Draw projectiles
        for projectile in projectiles:
            sprite = projectile.get_sprite()
            rect = sprite.get_rect(center=projectile.pos)
            screen.blit(sprite, rect)

        # Draw UI elements (e.g., current wave)
        wave_text = font.render(f"Wave: {wave_gen.wave_number}", True, (255, 255, 255))
        screen.blit(wave_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
