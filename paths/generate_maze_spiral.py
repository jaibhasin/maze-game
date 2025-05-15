import random

N = 50

# 0 = wall, 1 = path
maze = [[0 for _ in range(N)] for _ in range(N)]  



import math
# spiral
def is_valid(x, y):
    cx, cy = N // 2, N // 2
    dx, dy = x - cx, y - cy
    r = math.hypot(dx, dy)
    theta = math.atan2(dy, dx)
    return (0 <= x < N and 0 <= y < N and 
            (r < (theta + math.pi) * N / (2 * math.pi)) and maze[x][y] == 0)




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
            # Count adjacent path cells
            count = 0
            for ddx, ddy in dirs:
                adjx, adjy = nx + ddx, ny + ddy
                if (0 <= adjx < N and 0 <= adjy < N and 
                    (adjx - N//2)**2 + (adjy - N//2)**2 <= (N//2)**2 and
                    maze[adjx][adjy] == 1):
                    count += 1
            if count <= 1:
                build_maze(nx, ny)


def print_maze():
    cx, cy = N // 2, N // 2
    radius = N // 2
    for i in range(N):
        for j in range(N):
            if (i - cx)**2 + (j - cy)**2 > radius**2:
                print(' ', end=' ')
            elif (i, j) == (0, 0):
                print('S', end=' ')
            elif (i, j) == (N - 1, N - 1):
                print('E', end=' ')
            else:
                print(maze[i][j], end=' ')
        print()


# def get_maze():
#     build_maze(0, 0)
#     maze[0][0] = 'S'
#     maze[N-1][N-1] = 'E'
#     return maze

def get_maze():
    start_x, start_y = N // 2, N // 2  # Start from center
    build_maze(start_x, start_y)
    maze[start_x][start_y] = 'S'
    # maze[N - 1][N - 1] = 'E'  # You can move this if you want a better end point
    opc = 1
    for i in range(N):
        for j in range(N):
            if maze[i][j] == 1:
                opc += 1
                if opc == 25:
                    maze[i][j] = 'E'
                    break
    return maze



# Example usage
if __name__ == "__main__":
    get_maze()
    print_maze()
