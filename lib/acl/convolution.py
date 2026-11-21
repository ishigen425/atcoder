'''
畳み込み (ACL互換API)

    convolution(a, b, mod=998244353)  # NTT。c[k] = sum_{i+j=k} a[i]*b[j] mod mod
    convolution_ll(a, b)              # 整数のまま厳密な畳み込み (3素数NTT + CRT)
    convolution_fast(a, b, mod=998244353)  # 10進パッキング版 (CPython ではこちらが約5倍速い)
    convolution_ll_fast(a, b)              # 10進パッキング版の厳密畳み込み (負数・巨大値OK)

CPython では純Python の NTT より、配列を1つの巨大な10進数にエンコードして
decimal モジュール (C実装 libmpdec, 巨大な桁では内部で NTT) の掛け算に任せる方が速い。
mod も NTT-friendly である必要がない。迷ったら *_fast を使う。
(int 同士の掛け算でパッキングする方法は CPython の int が Karatsuba 止まりのため
 N=2*10^5 では NTT より遅い。decimal を使うのがポイント。)

N = M = 2*10^5 での目安 (CPython 3.14):
    convolution 2.1s / convolution_fast 0.45s / convolution_ll 6.7s / convolution_ll_fast 0.55s
'''
import decimal

_cache = {}


def _primitive_root(m):
    # ACL internal::primitive_root と同じ
    if m == 2:
        return 1
    if m == 167772161 or m == 469762049 or m == 998244353:
        return 3
    if m == 754974721:
        return 11
    divs = []
    x = (m - 1) // 2
    while x % 2 == 0:
        x //= 2
    divs.append(2)
    i = 3
    while i * i <= x:
        if x % i == 0:
            divs.append(i)
            while x % i == 0:
                x //= i
        i += 2
    if x > 1:
        divs.append(x)
    g = 2
    while True:
        if all(pow(g, (m - 1) // d, m) != 1 for d in divs):
            return g
        g += 1


def _prepare(mod):
    # ACL の sum_e / sum_ie から、ブロック s 用の回転因子列 (全段共通) を作る
    if mod in _cache:
        return _cache[mod]
    g = _primitive_root(mod)
    cnt2 = ((mod - 1) & -(mod - 1)).bit_length() - 1
    e = pow(g, (mod - 1) >> cnt2, mod)
    ie = pow(e, mod - 2, mod)
    es = [0] * max(cnt2 - 1, 0)
    ies = [0] * max(cnt2 - 1, 0)
    for i in range(cnt2, 1, -1):
        es[i - 2] = e
        ies[i - 2] = ie
        e = e * e % mod
        ie = ie * ie % mod
    sum_e = []
    sum_ie = []
    now = inow = 1
    for i in range(cnt2 - 1):
        sum_e.append(es[i] * now % mod)
        now = now * ies[i] % mod
        sum_ie.append(ies[i] * inow % mod)
        inow = inow * es[i] % mod
    _cache[mod] = r = [cnt2, sum_e, sum_ie, [1], [1]]
    return r


def _twiddle(tw, se, w, mod):
    # tw[s+1] = tw[s] * se[bsf(~s)] を長さ w まで伸ばす
    s = len(tw)
    while s < w:
        t = tw[s - 1]
        u = s - 1
        tw.append(t * se[(~u & (u + 1)).bit_length() - 1] % mod)
        s += 1


def _butterfly(a, mod, pre):
    n = len(a)
    h = n.bit_length() - 1
    tw = pre[3]
    _twiddle(tw, pre[1], n >> 1, mod)
    for ph in range(1, h + 1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        if p >= w:
            for s in range(w):
                o = s * 2 * p
                t = tw[s]
                L = a[o:o + p]
                R = a[o + p:o + 2 * p]
                if t != 1:
                    R = [x * t % mod for x in R]
                a[o:o + p] = [(x + y) % mod for x, y in zip(L, R)]
                a[o + p:o + 2 * p] = [(x - y) % mod for x, y in zip(L, R)]
        else:
            T = tw[:w]
            q = 2 * p
            for i in range(p):
                L = a[i::q]
                R = [x * t % mod for x, t in zip(a[i + p::q], T)]
                a[i::q] = [(x + y) % mod for x, y in zip(L, R)]
                a[i + p::q] = [(x - y) % mod for x, y in zip(L, R)]


def _butterfly_inv(a, mod, pre):
    n = len(a)
    h = n.bit_length() - 1
    tw = pre[4]
    _twiddle(tw, pre[2], n >> 1, mod)
    for ph in range(h, 0, -1):
        w = 1 << (ph - 1)
        p = 1 << (h - ph)
        if p >= w:
            for s in range(w):
                o = s * 2 * p
                t = tw[s]
                L = a[o:o + p]
                R = a[o + p:o + 2 * p]
                a[o:o + p] = [(x + y) % mod for x, y in zip(L, R)]
                a[o + p:o + 2 * p] = [(x - y) * t % mod for x, y in zip(L, R)]
        else:
            T = tw[:w]
            q = 2 * p
            for i in range(p):
                L = a[i::q]
                R = a[i + p::q]
                a[i::q] = [(x + y) % mod for x, y in zip(L, R)]
                a[i + p::q] = [(x - y) * t % mod for x, y, t in zip(L, R, T)]


def _naive(a, b):
    if len(a) > len(b):
        a, b = b, a
    m = len(b)
    c = [0] * (len(a) + m - 1)
    for i, x in enumerate(a):
        if x:
            c[i:i + m] = [u + x * v for u, v in zip(c[i:i + m], b)]
    return c


def convolution(a, b, mod=998244353):
    '''
    NTT による畳み込み  O((N+M) log(N+M))  (ACL互換)
    mod は NTT-friendly な素数 (2^c | mod-1, len(a)+len(b)-1 <= 2^c)。
    min(len) <= 60 なら愚直。空配列なら []。
    ※ CPython では convolution_fast の方が速い。

    使用例:
        convolution([1, 2, 3], [4, 5])      # [4, 13, 22, 15]
        convolution(A, B, 924844033)        # 別の NTT 素数
    '''
    n, m = len(a), len(b)
    if not n or not m:
        return []
    if min(n, m) <= 60:
        return [x % mod for x in _naive(a, b)]
    pre = _prepare(mod)
    z = 1 << (n + m - 2).bit_length()
    assert z <= 1 << pre[0], "mod が NTT に対して小さすぎる"
    same = a is b
    a = [x % mod for x in a] + [0] * (z - n)
    _butterfly(a, mod, pre)
    if same:
        b = a
    else:
        b = [x % mod for x in b] + [0] * (z - m)
        _butterfly(b, mod, pre)
    c = [x * y % mod for x, y in zip(a, b)]
    _butterfly_inv(c, mod, pre)
    iz = pow(z, mod - 2, mod)
    return [x * iz % mod for x in c[:n + m - 1]]


_M1 = 754974721  # 2^24
_M2 = 167772161  # 2^25
_M3 = 469762049  # 2^26


def convolution_ll(a, b):
    '''
    整数のままの畳み込み (3つの NTT 素数 + CRT)  (ACL互換)
    結果の各要素の絶対値が M1*M2*M3/2 (約1.3e26) 未満なら正しい
    (ACL は int64 に収まる前提。こちらはそれより広い範囲で正しい)。負数OK。

    使用例:
        convolution_ll([10**9, -1], [10**9, 2])   # [10**18, 2*10**9 - 10**9, -2]
    '''
    n, m = len(a), len(b)
    if not n or not m:
        return []
    if min(n, m) <= 60:
        return _naive(a, b)
    c1 = convolution(a, b, _M1)
    c2 = convolution(a, b, _M2)
    c3 = convolution(a, b, _M3)
    M = _M1 * _M2 * _M3
    h = M >> 1
    m23, m13, m12 = _M2 * _M3, _M1 * _M3, _M1 * _M2
    i1 = pow(m23, -1, _M1)
    i2 = pow(m13, -1, _M2)
    i3 = pow(m12, -1, _M3)
    res = []
    for x, y, z in zip(c1, c2, c3):
        v = (x * i1 % _M1 * m23 + y * i2 % _M2 * m13 + z * i3 % _M3 * m12) % M
        res.append(v - M if v > h else v)
    return res


# ---- 10進パッキング (CPython 向け高速版) ----

def _dmul(a, b, w, L):
    # a, b: 非負整数列, w: 1要素あたりの桁数 (結果の各要素 < 10^w), L: 結果の長さ
    ctx = decimal.Context(prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN)
    fm = ('{:0%dd}' % w).format
    D = decimal.Decimal
    A = D(''.join(map(fm, a)))
    B = A if a is b else D(''.join(map(fm, b)))
    s = str(ctx.multiply(A, B)).zfill(w * L)
    return [int(s[i:i + w]) for i in range(0, w * L, w)]


def convolution_fast(a, b, mod=998244353):
    '''
    10進パッキングによる畳み込み  c[k] = sum a[i]*b[j] mod mod
    a, b を巨大な10進数にエンコードし decimal の積 (C実装) で計算する。
    CPython では NTT より約5倍速い。mod は任意 (素数でなくてよい)。

    使用例:
        convolution_fast([1, 2, 3], [4, 5])           # [4, 13, 22, 15]
        convolution_fast(A, B, 10**9 + 7)             # 任意 mod
    '''
    n, m = len(a), len(b)
    if not n or not m:
        return []
    if min(n, m) <= 60:
        return [x % mod for x in _naive(a, b)]
    w = len(str(min(n, m) * (mod - 1) ** 2))
    same = a is b
    a = [x % mod for x in a]
    b = a if same else [x % mod for x in b]
    return [x % mod for x in _dmul(a, b, w, n + m - 1)]


def convolution_ll_fast(a, b):
    '''
    10進パッキングによる厳密な整数畳み込み  (値の大きさ・符号に制限なし)
    負数は a[i] + Ma, b[j] + Mb と非負にずらして計算し、補正項を引く。
    (結果1要素が 4300 桁を超えると int(str) の桁数制限に掛かる。その場合は
     sys.set_int_max_str_digits(0) を呼ぶ。)

    使用例:
        convolution_ll_fast([10**18, -1], [10**18, 2])   # [10**36, 2*10**18 - 10**18, -2]
    '''
    n, m = len(a), len(b)
    if not n or not m:
        return []
    if min(n, m) <= 60:
        return _naive(a, b)
    L = n + m - 1
    Ma = -min(min(a), 0)
    Mb = -min(min(b), 0)
    same = a is b
    if Ma:
        a = [x + Ma for x in a]
    if same:
        b = a
    elif Mb:
        b = [x + Mb for x in b]
    w = len(str(min(n, m) * max(a) * max(b)))
    c = _dmul(a, b, w, L)
    if not Ma and not Mb:
        return c
    # (a+Ma)*(b+Mb) = a*b + Mb*(a*1) + Ma*(1*b) + Ma*Mb*(1*1)  (a, b はずらした後の値で計算)
    # => a*b = c - Mb*Sa - Ma*Sb + Ma*Mb*cnt   (Sa, Sb はずらした後の配列の区間和)
    pa = [0] * (n + 1)
    for i, x in enumerate(a):
        pa[i + 1] = pa[i] + x
    pb = [0] * (m + 1)
    for i, x in enumerate(b):
        pb[i + 1] = pb[i] + x
    MM = Ma * Mb
    for k in range(L):
        lo = k - m + 1 if k >= m else 0      # i の範囲 [lo, hi]
        hi = k if k < n else n - 1
        lo2 = k - n + 1 if k >= n else 0     # j の範囲
        hi2 = k if k < m else m - 1
        c[k] += MM * (hi - lo + 1) - Mb * (pa[hi + 1] - pa[lo]) - Ma * (pb[hi2 + 1] - pb[lo2])
    return c
