# 오목 프로그램 작성

import random
import time
import pygame
from pygame.locals import *

Margin = 10                 # 여유공간
CellSize = 50               # 줄과 줄 사이의 크기
CellSize2 = CellSize//2     # CellSize의 절반 크기
FPS = 30

# 오목 클래스 (9*9)
class Omok:
    # 클래스 초기화
    def __init__(self):
        # 0 : 비어있는 칸, 1 : 검은돌, 2 : 흰돌
        self.board = [ [0]*9 for _ in range(9) ]

        # pygame 초기화
        pygame.init()

        # 디스플레이 서피스 얻어오기
        self.display = pygame.display.set_mode(
            (Margin*2 + CellSize*9, Margin*2 + CellSize*9))

        # board 이미지 읽어오기
        self.boardImg = pygame.image.load('board.png')
        self.boardImg = pygame.transform.smoothscale(self.boardImg,
            (CellSize*9, CellSize*9))

        # 시작하는 돌은 검은 돌로 시작하도록 함
        self.turn = 1

        # 마지막에 놓은 돌의 위치를 저장
        self.lastPos = None

        # 프레임의 수치값 저장
        self.frames = 0
        
    # 그리기
    def draw(self):
        # 윈도우 클리어
        self.display.fill( (255, 255, 255) )

        # 보드 이미지를 화면에 그리기
        rt = self.boardImg.get_rect()
        rt.topleft = (Margin, Margin)
        self.display.blit(self.boardImg, rt)

        # 화면에 줄 긋기
        for i in range(9):
            pygame.draw.line(self.display,
                (0, 0, 0), (Margin + CellSize2, Margin + CellSize2 + i*CellSize),
                (Margin + CellSize2 + 8*CellSize, Margin + CellSize2 + i*CellSize))
            pygame.draw.line(self.display,
                (0, 0, 0), (Margin + CellSize2 + i*CellSize, Margin + CellSize2),
                (Margin + CellSize2 + i*CellSize, Margin + CellSize2 + 8*CellSize))

        # 화면에 돌 그리기
        board = self.board
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0: continue
                color = (0, 0, 0) if board[r][c] == 1 else (255, 255, 255)
                # 그림자
                pygame.draw.circle(self.display, (100, 100, 100),
                    (Margin + CellSize2 + c*CellSize+2, Margin + CellSize2 + r*CellSize+2),
                    CellSize2-5)
                pygame.draw.circle(self.display, (100, 100, 100),
                    (Margin + CellSize2 + c*CellSize+1, Margin + CellSize2 + r*CellSize+1),
                    CellSize2-5)
                # 돌
                pygame.draw.circle(self.display, color,
                    (Margin + CellSize2 + c*CellSize, Margin + CellSize2 + r*CellSize),
                    CellSize2-5)

        # 마지막에 놓을 돌 위치 표시
        if self.lastPos != None and self.frames%FPS < FPS*3//4 :
            r, c = self.lastPos
            pygame.draw.circle(self.display, (255, 0, 0),
                (Margin + CellSize2 + c*CellSize, Margin + CellSize2 + r*CellSize),
                5)
        
        # 디스플레이 적용
        pygame.display.update()

        # 딜레이
        time.sleep(1/FPS)

        # 프레임 증가
        self.frames += 1

    # (r, c) 위치에 돌 놓기
    def onPlace(self, r, c):
        # (r, c) 위치에 turn(검은돌 or 흰돌)을 놓음 
        self.board[r][c] = self.turn        
        # 마지막에 놓은 돌의 위치 저장
        self.lastPos = (r, c)
        # 마지막 위치의 돌을 놓았을 때, 몇개가 같은 줄에 있는지 세기
        drc = ((0, 1), (1, 1), (1, 0), (1, -1))
        for dr, dc in drc:
            count = 1
            for i in range(1, 6):
                nr, nc = r+dr*i, c+dc*i
                if nr < 0 or nr >= 9 or nc < 0 or nc >= 9: break
                if self.board[nr][nc] != self.turn: break
                count += 1
            for i in range(1, 6):
                nr, nc = r-dr*i, c-dc*i
                if nr < 0 or nr >= 9 or nc < 0 or nc >= 9: break
                if self.board[nr][nc] != self.turn: break
                count += 1
            if count == 5:
                print(f'{self.turn} win!!')
                return False
        # 다음 턴에 해당하는 돌로 바꿈 
        self.turn ^= 3
        return True

    # 게임 업데이트
    def update(self):
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                return False
            # 마우스 입력 처리
            if e.type == MOUSEBUTTONUP:
                r, c = (e.pos[1]-Margin)//CellSize, (e.pos[0]-Margin)//CellSize
                # 영역 밖이 클릭된 경우에는 처리하지 않음
                if r < 0 or r >= 9 or c < 0 or c >= 9: continue
                # 이미 돌이 있는 경우에도 처리하지 않음
                if self.board[r][c] != 0: continue
                return self.onPlace(r, c)
        return True

    # 게임 종료
    def shutdown(self):
        pygame.quit()

game = Omok()
# quitFlag는 지연 종료를 위한 변
quitFlag = -1
while quitFlag < FPS * 10:
    if quitFlag == -1 and not game.update(): quitFlag = 0
    game.draw()
    if quitFlag != -1: quitFlag += 1
game.shutdown()
