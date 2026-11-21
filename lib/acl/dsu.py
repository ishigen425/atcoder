class DSU:
    '''
    Union-Find (ACL互換API) 経路圧縮(非再帰) + union by size
    n: 頂点数

    使用例:
        uf = DSU(N)
        uf.merge(a, b)   # a, b を併合し、新しい代表元を返す
        uf.same(a, b)    # a, b が同じ連結成分か
        uf.leader(a)     # a の代表元
        uf.size(a)       # a を含む連結成分の大きさ
        uf.groups()      # 連結成分ごとの頂点リストのリスト
        len(uf.groups()) # 連結成分の個数
    '''
    def __init__(self, n):
        self.n = n
        # 負なら根で -size, 非負なら親
        self.p = [-1] * n

    def merge(self, a, b):
        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return x
        p = self.p
        if -p[x] < -p[y]:
            x, y = y, x
        p[x] += p[y]
        p[y] = x
        return x

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def leader(self, a):
        p = self.p
        r = a
        while p[r] >= 0:
            r = p[r]
        while p[a] >= 0:
            p[a], a = r, p[a]
        return r

    def size(self, a):
        return -self.p[self.leader(a)]

    def groups(self):
        leader = self.leader
        res = [[] for _ in range(self.n)]
        for i in range(self.n):
            res[leader(i)].append(i)
        return [g for g in res if g]

    def __repr__(self):
        return f"DSU({self.groups()})"
