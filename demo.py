import numpy as np
from scipy.stats import pearsonr
import json

# We define two sequences x, y as numpy array
# where y is actually a sub-sequence from x
# x = np.array([2, 0, 1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)
# y = np.array([1, 1, 2, 4, 2, 1, 2, 0]).reshape(-1, 1)

from dtw import dtw

with open('standard.json') as f:
    standard = json.load(f)

with open('output.json') as f:
    output = json.load(f)

x = standard['frames'][0]['points']
y = output['frames'][0]['points']


def eculidDisSim(x,y):
    '''欧几里得相似度'''
    return np.sqrt(sum(pow(a-b,2) for a,b in zip(x,y)))

def cosSim(x,y):
    '''余弦相似度'''
    tmp=np.sum(x*y)
    non=np.linalg.norm(x)*np.linalg.norm(y)
    return np.round(tmp/float(non),9)

def pearsonrSim(x,y):
    '''皮尔森相似度'''
    return pearsonr(x,y)[0]

def manhattanDisSim(x,y):
    '''曼哈顿相似度'''
    return sum(abs(a-b) for a,b in zip(x,y))


d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattanDisSim)
print(d)

# You can also visualise the accumulated cost and the shortest path
import matplotlib.pyplot as plt

plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.show()

