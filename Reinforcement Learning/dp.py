# 동적 프로그래밍 (Dynamic Programming)

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
    
    # s상태에서 dir로 움직일 경우 다음 상태 
    def nextState(self, s, dir):
        dxy = [ (0, 1), (1, 0), (0, -1), (-1, 0) ]
        # dir값에 따라 움직여야 할 위치를 계산
        nr, nc = s[0] + dxy[dir][0], s[1] + dxy[dir][1]
        # 움직일 수 있는 위치인지 파악
        if nr < 0 or nr >= self.n or nc < 0 or nc >= self.m or self.map[nr][nc] != 0 :
            nr, nc = s        
        return (nr, nc)

    # 결과값 출력
    def print(self, ss):
        print('-'*(9*self.m))
        for r in range(self.n):
            line = ''
            for c in range(self.m):
                if self.map[r][c] == 1: line += ' [#####] '
                else: line += '{:^9.2f}'.format(ss[r][c])
            print(line)
        print('-'*(9*self.m))              
        

mapName = input('Map name : ')
errLimit = 0.0001
env = GridWorld(mapName)

# 상태공간 만들기
ss = [ [0] * env.m for _ in range(env.n) ]
while True:
    # 현재 값을 저장할 상태공간 만들기
    nss = [ [0]*env.m for _ in range(env.n) ]
    # 모든 상태에 대해서
    for r in range(env.n):
        for c in range(env.m):
            # 현재 상태
            s = (r, c)
            # 현재 상태가 목적지인 경우 무시
            if s == env.end: continue
            # 갈 수 있는 모든 상태에 대해
            for d in range(4):
                ns = env.nextState(s, d)
                nss[r][c] += (-1 + ss[ns[0]][ns[1]])*0.25  # -1: reward 값 
    # 에러 계산
    errSum = 0.0
    for r in range(env.n):
        for c in range(env.m):
            errSum += (nss[r][c] - ss[r][c])**2
    print(errSum/(env.n*env.m))
    ss = nss
    # error square mean value is under errLimit,
    if errSum < errLimit*env.n*env.m: break
                    
env.print(ss)



