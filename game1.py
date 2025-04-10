from generate_maze import get_maze
import pygame

maze = get_maze() 
N = len(maze)

CELL_SIZE = 10
WIDTH = HEIGHT = N * CELL_SIZE

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Find start position
for i in range(N):
    for j in range(N):
        if maze[i][j] == 'S':
            player_x, player_y = i, j

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
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

            # Stay inside bounds and move only on path or end
            if 0 <= new_x < N and 0 <= new_y < N:
                if maze[new_x][new_y] in [1, 'E']:
                    player_x, player_y = new_x, new_y
                    if maze[player_x][player_y] == 'E':
                        print("🎉 You Win!")
                        font = pygame.font.SysFont(None, 72)
                        text = font.render("🎉 You Win!", True, (0, 255, 0))
                        win.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 30))
                        pygame.display.update()
                        pygame.time.delay(3000)
                        # run = False
    # Draw maze
    for i in range(N):
        for j in range(N):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            if maze[i][j] == 0:
                color = BLACK
            elif maze[i][j] == 1:
                color = WHITE
            elif maze[i][j] == 'S' or maze[player_x][player_y] == 'E':
                color = GREEN
            elif maze[i][j] == 'E':
                color = RED
            pygame.draw.rect(win, color, (x, y, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.circle(
        win,
        BLUE,
        (player_y * CELL_SIZE + CELL_SIZE // 2, player_x * CELL_SIZE + CELL_SIZE // 2),
        CELL_SIZE // 3,
    )

    pygame.display.update()

pygame.quit()
