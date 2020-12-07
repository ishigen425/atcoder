import bisect
import copy
import heapq
import math
import sys
from collections import *
from itertools import accumulate, combinations, permutations, product
from math import gcd
def ruiseki(lst):
    return [0]+list(accumulate(lst))
mod=pow(10,9)+7
al=[chr(ord('a') + i) for i in range(26)]
direction=[[1,0],[0,1],[-1,0],[0,-1]]
cnt = 0
for j in range(N+1):cnt += (i>>j)&1

def euclidean(x0, y0, x1, y1):
    import math
    return math.sqrt(abs(x0-x1)**2 + abs(y0-y1)**2)

