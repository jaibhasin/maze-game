import random

N = 50

maze = [[0 for _ in range(N)] for _ in range(N)]  # 0 = wall, 1 = path    

def is_valid(x, y):
    cx, cy = N // 2, N // 2
    return (0 <= x < N and 0 <= y < N and 
            abs(x - cx) + abs(y - cy) <= N // 2 and maze[x][y] == 0)



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
    build_maze(N//2,N//2)
    maze[N//2][N//2] = 'S'  # currently we changed starting position so 49,49 is not reachable 
    # maze[49][49] = 'E'
    temp_1 = 1
    for i in range(N):
        for j in range(N):
            if maze[i][j] == 1:
                temp_1 += 1
                if temp_1 == 25:
                    maze[i][j] = 'E'
                    break
    return maze

# def check1():
#     build_maze(0, 0)
#     print_maze()
# check1()