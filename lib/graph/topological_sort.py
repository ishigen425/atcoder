from collections import deque
from heapq import heapify, heappop, heappush


def topological_sort(n, edges, lexicographic=False):
    '''
    トポロジカルソート (Kahn法)  O(N + M)
    edges: (u, v) のリスト (u -> v, 0-indexed)
    戻り値: 頂点順のリスト。閉路があれば None
    lexicographic=True で辞書順最小の順序 (heapq, O((N+M) log N))

    使用例:
        order = topological_sort(N, [(0, 1), (1, 2)])
        if order is None: print("閉路あり")

        # DAG上の最長パス (頂点数)
        dp = [1] * N
        for u in order:
            for v in adj[u]: dp[v] = max(dp[v], dp[u] + 1)
    '''
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1
    order = []
    if lexicographic:
        hq = [i for i in range(n) if indeg[i] == 0]
        heapify(hq)
        while hq:
            u = heappop(hq)
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    heappush(hq, v)
    else:
        q = deque(i for i in range(n) if indeg[i] == 0)
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
    return order if len(order) == n else None
