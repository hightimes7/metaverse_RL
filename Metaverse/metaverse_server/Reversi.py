# Reversi.py
"""
1) join playerName
  게임에 참여한다
  ret : a. Black or White, b. Refuse
2) board 
    '0123' 0 : 놓을 수 있는 곳, 1 : white, 2 : black, 3 : 놓을 수 없는 곳
3) put playerName postion
  리버시 position 위치에 돌을 올려놓는다
  ret : success, fail

"""

class Reversi:
    def __init__(self):
        self.board = [3]*64
        # 플레이어들이 현재 접속 안 되어 있다고 표시
        self.players = [0, None, None]
        self.turn = 0

    def onStart(self):
        self.board = [3]*64
        self.board[27], self.board[28] = 1, 2
        self.board[35], self.board[36] = 2, 1
        self.board[20], self.board[29] = 0, 0
        self.board[34], self.board[43] = 0, 0
        self.turn = 1
        self.hintCount = 4

    def onJoin(self, ss):
        if self.players[1] == None:
            self.players[1] = ss[1]
            ret = "white"
            self.players[0] += 1
        elif self.players[2] == None:
            self.players[2] = ss[1]
            ret = "black"
            self.players[0] += 1
        else: return "refuse"
        print(f"{ss[1]}이 게임에 {ret}로 참여합니다.")
        # 현재 플레이어 2명이 모였으면 플레이를 시작하도록 합니다.
        if self.players[0] == 2:
            self.onStart()
        return ret

    def onBoard(self):
        turnColor = ("none", "white", "black")
        ret = "".join(list(map(str, self.board))) + f" {turnColor[self.turn]}"
        return ret

    def onQuit(self):
        # 끝났으면, 스코어를 기록하도록 합니다.
        w, b = 0, 0
        for t in self.board:
            if t == 1: w += 1
            elif t == 2: b += 1
        # players를 초기화하도록 합니다.
        self.players = [ 0, None, None ]
        self.turn = 0
        # 결과값을 만듭니다.
        return f'quit {w} {b}'
        
    def onLeave(self, ss):
        # ss[1]이 플레이어에 있는지 검사한다.
        for i in range(1, 3):
            if self.players[i] == ss[1]:
                self.players[i] = None
                self.players[0] -= 1
                return f"leave {ss[1]} success"
        return f"leave {ss[1]} fail"

    def onPlace(self, ss):
        # place 명령을 실행한 플레이어가 현재 턴 소유자가 아니면 무시한다.
        if self.players[self.turn] != ss[1]: return f"fail"
        p = int(ss[2])
        # 놓을 위치가 놓을 수 없는 위치인 경우 무시한다.
        if self.board[p] != 0: return f"fail"
        # 보드의 p 위치에 돌을 놓습니다.
        self.board[p] = self.turn
        # p위치에 돌을 놓을 경우 바뀌어야할 돌들의 리스트를 얻어옵니다.
        flips = Reversi.getFlips(self.board, p, self.turn)
        # 플립될 돌들에 대해서 내 돌로 플립한다.
        for ft in flips: self.board[ft] = self.turn
        # 현재 턴을 상대 턴으로 바꾼다.
        self.turn ^= 3
        # 이 턴에서 놓을 수 있는 위치를 계산한다.
        if Reversi.getHints(self.board, self.turn) > 0: return self.onBoard()
        # 이전 턴에서 놓을 수 있는 위치가 없는 경우이므로 다시 턴을 돌린다.
        self.turn ^= 3
        # 이 턴에서 놓을 수 있는 위치를 계산한다.
        if Reversi.getHints(self.board, self.turn) > 0: return self.onBoard()
        # 두 턴 모두 놓을 수 있는 위치가 없으므로 게임을 종료한다.
        return self.onQuit()

    def runCommand(self, s):
        ss = s.split()
        if ss[0] == "join": return self.onJoin(ss)
        if ss[0] == "board": return self.onBoard()
        if ss[0] == "place": return self.onPlace(ss)
        if ss[0] == "leave": return self.onLeave(ss)

    def getFlips(board, p, turn):
        # 8개의 방향에 대한 dx, dy를 튜플로 작성
        dxy = ( (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1) )
        # 플립될 타일들을 최종적으로 저장할 변수 flips 초기화
        flips = []
        # 8개의 방향에 대해서 처리
        for dx, dy in dxy:
            x, y = p%8, p//8     # p로부터 보드의 x, y를 계산합니다.
            nx, ny = x+dx, y+dy
            # 해당 방향에 대해서 임시로 플립될 타일들을 저장할 변수 tf 초기화
            tf = []
            # 해당 방향에 대해서 플립이 실제로 이루어질것인지 변수
            isFlip = False
            # 해당 방향으로 한칸씩 진행하면서 검사
            while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                np = ny*8+nx
                # 내 턴의 돌인 경우 플립이 완성
                if board[np] == turn:
                    isFlip = True
                    break
                # 중간에 비어있는 타일이 있는 경우 중단
                if board[np] != (turn^3): break
                tf.append(np)
                nx, ny = nx+dx, ny+dy
            # 플립이 완성되었다면, 임시 플립 저장소를 최종 플립 저장소에 저장
            if isFlip: flips += tf
        return flips

    def getHints(board, turn):
        # 놓을 수 있는 위치의 개수를 0으로 설정한다.
        hintCount = 0
        # 8x8 모든 위치에 대해서
        for i in range(64):
            # 현재 돌이 이미 있는 곳은 무시한다.
            if board[i] == 1 or board[i] == 2: continue
            # 해당 위치에 turn 타일을 놓을 경우 플립될 돌들을 가져온다.
            flips = Reversi.getFlips(board, i, turn)
            # hintCount를 flips 개수가 있는 경우 증가시키고 board의 값을 0으로 설정
            if len(flips) > 0:
                hintCount += 1
                board[i] = 0
            else:
                board[i] = 3
        # hintCount를 반환한다.
        return hintCount
