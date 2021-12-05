# 미로 만들기
import random
import time
import pygame
from pygame.locals import *

# 각각의 방향에 대한 값 (4방향 모두 꽉 차있다고 하면 15란 값을 가진다.)
UP = 8
RIGHT = 4
DOWN = 2
LEFT = 1
MULTIPASS = 2

# pygame에 필요한 상수들 정의
FPS = 20
Margin = (10, 10, 10, 10)       # Left, Top, Right, Bottom
CellSize = 20
Start, End = (0, 0), (0, 0)

# maze에 통로를 만드는 함수
def mazesplit(maze, lt, rb):
    # 가로와 세로의 크기가 모두 1이면 종료
    if lt == rb: return
    # 통로를 만들 선택이 세로인 경우
    if lt[0] == rb[0] or (lt[1] != rb[1] and random.randrange(0, 2) == 0):
        u = random.randrange(lt[1], rb[1])
        for _ in range(MULTIPASS):
            v = random.randrange(lt[0], rb[0]+1)
            if (maze[u][v] & DOWN) == 0: continue
            # 위에 있는 칸에서는 아래쪽에 통로를 만들고
            maze[u][v] -= DOWN
            # 아래에 있는 칸에서는 위쪽에 통로를 만듭니다.
            maze[u+1][v] -= UP
        # 나누어진 칸에 대해서 mazesplit을 실행합니다.
        mazesplit(maze, lt, (rb[0], u))
        mazesplit(maze, (lt[0], u+1), rb)
    # 통로를 만들 선택이 가로인 경우
    else:
        v = random.randrange(lt[0], rb[0])
        for _ in range(MULTIPASS):
            u = random.randrange(lt[1], rb[1]+1)
            if (maze[u][v] & RIGHT) == 0: continue
            # 왼쪽에 있는 칸에서는 오른쪽에 통로를 만들고
            maze[u][v] -= RIGHT
            # 오른쪽에 있는 칸에서는 왼쪽에 통로를 만듭니다.
            maze[u][v+1] -= LEFT
        mazesplit(maze, lt, (v, rb[1]))
        mazesplit(maze, (v+1, lt[1]), rb)

def mazeprint(maze, n, m, path):
    '''
    for r in range(n):
        str = "+"
        for c in range(m):
            if (maze[r][c] & UP) != 0: str += "--+"
            else: str += "  +"
        print(str)
        str = "|"
        for c in range(m):
            if (maze[r][c] & RIGHT) != 0: str += "  |"
            else: str += "   "
        print(str)
    print("+"+"--+"*m)
    '''

    surface.fill((255, 255, 255))
    for r in range(n):
        # 셀에서 위에 있는 줄 그리기 
        for c in range(m):
            if (maze[r][c] & UP) != 0:
                pygame.draw.line(surface, (0, 0, 0), \
                    (Margin[0] + c*CellSize, Margin[1] + r*CellSize), \
                    (Margin[0] + c*CellSize + CellSize, Margin[1] + r*CellSize))
        # 셀에서 왼쪽에 있는 줄 그리기
        for c in range(m):
            if(maze[r][c] & LEFT) != 0:
                pygame.draw.line(surface, (0, 0, 0), \
                    (Margin[0] + c*CellSize, Margin[1] + r*CellSize), \
                    (Margin[0] + c*CellSize, Margin[1] + r*CellSize + CellSize))
    pygame.draw.line(surface, (0, 0, 0), \
        (Margin[0] + m*CellSize, Margin[1]), \
        (Margin[0] + m*CellSize, Margin[1] + n*CellSize))
    pygame.draw.line(surface, (0, 0, 0), \
        (Margin[0], Margin[1] + n*CellSize), \
        (Margin[0] + m*CellSize, Margin[1] + n*CellSize))

    # Draw Start & End position
    pygame.draw.rect(surface, (128, 128, 255), \
        (Margin[0] + Start[0]*CellSize + CellSize//2-3, \
         Margin[1] + Start[1]*CellSize + CellSize//2-3, \
         6, 6))
    pygame.draw.rect(surface, (255, 128, 128), \
        (Margin[0] + End[0]*CellSize + CellSize//2-3, \
         Margin[1] + End[1]*CellSize + CellSize//2-3, \
         6, 6))

    # 현재까지의 경로 출력
    if len(path) > 1:
        pygame.draw.lines(surface, (0, 255, 0), False, path, 4)

    # 디스플레이 서피스를 업데이트
    pygame.display.update()

    # FPS 시간이 맞게 잠시 딜레이를 줌
    time.sleep(1/FPS)

# dfs 함수
def dfs(maze, n, m, c, path):
    # 현재 미로를 출력
    mazeprint(maze, n, m, path)
    # 도착지점에 왔으면 끝냄
    if c == End: return 1
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            return -1
    visit[c[1]][c[0]] = True
    # 오른쪽이 열려있으면
    if (maze[c[1]][c[0]] & RIGHT) == 0:
        nc = (c[0]+1, c[1])
        if not visit[nc[1]][nc[0]]:
            path.append((Margin[0]+nc[0]*CellSize+CellSize//2, \
                         Margin[1]+nc[1]*CellSize+CellSize//2))
            ret = dfs(maze, n, m, nc, path)
            if ret == 1 or ret == -1: return ret
            path.pop()
    # 아래쪽이 열려있으면
    if (maze[c[1]][c[0]] & DOWN) == 0:
        nc = (c[0], c[1]+1)
        if not visit[nc[1]][nc[0]]:
            path.append((Margin[0]+nc[0]*CellSize+CellSize//2, \
                         Margin[1]+nc[1]*CellSize+CellSize//2))
            ret = dfs(maze, n, m, nc, path)
            if ret == 1 or ret == -1: return ret
            path.pop()
    # 왼쪽이 열려있으면
    if (maze[c[1]][c[0]] & LEFT) == 0:
        nc = (c[0]-1, c[1])
        if not visit[nc[1]][nc[0]]:
            path.append((Margin[0]+nc[0]*CellSize+CellSize//2, \
                         Margin[1]+nc[1]*CellSize+CellSize//2))
            ret = dfs(maze, n, m, nc, path)
            if ret == 1 or ret == -1: return ret
            path.pop()
    # 위쪽이 열려있으면
    if (maze[c[1]][c[0]] & UP) == 0:
        nc = (c[0], c[1]-1)
        if not visit[nc[1]][nc[0]]:
            path.append((Margin[0]+nc[0]*CellSize+CellSize//2, \
                         Margin[1]+nc[1]*CellSize+CellSize//2))
            ret = dfs(maze, n, m, nc, path)
            if ret == 1 or ret == -1: return ret
            path.pop()
    # 현재 미로를 출력
    mazeprint(maze, n, m, path)
    # 못 찾은 경우 
    return 0

n, m = map(int, input("세로의 크기와 가로의 크기 입력 :  ").split())
CellSize = min(800//m, 600//n)

# pygame 초기화
pygame.init()

# 그림을 그릴 디스플레이 서피스를 생성
width = Margin[0] + Margin[2] + m*CellSize
height = Margin[1] + Margin[3] + n*CellSize
surface = pygame.display.set_mode((width, height))

# maze 생성
maze = [ [15]*m for _ in range(n) ]

# 시작점과 끝점 생성
Start = (0, random.randrange(n))
End = (m-1, random.randrange(n)) 

# maze에 통로를 만듭니다.
mazesplit(maze, (0, 0), (m-1, n-1))

# 길찾기를 합니다 (DFS 알고리즘) 
path = [ (Margin[0]+Start[0]*CellSize+CellSize//2, \
          Margin[1]+Start[1]*CellSize+CellSize//2) ]
visit = [ [False]*m for _ in range(n) ]
dfs(maze, n, m, Start, path)

# pygame 닫기가 눌릴 때까지 기다림
isQuit = False
while not isQuit:
    # maze를 출력합니다.
    mazeprint(maze, n, m, path)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            isQuit = True
            break

# pygame 종료
pygame.quit()
