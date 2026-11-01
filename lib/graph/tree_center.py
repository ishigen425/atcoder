# 木の直径と中心
#
# N: 頂点数 (0-indexed)
# edges[v]: 頂点vの隣接頂点リスト
#
# - tree_diameter(N, edges) -> (diameter, path)
#   diameter: 直径の長さ (辺の本数)
#   path: 直径の両端を結ぶパス (頂点リスト, 長さ diameter+1)
# - tree_center(N, edges) -> (centers, radius)
#   centers: 中心のリスト。直径が偶数なら1つ、奇数なら隣接する2つ
#   radius: 中心から最も遠い頂点までの距離 (= ceil(diameter / 2))
#
# 直径が奇数で中心が2つあると扱いにくい場合は、2つの中心 c1, c2 の間の辺を消して
# 仮想頂点 N を挟む (c1 - N - c2) と、中心が N の1つ、半径が diameter//2 + 1 になる。
# このとき直径のパスはすべて仮想頂点を通る (ABC482 E)。
#
# 計算量: O(N)
from collections import deque


def _bfs(N, edges, start):
    dist = [-1] * N
    par = [-1] * N
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


def tree_diameter(N, edges):
    # 適当な頂点から最遠の頂点 a、a から最遠の頂点 b が直径の両端
    dist0, _ = _bfs(N, edges, 0)
    a = max(range(N), key=lambda i: dist0[i])
    dist_a, par_a = _bfs(N, edges, a)
    b = max(range(N), key=lambda i: dist_a[i])
    path = [b]
    while path[-1] != a:
        path.append(par_a[path[-1]])
    return dist_a[b], path


def tree_center(N, edges):
    # 中心は直径パスの真ん中
    diameter, path = tree_diameter(N, edges)
    if diameter % 2 == 0:
        return [path[diameter // 2]], diameter // 2
    return [path[diameter // 2], path[diameter // 2 + 1]], diameter // 2 + 1


if __name__ == "__main__":
    # 1 - 2 - 3 - 4 - 5 (直径4, 中心3)
    N = 5
    edges = [[] for _ in range(N)]
    for u, v in [(0, 1), (1, 2), (2, 3), (3, 4)]:
        edges[u].append(v)
        edges[v].append(u)
    assert tree_diameter(N, edges)[0] == 4
    assert tree_center(N, edges) == ([2], 2)

    # 1 - 2 - 3 - 4 (直径3, 中心2,3)
    N = 4
    edges = [[] for _ in range(N)]
    for u, v in [(0, 1), (1, 2), (2, 3)]:
        edges[u].append(v)
        edges[v].append(u)
    centers, radius = tree_center(N, edges)
    assert sorted(centers) == [1, 2] and radius == 2

    # スター (直径2, 中心0)
    N = 5
    edges = [[] for _ in range(N)]
    for v in range(1, N):
        edges[0].append(v)
        edges[v].append(0)
    assert tree_center(N, edges) == ([0], 1)
    print("ok")
