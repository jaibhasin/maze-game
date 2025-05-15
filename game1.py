import random
import pygame
import heapq
import time


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

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze with AI Solver")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)  

# Find start position and end position
player_x, player_y = 0, 0
end_x, end_y = 0, 0
for i in range(N):
    for j in range(N):
        if maze[i][j] == 'S':
            player_x, player_y = i, j
        elif maze[i][j] == 'E':
            end_x, end_y = i, j

def bfs(maze , start):
    queue = [start]
    visited = set()
    visited.add(start)
    parent = {start:None}

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
# A* search algorithm
def astar_search(maze, start, end):
    def heuristic(pos, end):
        return abs(pos[0] - end[0]) + abs(pos[1] - end[1]) # this is the Manhattan distance
    
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, end), start))
    
    # Dict to track where we came from
    came_from = {}
    
    # Cost to reach each node from start
    g_score = {start: 0}
    
    while open_set:

        # Get the node with lowest f_score
        current_f, current = heapq.heappop(open_set)
        
        # If we reached the end
        if current == end:
            # Reconstruct the path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            # print('okoko checkong 2')
            return path[::-1]  # Reverse to get start-to-end
            # print('okoko checkong 2')
        
        # Check neighbors
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Check if neighbor is valid
            if 0 <= neighbor[0] < N and 0 <= neighbor[1] < N:
                if maze[neighbor[0]][neighbor[1]] == 0:  # Wall
                    continue
                
                move_cost = 1
                
                # g_score is cost to reach the neighbor from start 
                tentative_g = g_score.get(current, float('inf')) + move_cost
                

                # If this path is better than any previous one
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)                    
                    heapq.heappush(open_set, (f_score, neighbor))
    
    return None  

# Find the solution path
ai_path = None
ai_path_bfs = None
showing_solution = False
showing_bfs_path = False

def draw_controls(win):
    font = pygame.font.SysFont(None, 24)
    controls = [
        "Controls:",
        "- Move: W/A/S/D or Arrow Keys",
        "- Diagonal Move: Q/E/Z/C",
        "- Toggle A* AI Path: SPACE",
        "- Toggle BFS Path: P"
    ]
    for i, line in enumerate(controls):
        text = font.render(line, True, (100, 100, 50))
        win.blit(text, (10, HEIGHT - 100 + i * 20))  # Adjust Y position as needed


def show_intro_screen():
    intro = True
    while intro:
        win.fill(BLACK)
        # Draw title
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("Maze Game", True, (100, 255, 0))
        win.blit(title_text, (WIDTH // 2 - 150, HEIGHT // 3))
        
        # Draw instructions
        instruction_font = pygame.font.SysFont(None, 36)
        instruction_text = instruction_font.render("Press ENTER to start", True, (255, 255, 255))
        win.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2))
        
        # Draw controls
        draw_controls(win)
        
        pygame.display.update()
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    intro = False

# Show intro screen before starting the game
show_intro_screen()



run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print("Now Applying BFS")
                showing_bfs_path = not showing_bfs_path
                if showing_bfs_path:
                    ai_path_bfs = bfs(maze, (player_x, player_y))
                    font = pygame.font.SysFont(None, 72)
                    text = font.render("Now Applying BFS", True, (100, 255, 0))
                    win.blit(text, (WIDTH // 2 - 230, HEIGHT // 2 - 30))
                    pygame.display.update()
                    time.sleep(2)  # Pause after showing the message

            if event.key == pygame.K_SPACE:
                # Toggle AI solution
                showing_solution = not showing_solution
                if showing_solution :
                    # Calculate the solution only once
                    ai_path = astar_search(maze, (player_x, player_y), (end_x, end_y))
                    font = pygame.font.SysFont(None, 72)
                    text = font.render("Now Applying A*", True, (100, 255, 0))
                    win.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 30))
                    pygame.display.update()
                    time.sleep(2)  # Pause after showing the message

                    # print("checking3")
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
                    player_x, player_y = new_x, new_y
                    
                    if maze[player_x][player_y] == 'E':
                        print("🎉 You Win!")
                        font = pygame.font.SysFont(None, 72)
                        text = font.render("You Win!", True, (0, 255, 0))
                        win.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
                        pygame.display.update()
    
    # Draw maze
    for i in range(N):
        for j in range(N):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if maze[i][j] == 0:
                color = BLACK
            elif maze[i][j] == 1:
                color = WHITE
            elif maze[i][j] == 'S':
                color = GREEN
            elif maze[i][j] == 'E':
                color = RED
            pygame.draw.rect(win, color, (x, y, CELL_SIZE, CELL_SIZE))
    
    if showing_bfs_path and ai_path_bfs:
        for pos in ai_path_bfs:
            if maze[pos[0]][pos[1]] not in ['S', 'E']:
                pygame.draw.rect(win, (100,20,30), 
                                (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if showing_solution and ai_path:
        # print("checking4")
        for pos in ai_path:
            if maze[pos[0]][pos[1]] not in ['S', 'E']:
                pygame.draw.rect(win, YELLOW, 
                                (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.draw.circle(
        win,
        BLUE,
        (player_y * CELL_SIZE + CELL_SIZE // 2, player_x * CELL_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 3,
    )
    pygame.display.update()

pygame.quit()
