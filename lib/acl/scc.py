class SCCGraph:
    '''
    強連結成分分解 Tarjan法 (ACL互換API, 非再帰)  O(N + M)
    頂点は 0-indexed。

    使用例:
        g = SCCGraph(N)
        g.add_edge(u, v)       # 有向辺 u -> v
        groups = g.scc()       # 成分のリスト (トポロジカル順: 辺 u->v なら u の成分が先 or 同じ)
        num, ids = g.scc_ids() # 成分数と各頂点の成分番号 (番号もトポロジカル順)
    '''
    __slots__ = ('n', 'frm', 'to')

    def __init__(self, n):
        self.n = n
        self.frm = []
        self.to = []

    def add_edge(self, frm, to):
        assert 0 <= frm < self.n and 0 <= to < self.n
        self.frm.append(frm)
        self.to.append(to)

    def scc_ids(self):
        n = self.n
        # CSR 形式の隣接リスト
        start = [0] * (n + 1)
        for u in self.frm:
            start[u + 1] += 1
        for i in range(n):
            start[i + 1] += start[i]
        it = start[:]
        elist = [0] * len(self.to)
        for u, v in zip(self.frm, self.to):
            elist[it[u]] = v
            it[u] += 1
        it = start[:n]

        now_ord = 0
        group_num = 0
        visited = []
        low = [0] * n
        ord_ = [-1] * n
        ids = [0] * n
        for root in range(n):
            if ord_[root] != -1:
                continue
            ord_[root] = low[root] = now_ord
            now_ord += 1
            visited.append(root)
            stack = [root]
            while stack:
                v = stack[-1]
                i = it[v]
                end = start[v + 1]
                # v の未処理の辺を進める (訪問済みの頂点は low を更新するだけ)
                lv = low[v]
                while i < end:
                    w = elist[i]
                    i += 1
                    ow = ord_[w]
                    if ow == -1:
                        break
                    if ow < lv:
                        lv = ow
                else:
                    w = -1
                low[v] = lv
                it[v] = i
                if w != -1:
                    ord_[w] = low[w] = now_ord
                    now_ord += 1
                    visited.append(w)
                    stack.append(w)
                    continue
                # v の探索終了
                stack.pop()
                if lv == ord_[v]:
                    while True:
                        u = visited.pop()
                        ord_[u] = n
                        ids[u] = group_num
                        if u == v:
                            break
                    group_num += 1
                if stack:
                    p = stack[-1]
                    if lv < low[p]:
                        low[p] = lv
        for i in range(n):
            ids[i] = group_num - 1 - ids[i]
        return group_num, ids

    def scc(self):
        group_num, ids = self.scc_ids()
        groups = [[] for _ in range(group_num)]
        for v, c in enumerate(ids):
            groups[c].append(v)
        return groups
