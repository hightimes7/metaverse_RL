# nxm 슬라이딩 퍼즐 섞어놓기
import random
import time
import pygame
from pygame.locals import *

Margin = 10
FPS = 20

# puzzle class
class Puzzle:
    # n : 세로칸의 크기, m : 가로칸의 크기
    def __init__(self, n, m):
        self.n = n
        self.m = m
        # 셀의 크기를 결정하도록 함
        self.size = min(640//m, 400//n)

        # 퍼즐을 초기화하고 퍼즐을 랜덤하게 섞어놓기 
        puzzle = [ [r*m+c+1 for c in range(m) ] for r in range(n) ]

        # 비어있는 곳의 위치 설정
        self.emptyr, self.emptyc = n-1, m-1

        # n*m*100번에 걸쳐서 섞어놓기
        for _ in range(n*m*100):
            v = random.randrange(4)
            r, c = self.emptyr, self.emptyc
            drc = ( (0, 1), (1, 0), (0, -1), (-1, 0) )
            nr, nc = r+drc[v][0], c+drc[v][1]
            # 옮겨야할 셀 위치가 퍼즐 위치를 벗어나는 경우 무시 
            if nr < 0 or nr >= n or nc < 0 or nc >= m: continue
            puzzle[r][c] = puzzle[nr][nc]
            # 비어있는 위치 업데이트
            self.emptyr, self.emptyc = nr, nc            

        # 비어있는 칸의 숫자 넣기 
        puzzle[self.emptyr][self.emptyc] = 0
        self.puzzle = puzzle

        # pygame 초기화
        pygame.init()

        # 그림을 그릴 디스플레이를 설정
        self.display = pygame.display.set_mode((Margin*2+m*self.size, 
                                          Margin*2+n*self.size))

        # 텍스트를 설정할 폰트 생성
        self.font = pygame.font.Font('freesansbold.ttf', self.size//2-1)

    # 퍼즐이 다 맞았는지 검사
    def checkPuzzle(self):
        for r in range(self.n):
            for c in range(self.m):
                if (r != self.n-1 or c != self.m-1) and \
                self.puzzle[r][c] != r*self.m + c + 1: return 1
        return 0

    # 퍼즐의 셀이 클릭된 경우 처리
    def onClick(self, r, c):
        drc = ((0, 1), (1, 0), (0, -1), (-1, 0))
        er, ec = self.emptyr, self.emptyc
        puzzle = self.puzzle
        for dr, dc in drc:
            if r == er+dr and c == ec+dc:
                puzzle[er][ec] = puzzle[r][c]
                puzzle[r][c] = 0
                self.emptyr, self.emptyc = r, c
                return self.checkPuzzle()       
        return -1
    
    # 루프 돌기. False 반환시 종료
    def update(self):
        # 이벤트 처리
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                return False
            # 마우스 입력이 들어온 경우 처리
            if e.type == MOUSEBUTTONUP:
                r, c = (e.pos[1]-Margin)//self.size, (e.pos[0]-Margin)//self.size
                # 영역 밖 클릭한 경우 무시 
                if r < 0 or r >= self.n or c < 0 or c >= self.m: continue
                # onClick 실행
                # return : 0 - 게임 종료, 1 - 지속, -1 - 잘못 누른경우 
                ret = self.onClick(r, c)
                if ret != -1: return bool(ret)
        return True

    # 그림 그리기
    def draw(self):
            
        # 윈도우를 하얀색으로 클리어
        display = self.display
        display.fill( (255, 255, 255) )

        # 슬라이딩 퍼즐 그림 그리기
        puzzle = self.puzzle
        for r in range(self.n):
            for c in range(self.m):
                # 박스 그리기 
                color = (250, 250, 250)
                if puzzle[r][c] == 0: color = (100, 100, 100)
                pygame.draw.rect(display, color, (Margin+c*self.size, 
                    Margin+r*self.size, self.size, self.size))
                pygame.draw.rect(display, (0, 0, 0), (Margin+c*self.size, 
                    Margin+r*self.size, self.size, self.size),1)
                # 박스 안에 글자 쓰기
                if puzzle[r][c] == 0: continue
                text = self.font.render(str(puzzle[r][c]), True, (0, 0, 0))
                rect = text.get_rect()
                rect.center = (Margin+c*self.size+self.size//2,
                               Margin+r*self.size+self.size//2)
                display.blit(text, rect)
                
        # 디스플레이 업데이트
        pygame.display.update()
        # FPS에 맞게 잠을 잡니다
        time.sleep(1/FPS)
        # 기본은 True를 반환 
        return True

    # 종료
    def shutdown(self):
        pygame.quit()
        
n, m = map(int, input('세로와 가로의 크기 입력 : ').split())
puzzle = Puzzle(n, m)

quitFlag = -1
while quitFlag < FPS*3:
    if quitFlag == -1 and puzzle.update() == False: quitFlag = 0
    puzzle.draw()
    if quitFlag != -1 : quitFlag += 1
puzzle.shutdown()


'''
# 퍼즐 출력하기
fmt = '{:^3}|'
for r in range(n):
    print('+' + '---+'*m)
    s = '|'
    for c in range(m):
        if r == puzzle.emptyr and c == puzzle.emptyc: s += fmt.format('')
        else: s += fmt.format(puzzle.puzzle[r][c])
    print(s)
print('+' + '---+'*m)
'''        
