class MFGraph:
    '''
    最大流 Dinic法 (ACL互換API, 非再帰)  O(N^2 M) だが実用上かなり速い
    頂点は 0-indexed。容量は非負整数。

    使用例:
        g = MFGraph(N)
        i = g.add_edge(u, v, cap)   # 辺番号 (追加順 0, 1, 2, ...) を返す
        f = g.flow(s, t)            # s -> t の最大流 (流量は内部に残る)
        f = g.flow(s, t, lim)       # 流量の上限 lim まで流す
        cut = g.min_cut(s)          # flow 後: 残余グラフで s から到達可能なら True (s 側)
        e = g.get_edge(i)           # e.frm, e.to, e.cap, e.flow
        g.edges()                   # 全辺の Edge リスト (追加順)
        g.change_edge(i, new_cap, new_flow)  # 辺 i の容量・流量を書き換え

    Edge は __slots__ 付きの小さなクラス (frm, to, cap, flow)。get_edge の戻り値は
    スナップショットなので書き換えてもグラフには反映されない。
    内部表現: 辺 i の順辺 = 2i, 逆辺 = 2i+1 (相方は e ^ 1)。to/cap はフラットなリスト。
    '''
    __slots__ = ('n', 'g', 'to', 'cap')

    class Edge:
        __slots__ = ('frm', 'to', 'cap', 'flow')

        def __init__(self, frm, to, cap, flow):
            self.frm = frm
            self.to = to
            self.cap = cap
            self.flow = flow

        def __repr__(self):
            return f"Edge(frm={self.frm}, to={self.to}, cap={self.cap}, flow={self.flow})"

        def __eq__(self, other):
            return (self.frm, self.to, self.cap, self.flow) == (other.frm, other.to, other.cap, other.flow)

    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.to = []
        self.cap = []

    def add_edge(self, frm, to, cap):
        assert 0 <= frm < self.n and 0 <= to < self.n and 0 <= cap
        m = len(self.to) >> 1
        self.g[frm].append(2 * m)
        self.g[to].append(2 * m + 1)
        self.to.append(to)
        self.to.append(frm)
        self.cap.append(cap)
        self.cap.append(0)
        return m

    def get_edge(self, i):
        assert 0 <= 2 * i < len(self.to)
        to, cap = self.to, self.cap
        return MFGraph.Edge(to[2 * i + 1], to[2 * i], cap[2 * i] + cap[2 * i + 1], cap[2 * i + 1])

    def edges(self):
        return [self.get_edge(i) for i in range(len(self.to) >> 1)]

    def change_edge(self, i, new_cap, new_flow):
        assert 0 <= 2 * i < len(self.to) and 0 <= new_flow <= new_cap
        self.cap[2 * i] = new_cap - new_flow
        self.cap[2 * i + 1] = new_flow

    def flow(self, s, t, flow_limit=float('inf')):
        n = self.n
        assert 0 <= s < n and 0 <= t < n and s != t
        g, to, cap = self.g, self.to, self.cap
        flow = 0
        while flow < flow_limit:
            # BFS: s からの距離 (t に届いたら打ち切り)
            level = [-1] * n
            level[s] = 0
            q = [s]
            for v in q:
                lv = level[v] + 1
                for e in g[v]:
                    w = to[e]
                    if cap[e] and level[w] < 0:
                        level[w] = lv
                        q.append(w)
                if level[t] >= 0:
                    break
            if level[t] < 0:
                break
            # 非再帰 DFS で増加路を 1 本ずつ流す (it で辺を使い切ったら先へ進む)
            it = [0] * n
            lt = level[t]
            while flow < flow_limit:
                path = []
                v = s
                while v != t:
                    adj = g[v]
                    i = it[v]
                    la = len(adj)
                    nl = level[v] + 1
                    while i < la:
                        e = adj[i]
                        w = to[e]
                        if cap[e] and level[w] == nl and (nl < lt or w == t):
                            break
                        i += 1
                    it[v] = i
                    if i < la:
                        path.append(adj[i])
                        v = to[adj[i]]
                    else:
                        # 行き止まり: 以後この頂点は使わない
                        level[v] = -1
                        if not path:
                            break
                        e = path.pop()
                        v = to[e ^ 1]
                        it[v] += 1
                if v != t:
                    break
                f = flow_limit - flow
                for e in path:
                    if cap[e] < f:
                        f = cap[e]
                for e in path:
                    cap[e] -= f
                    cap[e ^ 1] += f
                flow += f
        return flow

    def min_cut(self, s):
        g, to, cap = self.g, self.to, self.cap
        visited = [False] * self.n
        visited[s] = True
        q = [s]
        for v in q:
            for e in g[v]:
                w = to[e]
                if cap[e] and not visited[w]:
                    visited[w] = True
                    q.append(w)
        return visited
