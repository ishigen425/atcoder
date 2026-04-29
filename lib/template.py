import bisect
import copy
import heapq
import math
import sys
from collections import *
from math import gcd
from itertools import accumulate, combinations, permutations, product
def ruiseki(lst): return list(accumulate(lst))
mod=pow(10,9)+7
al=[chr(ord('a') + i) for i in range(26)]
al={chr(ord('a') + i):i for i in range(26)}
direction=[[1,0],[0,1],[-1,0],[0,-1]]
cnt = 0
for j in range(N+1):cnt += (i>>j)&1

def euclidean(x0, y0, x1, y1):
    import math
    return math.sqrt(abs(x0-x1)**2 + abs(y0-y1)**2)

from functools import lru_cache
@lru_cache(maxsize=10**6)
