import random

N = 50

maze = [[0 for _ in range(N)] for _ in range(N)]  # 0 = wall, 1 = path    


def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N and maze[x][y] == 0

def build_maze(x, y):
    maze[x][y] = 1

    dirs = [
    (1, 0), (-1, 0), (0, 1), (0, -1),  
    (1, 1), (1, -1), (-1, 1), (-1, -1)  
    ]
    random.shuffle(dirs)  

    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny):
            # Count number of adjacent path cells (to avoid loops)
            count = 0
            for ddx, ddy in dirs:
                adjx, adjy = nx + ddx, ny + ddy
                if 0 <= adjx < N and 0 <= adjy < N and maze[adjx][adjy] == 1:
                    count += 1
            if count <= 1:
                build_maze(nx, ny)

def print_maze():
    for i in range(N):
        for j in range(N):
            if (i, j) == (0, 0):
                print('S', end=' ')
            elif (i, j) == (N-1, N-1):
                print('E', end=' ')
            else:
                print(maze[i][j], end=' ')
        print()



def get_maze():
    build_maze(0, 0)
    maze[0][0] = 'S'
    maze[49][49] = 'E'
    return maze