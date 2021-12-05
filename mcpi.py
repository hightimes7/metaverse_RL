# 몬테카를로 법칙으로 원주율 구하기
# 결과값의 폭이 넓고(high variance), 결과값의 평균이 좁음(low bias)

import matplotlib.pyplot as plt
import matplotlib.style
import random

matplotlib.style.use('bmh')
_, ax = plt.subplots()
plt.axis((0, 1, 0, 1))
ax.set_aspect(1)

n = int(input('n = '))
inCount = 0             # 4분원 안에 들어가는 점의 갯수
inListX, inListY = [], []
outListX, outListY = [], []
for i in range(1, n+1):
    x, y = (random.uniform(0,1), random.uniform(0,1))
    isIn = (x**2 + y**2 <= 1)
    inCount += isIn
    if isIn :
        inListX.append(x)
        inListY.append(y)
    else:
        outListX.append(x)
        outListY.append(y)
    if i%100 == 0:
        ax.set_title(f'n = {i} pi ~ {inCount*4/i:5f}')
        ax.scatter(inListX, inListY, c='b', s=2)
        ax.scatter(outListX, outListY, c='r', s=2)
        plt.pause(0.1)
        inListX, inListY = [], []
        outListX, outListY = [], []
    
print(f'pi = {inCount*4/n}')

