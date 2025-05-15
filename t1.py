import random
import pygame
import heapq
import time
import os
import math
from PIL import Image, ImageFilter
import pygame.surfarray

# Initialize pygame mixer for sound effects
pygame.mixer.init()

a = random.randint(0, 5)
if a == 0:
    from paths.generate_maze import get_maze
elif a == 1:
    from paths.generate_maze_rhombus import get_maze
elif a == 2:
    from paths.generate_maze_brain import get_maze
elif a == 3:
    from paths.generate_maze_spiral import get_maze
elif a == 4:
    from paths.generate_maze_heart import get_maze
else:
    from paths.generate_maze_sphere import get_maze

maze = get_maze() 
N = len(maze)

CELL_SIZE = 10
WIDTH = HEIGHT = N * CELL_SIZE

# Create a centered window
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_pos_x = (screen_width - WIDTH) // 2
window_pos_y = (screen_height - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_pos_x},{window_pos_y}"

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Adventure")

# Improved colors with more vibrance
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
BLUE = (30, 144, 255)  # Dodger Blue
YELLOW = (255, 255, 0)
WALL_COLOR = (40, 40, 60)  # Dark blue-ish for walls
PATH_COLOR = (230, 230, 250)  # Lavender for paths
BFS_COLOR = (255, 105, 180)  # Hot pink for BFS
ASTAR_COLOR = (255, 215, 0)  # Gold for A*

# Particle system
particles = []

# Find start position and end position
player_x, player_y = 0, 0
end_x, end_y = 0, 0
for i in range(N):
    for j in range(N):
        if maze[i][j] == 'S':
            player_x, player_y = i, j
        elif maze[i][j] == 'E':
            end_x, end_y = i, j

# Create clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Try to load sound effects (with fallback if files don't exist)
try:
    move_sound = pygame.mixer.Sound("sounds/move.wav")
    algorithm_sound = pygame.mixer.Sound("sounds/algorithm.wav")
    win_sound = pygame.mixer.Sound("sounds/win.wav")
except:
    # Create silent dummy sounds if files don't exist
    move_sound = pygame.mixer.Sound(bytearray(44))  # Empty sound
    algorithm_sound = pygame.mixer.Sound(bytearray(44))
    win_sound = pygame.mixer.Sound(bytearray(44))

# Load or create a small font
try:
    small_font = pygame.font.Font("fonts/game_font.ttf", 16)
except:
    small_font = pygame.font.SysFont(None, 16)

# Stats tracking
moves_made = 0
start_time = None
algorithm_uses = {"BFS": 0, "A*": 0}

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(1, 3)
        self.lifetime = random.randint(20, 40)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        return self.lifetime <= 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

def create_particles(x, y, color, count=10):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def bfs(maze, start):
    queue = [start]
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.pop(0)
        if maze[current[0]][current[1]] == 'E':
            path1 = []
            while current is not None:
                path1.append(current)
                current = parent[current]
            return path1[::-1]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < N and 0 <= neighbor[1] < N:
                if maze[neighbor[0]][neighbor[1]] == 0:
                    continue
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current
    return None

def astar_search(maze, start, end):
    def heuristic(pos, end):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
    
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), start))
    
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < N and 0 <= neighbor[1] < N:
                if maze[neighbor[0]][neighbor[1]] == 0:
                    continue
                
                move_cost = 1
                tentative_g = g_score.get(current, float('inf')) + move_cost
                
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))
    
    return None

def draw_controls(win):
    font = pygame.font.SysFont(None, 24)
    controls = [
        "Controls:",
        "- Move: W/A/S/D or Arrow Keys",
        "- Diagonal Move: Q/E/Z/C",
        "- Toggle A* AI Path: SPACE",
        "- Toggle BFS Path: P"
    ]
    # Draw semi-transparent background for controls
    control_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
    pygame.draw.rect(control_surface, (0, 0, 0, 150), (0, 0, WIDTH, 100))
    win.blit(control_surface, (0, HEIGHT - 100))
    
    for i, line in enumerate(controls):
        text = font.render(line, True, (200, 200, 100))
        win.blit(text, (10, HEIGHT - 100 + i * 20))

def draw_stats(win):
    # Calculate elapsed time
    if start_time:
        elapsed = time.time() - start_time
        time_str = f"Time: {int(elapsed // 60):02d}:{int(elapsed % 60):02d}"
    else:
        time_str = "Time: 00:00"
    
    # Create stats display
    stats = [
        f"Moves: {moves_made}",
        time_str,
        f"BFS used: {algorithm_uses['BFS']}",
        f"A* used: {algorithm_uses['A*']}"
    ]
    
    # Draw semi-transparent background for stats
    stats_surface = pygame.Surface((150, 85), pygame.SRCALPHA)
    pygame.draw.rect(stats_surface, (0, 0, 0, 150), (0, 0, 150, 85))
    win.blit(stats_surface, (WIDTH - 160, 10))
    
    font = pygame.font.SysFont(None, 20)
    for i, line in enumerate(stats):
        text = font.render(line, True, (200, 200, 200))
        win.blit(text, (WIDTH - 150, 15 + i * 20))

def draw_maze_with_fog(win, maze, player_pos, visibility_radius=5):
    # Draw base maze with fog of war effect
    for i in range(N):
        for j in range(N):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            
            # Calculate distance from player
            dx = abs(i - player_pos[0])
            dy = abs(j - player_pos[1])
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Determine visibility (0 = invisible, 1 = fully visible)
            visibility = max(0, min(1, (visibility_radius - distance) / visibility_radius))
            
            if maze[i][j] == 0:  # Wall
                color = WALL_COLOR
            elif maze[i][j] == 1:  # Path
                color = PATH_COLOR
            elif maze[i][j] == 'S':  # Start
                color = GREEN
            elif maze[i][j] == 'E':  # End
                color = RED
            else:
                color = BLACK
                
            # Apply fog of war (darken based on distance)
            if visibility > 0:
                r = int(color[0] * visibility)
                g = int(color[1] * visibility)
                b = int(color[2] * visibility)
                pygame.draw.rect(win, (r, g, b), (x, y, CELL_SIZE, CELL_SIZE))
            else:
                # Draw as dark gray if beyond visibility
                pygame.draw.rect(win, (20, 20, 20), (x, y, CELL_SIZE, CELL_SIZE))

def animate_path(win, path, color, delay=0.005):
    """Animate a path being drawn with a brief delay"""
    for pos in path:
        if maze[pos[0]][pos[1]] not in ['S', 'E']:
            pygame.draw.rect(win, color, 
                          (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()
            time.sleep(delay)

# Path visualization variables
ai_path = None
ai_path_bfs = None
showing_solution = False
showing_bfs_path = False

def fade_transition(surface1, surface2, steps=30):
    """Create a fade transition between two surfaces"""
    for alpha in range(0, 256, int(256/steps)):
        surface1.set_alpha(255 - alpha)
        win.blit(surface2, (0, 0))
        win.blit(surface1, (0, 0))
        pygame.display.update()
        time.sleep(0.01)

def show_intro_screen():
    global start_time
    
    # Create a background for the intro (could be a gradient or pattern)
    intro_bg = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        color_value = int(200 * y / HEIGHT) + 20
        pygame.draw.line(intro_bg, (0, color_value, color_value), (0, y), (WIDTH, y))
    
    intro = True
    title_angle = 0
    
    while intro:
        win.blit(intro_bg, (0, 0))
        
        # Create a rotating, pulsating title
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("Maze Adventure", True, (100, 255, 0))
        
        # Get the rect of the text surface
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # Create a rotated version of the text
        scale_factor = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() / 500)
        scaled_title = pygame.transform.scale(
            title_text, 
            (int(title_rect.width * scale_factor), int(title_rect.height * scale_factor))
        )
        scaled_rect = scaled_title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # Draw the title
        win.blit(scaled_title, scaled_rect)
        
        # Draw a glowing "Press ENTER to start" text
        glow_value = int(127 + 127 * math.sin(pygame.time.get_ticks() / 300))
        instruction_font = pygame.font.SysFont(None, 36)
        instruction_text = instruction_font.render("Press ENTER to start", True, (255, glow_value, glow_value))
        win.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2))
        
        # Draw controls with shadow
        shadow_offset = 2
        controls = [
            "Controls:",
            "- Move: W/A/S/D or Arrow Keys",
            "- Diagonal Move: Q/E/Z/C",
            "- Toggle A* AI Path: SPACE",
            "- Toggle BFS Path: P"
        ]
        
        control_font = pygame.font.SysFont(None, 24)
        for i, line in enumerate(controls):
            # Draw shadow
            shadow_text = control_font.render(line, True, (0, 0, 0))
            win.blit(shadow_text, (12 + shadow_offset, HEIGHT - 150 + i * 25 + shadow_offset))
            
            # Draw text
            text = control_font.render(line, True, (180, 180, 80))
            win.blit(text, (12, HEIGHT - 150 + i * 25))
        
        # Add some animated particles
        if random.random() < 0.1:  # 10% chance each frame
            create_particles(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                5
            )
        
        # Update and draw particles
        particles_to_remove = []
        for i, particle in enumerate(particles):
            if particle.update():
                particles_to_remove.append(i)
            particle.draw(win)
        
        # Remove dead particles
        for i in sorted(particles_to_remove, reverse=True):
            particles.pop(i)
        
        pygame.display.update()
        clock.tick(FPS)
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False
                    start_time = time.time()  # Start the timer when game begins

def show_message(message, color=(100, 255, 0), duration=1.5):
    """Display a message in the center of the screen"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 150), (0, 0, WIDTH, HEIGHT))
    win.blit(overlay, (0, 0))
    
    # Render the message
    font = pygame.font.SysFont(None, 72)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # Add a glow effect
    glow_surf = pygame.Surface((text_rect.width + 20, text_rect.height + 20), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf, (*color, 100), (0, 0, text_rect.width + 20, text_rect.height + 20))
    glow_surf = apply_gaussian_blur(glow_surf, 10)
    win.blit(glow_surf, (text_rect.x - 10, text_rect.y - 10))
    
    # Draw the message
    win.blit(text, text_rect)
    pygame.display.update()
    
    # Create particles at the text position
    create_particles(WIDTH // 2, HEIGHT // 2, color, 30)
    
    # Wait for specified duration
    pygame.time.delay(int(duration * 1000))

# Show intro screen before starting the game
show_intro_screen()

# Main game loop
run = True
show_fog_of_war = True  # Enable fog of war by default
path_animation_speed = 0.005  # Animation speed for paths

# Function to apply Gaussian blur using Pillow
def apply_gaussian_blur(surface, radius):
    array = pygame.surfarray.array3d(surface)
    image = Image.fromarray(array)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    return pygame.image.fromstring(blurred_image.tobytes(), surface.get_size(), "RGB")

while run:
    clock.tick(FPS)  # Control the frame rate
    
    # Clear the screen
    win.fill(BLACK)
    
    # Update particles
    particles_to_remove = []
    for i, particle in enumerate(particles):
        if particle.update():
            particles_to_remove.append(i)
        particle.draw(win)
    
    # Remove dead particles
    for i in sorted(particles_to_remove, reverse=True):
        if i < len(particles):  # Safety check
            particles.pop(i)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                showing_bfs_path = not showing_bfs_path
                if showing_bfs_path:
                    # Show BFS message and play sound
                    algorithm_sound.play()
                    algorithm_uses["BFS"] += 1
                    show_message("Applying BFS", (255, 100, 200))
                    
                    # Calculate BFS path
                    ai_path_bfs = bfs(maze, (player_x, player_y))
                    # Animate the path being drawn
                    if ai_path_bfs:
                        animate_path(win, ai_path_bfs, BFS_COLOR, path_animation_speed)

            elif event.key == pygame.K_SPACE:
                # Toggle AI solution
                showing_solution = not showing_solution
                if showing_solution:
                    # Show A* message and play sound
                    algorithm_sound.play()
                    algorithm_uses["A*"] += 1
                    show_message("Applying A*", (255, 215, 0))
                    
                    # Calculate the solution
                    ai_path = astar_search(maze, (player_x, player_y), (end_x, end_y))
                    # Animate the path being drawn
                    if ai_path:
                        animate_path(win, ai_path, ASTAR_COLOR, path_animation_speed)
            
            elif event.key == pygame.K_f:
                # Toggle fog of war
                show_fog_of_war = not show_fog_of_war
                show_message("Fog: " + ("ON" if show_fog_of_war else "OFF"), (100, 100, 255), 1.0)

            # Handle movement
            dx, dy = 0, 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                dx, dy = -1, 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                dx, dy = 1, 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx, dy = 0, -1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx, dy = 0, 1
            elif event.key == pygame.K_q:  # up-left
                dx, dy = -1, -1
            elif event.key == pygame.K_e:  # up-right
                dx, dy = -1, 1
            elif event.key == pygame.K_z:  # down-left
                dx, dy = 1, -1
            elif event.key == pygame.K_c:  # down-right
                dx, dy = 1, 1

            new_x = player_x + dx
            new_y = player_y + dy

            if 0 <= new_x < N and 0 <= new_y < N:
                if maze[new_x][new_y] in [1, 'E']:
                    # Play move sound and count the move
                    move_sound.play()
                    moves_made += 1
                    
                    # Create movement particles
                    create_particles(
                        player_y * CELL_SIZE + CELL_SIZE // 2,
                        player_x * CELL_SIZE + CELL_SIZE // 2,
                        BLUE, 5
                    )
                    
                    # Update player position
                    player_x, player_y = new_x, new_y
                    
                    if maze[player_x][player_y] == 'E':
                        # Victory!
                        win_sound.play()
                        elapsed_time = time.time() - start_time if start_time else 0
                        minutes = int(elapsed_time // 60)
                        seconds = int(elapsed_time % 60)
                        
                        # Create lots of celebratory particles
                        for _ in range(100):
                            create_particles(
                                random.randint(0, WIDTH),
                                random.randint(0, HEIGHT),
                                (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                                2
                            )
                        
                        # Show victory message with stats
                        victory_message = f"You Win! Time: {minutes}:{seconds:02d} Moves: {moves_made}"
                        show_message(victory_message, (0, 255, 0), 3.0)
    
    # Draw the maze with fog of war effect if enabled
    if show_fog_of_war:
        draw_maze_with_fog(win, maze, (player_x, player_y))
    else:
        # Draw maze normally
        for i in range(N):
            for j in range(N):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                if maze[i][j] == 0:
                    color = WALL_COLOR
                elif maze[i][j] == 1:
                    color = PATH_COLOR
                elif maze[i][j] == 'S':
                    color = GREEN
                elif maze[i][j] == 'E':
                    color = RED
                pygame.draw.rect(win, color, (x, y, CELL_SIZE, CELL_SIZE))
    
    # Draw BFS path if showing
    if showing_bfs_path and ai_path_bfs:
        for pos in ai_path_bfs:
            if maze[pos[0]][pos[1]] not in ['S', 'E']:
                pygame.draw.rect(win, BFS_COLOR, 
                               (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw A* path if showing
    if showing_solution and ai_path:
        for pos in ai_path:
            if maze[pos[0]][pos[1]] not in ['S', 'E']:
                pygame.draw.rect(win, ASTAR_COLOR, 
                               (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw player with glowing effect
    glow_radius = 5 + math.sin(time.time() * 5) * 2  # Pulsating glow
    glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (100, 100, 255, 100), (glow_radius, glow_radius), glow_radius)
    # Apply blur if available
    try:
        glow_surf = apply_gaussian_blur(glow_surf, 10)
    except:
        pass  # Skip blur if not available
    
    win.blit(glow_surf, (
        player_y * CELL_SIZE + CELL_SIZE // 2 - glow_radius,
        player_x * CELL_SIZE + CELL_SIZE // 2 - glow_radius
    ))
    
    # Draw player
    pygame.draw.circle(
        win,
        BLUE,
        (player_y * CELL_SIZE + CELL_SIZE // 2, player_x * CELL_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 3,
    )
    
    # Draw controls and stats
    draw_controls(win)
    draw_stats(win)
    
    pygame.display.update()

pygame.quit()