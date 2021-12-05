# Tic-Tae-Toe Temporal Difference Game
# Random module import
import random


class TicTaeToe:
    def __init__(self):
        self.board = [0] * 9
        self.aiTurn = random.randrange(1, 3)

    # turn이 pos 위치에 놓는다.
    def Put(self, turn, pos):
        self.board[pos] = turn

    # 경기가 끝났는지 검사
    def IsFinished(self):
        # 가로 검사
        for i in range(3):
            x = self.board[i * 3]
            if x == 0: continue
            isFinish = True
            for j in range(3):
                if x != self.board[i * 3 + j]:
                    isFinish = False
                    break
            if isFinish: return x
        # 세로 검사
        for i in range(3):
            x = self.board[i]
            if x == 0: continue
            isFinish = True
            for j in range(3):
                if x != self.board[i + j * 3]:
                    isFinish = False
                    break
            if isFinish: return x
        # 대각선 검사
        isFinish = True
        x = self.board[0]
        if x != 0:
            for i in range(3):
                if x != self.board[i * 4]:
                    isFinish = False
                    break
            if isFinish: return x

        # 대각선 검사
        isFinish = True
        x = self.board[2]
        if x != 0:
            for i in range(3):
                if x != self.board[i * 2 + 2]:
                    isFinish = False
                    break
            if isFinish: return x
        # all board is full
        isFinish = True
        for i in range(9):
            if self.board[i] == 0:
                isFinish = False
                break
        if isFinish: return 0
        return -1

    def Print(self):
        tt = (" ", "0", "X")
        print("+---+---+---+")
        print(f"| {tt[self.board[0]]} | {tt[self.board[1]]} | {tt[self.board[2]]} |")
        print("+---+---+---+")
        print(f"| {tt[self.board[3]]} | {tt[self.board[4]]} | {tt[self.board[5]]} |")
        print("+---+---+---+")
        print(f"| {tt[self.board[6]]} | {tt[self.board[7]]} | {tt[self.board[8]]} |")
        print("+---+---+---+")

    # 현재의 보드 상태를 숫자로 변환
    def GetState(self):
        state = 0
        for k in self.board:
            state = state*3 + k
        return state

    # p에 놓았을 경우 다음 상태를 반환
    def GetNextState(self, turn, p):
        nb = [k for k in self.board]
        nb[p] = turn
        state = 0
        for k in nb:
            state = state * 3 + k
        return state

# 모든 상태에 대해서 기대값을 기록할 상태공간 생성
import os.path
if os.path.isfile('ttt-td.sav'):
    with open('ttt-td.sav', 'r') as f:
        ss = list(map(float, f.readline().split()))

else:
    ss = [0.0] * (3**9)
lr = 0.1  # learning rate (lambda)

#  무한하게 게임 진행
while True:
    game = TicTaeToe()
    turn = 1
    # 에피소드를 저장할 리스트 생성
    ep = []
    while game.IsFinished() == -1:
        # 현재 상태를 에피소드에 저장
        ep.append(game.GetState())
        game.Print()
        cand = []
        for i in range(9):
            if game.board[i] == 0: cand.append(i)
        if turn == game.aiTurn:
            p, maxv = 0, -100.0
            mt = (1 if game.aiTurn == 1 else -1)
            board = [k for k in game.board]
            # 둘 수 있는 후보들에 대해
            for c in cand:
                ns = game.GetNextState(turn, c)
                board[c] = ss[ns]*mt
                if maxv < ss[ns] * mt: p, maxv = c, ss[ns] * mt
            print(*board)
            game.Put(turn, p)
        else:
            while True:
                p = int(input("pos : "))
                if p in cand: break
            game.Put(turn, p)
        turn ^= 3
    # 결과 에피소드를 저장
    ep.append(game.GetState())
    game.Print()
    rtext = ("Draw", "O Win", "X Win")
    win = game.IsFinished()
    print(rtext[win])
    # 에피소드 결과에 따라 보상값을 계산
    if win == 1 : reward = 1
    elif win == 2 : reward = -1
    else : reward = 0
    # 모든 에피소드에 대해서
    for e in ep:
        ss[e] += lr * (reward - ss[e])
    yn = input("Do you want more game : ")
    if yn != 'y' and yn != 'Y': break

with open('ttt-td.sav', 'w') as f:
    f.write(' '.join(map(str, ss)))
