from heapq import heappush, heappop


class MCFGraph:
    '''
    最小費用流 Primal-Dual (ポテンシャル付き Dijkstra) (ACL互換API)
    頂点は 0-indexed。容量・コストは非負整数 (負コストは不可)。
    計算量 O(F (N + M) log(N + M))  F: 流量

    使用例:
        g = MCFGraph(N)
        i = g.add_edge(u, v, cap, cost)   # 辺番号 (追加順) を返す
        f, c = g.flow(s, t)               # 流せるだけ流したときの (流量, 最小費用)
        f, c = g.flow(s, t, lim)          # 流量 lim まで
        sl = g.slope(s, t)                # 流量-費用の折れ線の頂点 [(0, 0), (f1, c1), ...]
                                          # (流量 x の最小費用は区分線形補間で得られる)
        e = g.get_edge(i)                 # e.frm, e.to, e.cap, e.flow, e.cost
        g.edges()                         # 全辺の Edge リスト (追加順)

    ACL と同様、flow / slope は同じグラフに対して 1 回だけ呼ぶ想定 (流した状態が残る)。
    Edge は __slots__ 付きの小さなクラス (frm, to, cap, flow, cost)。スナップショット。
    内部表現: 辺 i の順辺 = 2i, 逆辺 = 2i+1 (相方は e ^ 1)。to/cap/cost はフラットなリスト。
    '''
    __slots__ = ('n', 'g', 'to', 'cap', 'cost')

    class Edge:
        __slots__ = ('frm', 'to', 'cap', 'flow', 'cost')

        def __init__(self, frm, to, cap, flow, cost):
            self.frm = frm
            self.to = to
            self.cap = cap
            self.flow = flow
            self.cost = cost

        def __repr__(self):
            return (f"Edge(frm={self.frm}, to={self.to}, cap={self.cap}, "
                    f"flow={self.flow}, cost={self.cost})")

        def __eq__(self, other):
            return ((self.frm, self.to, self.cap, self.flow, self.cost)
                    == (other.frm, other.to, other.cap, other.flow, other.cost))

    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.to = []
        self.cap = []
        self.cost = []

    def add_edge(self, frm, to, cap, cost):
        assert 0 <= frm < self.n and 0 <= to < self.n and 0 <= cap and 0 <= cost
        m = len(self.to) >> 1
        self.g[frm].append(2 * m)
        self.g[to].append(2 * m + 1)
        self.to.append(to)
        self.to.append(frm)
        self.cap.append(cap)
        self.cap.append(0)
        self.cost.append(cost)
        self.cost.append(-cost)
        return m

    def get_edge(self, i):
        assert 0 <= 2 * i < len(self.to)
        to, cap = self.to, self.cap
        return MCFGraph.Edge(to[2 * i + 1], to[2 * i], cap[2 * i] + cap[2 * i + 1],
                             cap[2 * i + 1], self.cost[2 * i])

    def edges(self):
        return [self.get_edge(i) for i in range(len(self.to) >> 1)]

    def flow(self, s, t, flow_limit=float('inf')):
        return self.slope(s, t, flow_limit)[-1]

    def slope(self, s, t, flow_limit=float('inf')):
        n = self.n
        assert 0 <= s < n and 0 <= t < n and s != t
        g, to, cap, cost = self.g, self.to, self.cap, self.cost
        INF = float('inf')
        dual = [0] * n       # ACL と同じく -(ポテンシャル)
        prev_e = [-1] * n
        flow = 0
        cst = 0
        prev_cost_per_flow = -1
        result = [(0, 0)]
        while flow < flow_limit:
            # Dijkstra (被約コスト cost[e] - dual[w] + dual[v] >= 0)
            # ヒープのキーは d * n + v (d >= 0 の整数) でタプル生成を省く
            dist = [INF] * n
            vis = [False] * n
            dist[s] = 0
            hq = [s]
            while hq:
                k = heappop(hq)
                v = k % n
                if vis[v]:
                    continue
                vis[v] = True
                if v == t:
                    break
                dv = dist[v]
                dualv = dual[v] + dv
                for e in g[v]:
                    if not cap[e]:
                        continue
                    w = to[e]
                    if vis[w]:
                        continue
                    nd = cost[e] - dual[w] + dualv
                    if nd < dist[w]:
                        dist[w] = nd
                        prev_e[w] = e
                        heappush(hq, nd * n + w)
            if not vis[t]:
                break
            dt = dist[t]
            for v in range(n):
                if vis[v]:
                    dual[v] -= dt - dist[v]
            # 経路上のボトルネック
            c = flow_limit - flow
            v = t
            while v != s:
                e = prev_e[v]
                if cap[e] < c:
                    c = cap[e]
                v = to[e ^ 1]
            v = t
            while v != s:
                e = prev_e[v]
                cap[e] -= c
                cap[e ^ 1] += c
                v = to[e ^ 1]
            d = -dual[s]
            flow += c
            cst += c * d
            if prev_cost_per_flow == d:
                result.pop()
            result.append((flow, cst))
            prev_cost_per_flow = d
        return result
