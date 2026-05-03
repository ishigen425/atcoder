# 強連結成分分解

import sys
sys.setrecursionlimit(10**8)
from collections import Counter
N,M = map(int, input().split())

edges1 = [[] for i in range(N)]
edges2 = [[] for i in range(N)]
for _ in range(M):
    a, b = map(int, input().split())
    a-=1
    b-=1
    edges1[a].append(b)
    edges2[b].append(a)

count1 = [-1] * N
cnt = 0
def dfs(now):
    global cnt
    if count1[now] >= 0: return
    count1[now] = 0
    for nv in edges1[now]:
        dfs(nv)
    count1[now] = cnt
    cnt += 1

for i in range(N):
    if count1[i] >= 0: continue
    dfs(i)

count2 = [-1] * N
cnt = 0
def dfs2(now):
    global cnt
    if count2[now] >= 0: return
    count2[now] = cnt
    for nv in edges2[now]:
        dfs2(nv)

# print(count)
countidx = [[a, i] for i, a in enumerate(count1)]
countidx.sort(reverse=True)
for a, i in countidx:
    if count2[i] >= 0: continue
    dfs2(i)
    cnt += 1
    
# print(count2)
ans = 0
c = Counter(count2)
for i, v in c.items():
    ans += v * (v-1) // 2

print(ans)
