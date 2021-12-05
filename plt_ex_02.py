import matplotlib.pyplot as plt
import matplotlib.style
import numpy as np

matplotlib.style.use('bmh')
_, ax = plt.subplots()
cities = (('Seoul', 'ko-'),('Busan', 'r<--'),('Daejeon','bd-'))
y = np.arange(2000, 2021, dtype=int)
min, max = 10**9, -10**9
for c, m in cities:
    v = np.random.randn(21).cumsum()
    ax.plot(y, v, m)
    plt.annotate(c, (2021, v[20]))
    if min > v.min(): min = v.min()
    if max < v.max(): max = v.max()

plt.axis([1999, 2025, min-1, max+3])
plt.title('City Growth')
plt.xlabel('year')
plt.ylabel('population')
plt.legend(cities)
plt.show()
