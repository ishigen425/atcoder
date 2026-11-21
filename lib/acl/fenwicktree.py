class FenwickTree:
    '''
    Binary Indexed Tree (ACL互換API) 0-indexed
    n: 要素数 (初期値はすべて 0)

    使用例:
        ft = FenwickTree(N)
        ft.add(p, x)     # a[p] += x  O(logN)
        ft.sum(l, r)     # a[l] + ... + a[r-1]  半開区間 O(logN)
        # 転倒数
        ft = FenwickTree(M); inv = 0
        for i, a in enumerate(A): inv += i - ft.sum(0, a + 1); ft.add(a, 1)
    '''
    def __init__(self, n):
        self.n = n
        self.data = [0] * (n + 1)

    def add(self, p, x):
        p += 1
        n, data = self.n, self.data
        while p <= n:
            data[p] += x
            p += p & -p

    def sum(self, l, r):
        # 共通の祖先は打ち消し合うので prefix(r) - prefix(l) を同時に計算
        data = self.data
        s = 0
        while r > l:
            s += data[r]
            r &= r - 1
        while l > r:
            s -= data[l]
            l &= l - 1
        return s

    def __repr__(self):
        return f"FenwickTree({[self.sum(i, i + 1) for i in range(self.n)]})"
