import matplotlib.pyplot as plt
import matplotlib.style
import numpy as np

matplotlib.style.use('bmh')
_, ax = plt.subplots(2,2)
s = np.arange(0,10)
t = np.random.randint(1, 10, 10)
r = np.random.randint(1, 10, 100)
ax[0,0].bar(s,t)
ax[0,1].scatter(s,t)
ax[1,0].hist(r)
ax[1,1].pie(t)
plt.show()
