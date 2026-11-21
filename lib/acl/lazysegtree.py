class LazySegTree:
    '''
    非再帰遅延評価セグメント木 (ACL互換API)
    op: 二項演算 (結合則)  e: op の単位元
    mapping(f, x): 作用素 f を値 x に作用させた結果
    composition(f, g): f∘g (g を先に作用させ、その後 f)
    id_: 恒等写像  v: 要素数 or 初期配列
    ※ Python ではオーバーロード不可のため、一点作用は apply_point(p, f)、
      区間作用は apply(l, r, f) と名前を分けている

    使用例:
        # 区間加算 / 区間最小
        INF = 1 << 60
        st = LazySegTree(min, INF, lambda f, x: f + x, lambda f, g: f + g, 0, A)
        st.apply(l, r, x)    # a[l..r-1] += x

        # 区間アフィン (a = b*a + c) / 区間和  値は (sum, len) ペア
        MOD = 998244353
        st = LazySegTree(
            lambda a, b: ((a[0] + b[0]) % MOD, a[1] + b[1]), (0, 0),
            lambda f, x: ((f[0] * x[0] + f[1] * x[1]) % MOD, x[1]),
            lambda f, g: (f[0] * g[0] % MOD, (f[0] * g[1] + f[1]) % MOD),
            (1, 0), [(a, 1) for a in A])
        st.apply(l, r, (b, c))  # a[l..r-1] = b * a + c
        st.prod(l, r)[0]        # 区間和

        st[i] = x / st.set(i, x)   # 一点更新
        st[i]      / st.get(i)     # 一点取得
        st.prod(l, r)        # op(a[l], ..., a[r-1])  半開区間 O(logN)
        st.all_prod()        # 全体 O(1)
        st.apply_point(p, f) # a[p] = f(a[p])
        st.apply(l, r, f)    # i in [l, r) について a[i] = f(a[i])
        st.max_right(l, g)   # g(prod(l, r)) が True となる最大の r (g(e) は True)
        st.min_left(r, g)    # g(prod(l, r)) が True となる最小の l (g(e) は True)
    '''
    def __init__(self, op, e, mapping, composition, id_, v):
        if isinstance(v, int):
            v = [e] * v
        self.n = len(v)
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id_
        self.log = max(self.n - 1, 0).bit_length()
        self.size = 1 << self.log
        self.d = [e] * (2 * self.size)
        self.lz = [id_] * self.size
        self.d[self.size:self.size + self.n] = v
        d = self.d
        for i in range(self.size - 1, 0, -1):
            d[i] = op(d[2 * i], d[2 * i + 1])

    def _push(self, k):
        f = self.lz[k]
        if f is self.id or f == self.id:
            return
        d, lz, mapping, composition = self.d, self.lz, self.mapping, self.composition
        a = 2 * k
        b = a + 1
        d[a] = mapping(f, d[a])
        d[b] = mapping(f, d[b])
        if a < self.size:
            lz[a] = composition(f, lz[a])
            lz[b] = composition(f, lz[b])
        lz[k] = self.id

    def _push_path(self, p):
        # 根から葉 p の親までを push
        push = self._push
        for i in range(self.log, 0, -1):
            push(p >> i)

    def _update_path(self, p):
        op, d = self.op, self.d
        p >>= 1
        while p:
            d[p] = op(d[2 * p], d[2 * p + 1])
            p >>= 1

    def set(self, p, x):
        p += self.size
        self._push_path(p)
        self.d[p] = x
        self._update_path(p)

    def get(self, p):
        p += self.size
        self._push_path(p)
        return self.d[p]

    __setitem__ = set
    __getitem__ = get

    def prod(self, l, r):
        if l == r:
            return self.e
        l += self.size
        r += self.size
        push = self._push
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                push(l >> i)
            if ((r >> i) << i) != r:
                push((r - 1) >> i)
        op, d = self.op, self.d
        sml = smr = self.e
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

    def apply_point(self, p, f):
        p += self.size
        self._push_path(p)
        self.d[p] = self.mapping(f, self.d[p])
        self._update_path(p)

    def apply(self, l, r, f):
        if l == r:
            return
        size, log = self.size, self.log
        d, lz, op = self.d, self.lz, self.op
        mapping, composition = self.mapping, self.composition
        l += size
        r += size
        push = self._push
        for i in range(log, 0, -1):
            if ((l >> i) << i) != l:
                push(l >> i)
            if ((r >> i) << i) != r:
                push((r - 1) >> i)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                d[l] = mapping(f, d[l])
                if l < size:
                    lz[l] = composition(f, lz[l])
                l += 1
            if r & 1:
                r -= 1
                d[r] = mapping(f, d[r])
                if r < size:
                    lz[r] = composition(f, lz[r])
            l >>= 1
            r >>= 1
        l, r = l2, r2
        for i in range(1, log + 1):
            if ((l >> i) << i) != l:
                k = l >> i
                d[k] = op(d[2 * k], d[2 * k + 1])
            if ((r >> i) << i) != r:
                k = (r - 1) >> i
                d[k] = op(d[2 * k], d[2 * k + 1])

    def max_right(self, l, g):
        if l == self.n:
            return self.n
        op, d, size = self.op, self.d, self.size
        push = self._push
        l += size
        self._push_path(l)
        sm = self.e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not g(op(sm, d[l])):
                while l < size:
                    push(l)
                    l *= 2
                    if g(op(sm, d[l])):
                        sm = op(sm, d[l])
                        l += 1
                return l - size
            sm = op(sm, d[l])
            l += 1
            if l & -l == l:
                return self.n

    def min_left(self, r, g):
        if r == 0:
            return 0
        op, d, size = self.op, self.d, self.size
        push = self._push
        r += size
        self._push_path(r - 1)
        sm = self.e
        while True:
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not g(op(d[r], sm)):
                while r < size:
                    push(r)
                    r = 2 * r + 1
                    if g(op(d[r], sm)):
                        sm = op(d[r], sm)
                        r -= 1
                return r + 1 - size
            sm = op(d[r], sm)
            if r & -r == r:
                return 0

    def __repr__(self):
        return f"LazySegTree({[self.get(i) for i in range(self.n)]})"
