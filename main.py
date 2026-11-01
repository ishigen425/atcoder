from collections import defaultdict, deque

N = int(input())

# 頂点 N は直径が奇数のときに中心2頂点の間へ挿入する仮想頂点
edges = [[] for _ in range(N + 1)]
for _ in range(N - 1):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    edges[u].append(v)
    edges[v].append(u)

C = list(map(int, input().split())) + [0]


def bfs(start):
    """start からの距離と BFS 木での親を返す (非再帰)"""
    dist = [-1] * (N + 1)
    par = [-1] * (N + 1)
    dist[start] = 0
    q = deque([start])
    while q:
        v = q.popleft()
        for nv in edges[v]:
            if dist[nv] >= 0:
                continue
            dist[nv] = dist[v] + 1
            par[nv] = v
            q.append(nv)
    return dist, par


# 木の直径: 適当な頂点から最遠の頂点 a、a から最遠の頂点 b
dist0, _ = bfs(0)
a = max(range(N), key=lambda i: dist0[i])
dist_a, par_a = bfs(a)
b = max(range(N), key=lambda i: dist_a[i])
diameter = dist_a[b]

# b から a へ親をたどって直径パスを復元し、その真ん中を中心とする
path = [b]
while path[-1] != a:
    path.append(par_a[path[-1]])

if diameter % 2 == 1:
    # 中心が2つ → 間に仮想頂点 N を挟んで中心を1つにする
    c1 = path[diameter // 2]
    c2 = path[diameter // 2 + 1]
    edges[c1].remove(c2)
    edges[c2].remove(c1)
    edges[c1].append(N)
    edges[c2].append(N)
    edges[N] += [c1, c2]
    center = N
    radius = diameter // 2 + 1
else:
    center = path[diameter // 2]
    radius = diameter // 2

# 中心の各隣接頂点(枝)ごとに、中心から距離 radius の頂点を色別に数える
colors = [defaultdict(int) for _ in range(N + 1)]
dist_c, _ = bfs(center)
for first in edges[center]:
    stack = [first]
    while stack:
        v = stack.pop()
        if dist_c[v] == radius:
            colors[C[v]][first] += 1
            continue
        for nv in edges[v]:
            if dist_c[nv] > dist_c[v]:
                stack.append(nv)

ans = 0
for color in colors:
    if len(color) <= 1:
        continue
    # 異なる枝から1つずつ選ぶペア数 = (S^2 - Σc^2) / 2
    s = sum(color.values())
    sq = sum(v * v for v in color.values())
    ans += (s * s - sq) // 2

print(ans)
