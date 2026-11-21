def warshall_floyd(n, edges, directed=True):
    '''
    ワーシャルフロイド 全点対最短路  O(N^3)  (CPythonでは N≈400 程度まで)
    edges: (u, v, w) のリスト (0-indexed)
    戻り値: (dist, has_negative_cycle)  到達不能は INF (= 1 << 60)

    使用例:
        dist, neg = warshall_floyd(N, [(0, 1, 5), (1, 2, 3)], directed=False)
        d = dist[0][2]  # 8
    '''
    INF = 1 << 60
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]: d[u][v] = w
        if not directed and w < d[v][u]: d[v][u] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF: continue
            di = d[i]
            # 行ごとにリスト内包で更新 (二重ループより大幅に速い)
            d[i] = [a if a <= dik + b else dik + b for a, b in zip(di, dk)]
    neg = any(d[i][i] < 0 for i in range(n))
    return d, neg
