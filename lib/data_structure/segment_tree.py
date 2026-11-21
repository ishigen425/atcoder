class SegTree:
    '''
    非再帰セグメント木 (ACL互換API)
    op: 二項演算 (結合則を満たす)  e: 単位元  v: 要素数 or 初期配列

    使用例:
        st = SegTree(min, 1 << 60, A)            # 区間最小
        st = SegTree(max, -(1 << 60), N)         # 区間最大
        st = SegTree(lambda a, b: a + b, 0, A)   # 区間和
        from math import gcd; st = SegTree(gcd, 0, A)  # 区間GCD

        st[i] = x            # 一点更新 (= st.set(i, x))
        st[i]                # 一点取得 (= st.get(i))
        st.prod(l, r)        # op(a[l], ..., a[r-1])  半開区間 O(logN)
        st.all_prod()        # 全体 O(1)
        st.max_right(l, f)   # f(prod(l, r)) が True となる最大の r
        st.min_left(r, f)    # f(prod(l, r)) が True となる最小の l
    '''
    def __init__(self, op, e, v):
        if isinstance(v, int):
            v = [e] * v
        self.n = len(v)
        self.op = op
        self.e = e
        self.log = max(self.n - 1, 0).bit_length()
        self.size = 1 << self.log
        self.d = [e] * (2 * self.size)
        self.d[self.size:self.size + self.n] = v
        for i in range(self.size - 1, 0, -1):
            self.d[i] = op(self.d[2 * i], self.d[2 * i + 1])

    def set(self, p, x):
        p += self.size
        self.d[p] = x
        op, d = self.op, self.d
        p >>= 1
        while p:
            d[p] = op(d[2 * p], d[2 * p + 1])
            p >>= 1

    def get(self, p):
        return self.d[p + self.size]

    __setitem__ = set
    __getitem__ = get

    def prod(self, l, r):
        op, d = self.op, self.d
        sml = smr = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                sml = op(sml, d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = op(d[r], smr)
            l >>= 1
            r >>= 1
        return op(sml, smr)

    def all_prod(self):
        return self.d[1]

    def max_right(self, l, f):
        if l == self.n:
            return self.n
        op, d, size = self.op, self.d, self.size
        l += size
        sm = self.e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not f(op(sm, d[l])):
                while l < size:
                    l *= 2
                    if f(op(sm, d[l])):
                        sm = op(sm, d[l])
                        l += 1
                return l - size
            sm = op(sm, d[l])
            l += 1
            if l & -l == l:
                return self.n

    def min_left(self, r, f):
        if r == 0:
            return 0
        op, d, size = self.op, self.d, self.size
        r += size
        sm = self.e
        while True:
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not f(op(d[r], sm)):
                while r < size:
                    r = 2 * r + 1
                    if f(op(d[r], sm)):
                        sm = op(d[r], sm)
                        r -= 1
                return r + 1 - size
            sm = op(d[r], sm)
            if r & -r == r:
                return 0

    def __repr__(self):
        return f"SegTree({[self.get(i) for i in range(self.n)]})"


# 遅延評価セグメント木
# 区間最大値の取得 O(logN)
# 区間最大値の更新 O(logN)
# https://atcoder.jp/contests/typical90/submissions/25004902
