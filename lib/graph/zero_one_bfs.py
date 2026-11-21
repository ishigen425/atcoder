from collections import deque


def zero_one_bfs(n, adj, s):
    '''
    0-1 BFS  辺の重みが 0 か 1 のみの最短路  O(N + M)
    adj[u] = [(v, w), ...]  (w は 0 or 1)
    到達不能は -1

    使用例 (グリッド: 同じ色へは0, 壁壊しは1 など):
        adj = [[] for _ in range(N)]
        adj[u].append((v, 0))
        dist = zero_one_bfs(N, adj, 0)
    '''
    INF = 1 << 60
    dist = [INF] * n
    dist[s] = 0
    dq = deque([s])
    while dq:
        u = dq.popleft()
        d = dist[u]
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                if w == 0:
                    dq.appendleft(v)
                else:
                    dq.append(v)
    return [d if d < INF else -1 for d in dist]
