class TwoSAT:
    '''
    2-SAT (ACL互換API, 内部で非再帰 Tarjan SCC)  O(N + M)
    変数は 0-indexed。頂点 2i が「x_i = False」, 2i+1 が「x_i = True」。

    使用例:
        ts = TwoSAT(N)
        ts.add_clause(i, f, j, g)   # (x_i == f) or (x_j == g) を追加  f, g は bool
        # 例: x_i => x_j  は  add_clause(i, False, j, True)
        #     x_i を True に固定  は  add_clause(i, True, i, True)
        #     x_i != x_j  は  add_clause(i, True, j, True); add_clause(i, False, j, False)
        if ts.satisfiable():        # 充足可能か
            ans = ts.answer()       # 充足する割り当て list[bool] (satisfiable() 後に有効)
    '''
    __slots__ = ('n', '_answer', 'frm', 'to')

    def __init__(self, n):
        self.n = n
        self._answer = [False] * n
        self.frm = []
        self.to = []

    def add_clause(self, i, f, j, g):
        assert 0 <= i < self.n and 0 <= j < self.n
        # not(x_i == f) -> (x_j == g),  not(x_j == g) -> (x_i == f)
        self.frm.append(2 * i + (0 if f else 1))
        self.to.append(2 * j + (1 if g else 0))
        self.frm.append(2 * j + (0 if g else 1))
        self.to.append(2 * i + (1 if f else 0))

    def satisfiable(self):
        ids = self._scc_ids()
        ans = self._answer
        for i in range(self.n):
            a = ids[2 * i]
            b = ids[2 * i + 1]
            if a == b:
                return False
            ans[i] = a < b
        return True

    def answer(self):
        return self._answer

    def _scc_ids(self):
        # 成分番号はトポロジカル順 (ACL の scc_ids と同じ)
        n = 2 * self.n
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
        return ids
