from matplotlib import pyplot as plt
import numpy as np
mu = 0
sigma = 1
x = mu + sigma*np.random.randn(10000)
fig,(ax0,ax1)=plt.subplots(ncols=2, figsize=(9,6))
ax0.hist(x, 20, normed=1, histtype='bar', facecolor='g', alpha=0.75)
ax0.set_title('pdf')
ax1.hist(x, 20, normed=1, histtype='bar', rwidth=0.8, cumulative=True)
ax1.set_title('cdf')
plt.show()