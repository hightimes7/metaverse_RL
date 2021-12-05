import random       # 몬테 카를로 기법에서 사용할 무작위 수 모듈

# 격자세계를 읽고 프로세스할 클래스
class GridWorld:
    # 생성자
    def __init__(self, fname):
        # 비어있는 맵으로 초기화
        self.map = []
        # fname으로 파일을 열어서 처리
        with open(fname) as f:
            self.n, self.m = map(int, f.readline().split())
            self.start = tuple(map(int, f.readline().split()))
            self.end = tuple(map(int, f.readline().split()))
            for _ in range(self.n):
                self.map.append(
                    [0 if k == '0' else 1 for k in f.readline()
                     if k == '0' or k == '1'])

    # 환경을 초기화
    def init(self):
        # 에이전트의 위치를 시작지점으로 옮김
        self.agent = self.start
        return self.agent

    # 에이전트 움직이기
    def move(self, dir):
        dxy = [ (0, 1), (1, 0), (0, -1), (-1, 0) ]
        # dir값에 따라 움직여야 할 에이전트 위치를 계산
        nr, nc = self.agent[0] + dxy[dir][0], self.agent[1] + dxy[dir][1]
        # 움직일 수 있는 위치인지 파악
        if nr < 0 or nr >= self.n or nc < 0 or nc >= self.m or self.map[nr][nc] != 0 : nr, nc = self.agent
        self.agent = (nr, nc)
        return self.agent

    # 목적지 도착 여부
    def isFinish(self):
        return self.agent == self.end

    # 결과값 출력
    def print(self, ss):
        print('-'*(9*self.m))
        for r in range(self.n):
            line = ''
            for c in range(self.m):
                if self.map[r][c] == 1: line += ' [#####] '
                elif ss[r][c][1] == 0: line += '       '
                else: line += '{:^9.2f}'.format(ss[r][c][0]/ss[r][c][1])
            print(line)
        print('-'*(9*self.m))              
        

mapName = input('Map name : ')
iterCount = int(input('Iteration Count : '))
env = GridWorld(mapName)

# 상태공간 만들기
ss = [ [(0, 0)] * env.m for _ in range(env.n) ]
for _ in range(iterCount):
    # 에피소드 만들기
    episode = [env.init()]
    while not env.isFinish():
        dir = random.randrange(4)
        episode.append(env.move(dir))
    # 에피소드의 값을 가지고 상태값 수정
    reward = 0.0
    for s in episode[::-1]:
        ss[s[0]][s[1]] = (ss[s[0]][s[1]][0]+reward, ss[s[0]][s[1]][1]+1)
        reward += -1
env.print(ss)



