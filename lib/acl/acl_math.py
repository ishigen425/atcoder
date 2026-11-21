# ファイル名を math.py にしないのは、このディレクトリでスクリプトを実行したときに
# 標準ライブラリの math を上書き (shadow) してしまうため。


def pow_mod(x, n, m):
    '''
    x^n mod m  (ACL互換, 0 <= n, 1 <= m)

    使用例:
        pow_mod(2, 10, 1000)   # 24
        pow_mod(-3, 3, 5)      # 3  (負の x も可)
        pow_mod(5, 0, 1)       # 0
    '''
    return pow(x, n, m)


def inv_mod(x, m):
    '''
    x の mod m における逆元  (ACL互換, gcd(x, m) == 1, 1 <= m)
    戻り値は 0 <= y < m

    使用例:
        inv_mod(3, 7)    # 5  (3 * 5 = 15 ≡ 1)
        inv_mod(-1, 7)   # 6
    '''
    return pow(x, -1, m)  # gcd(x, m) != 1 なら ValueError


def crt(r, m):
    '''
    中国剰余定理  (ACL互換)
    x ≡ r[i] (mod m[i]) を全て満たす x を (y, z) = (x mod z, lcm(m)) で返す
    解なしなら (0, 0)、空入力なら (0, 1)。法は互いに素でなくてよい。r は負でもよい。

    使用例:
        crt([2, 3, 2], [3, 5, 7])   # (23, 105)
        crt([1, 2], [4, 6])         # (0, 0)  解なし
        crt([3, 5], [4, 6])         # (11, 12)
    '''
    assert len(r) == len(m)
    r0, m0 = 0, 1
    for r1, m1 in zip(r, m):
        assert m1 >= 1
        r1 %= m1
        if m0 < m1:
            r0, r1 = r1, r0
            m0, m1 = m1, m0
        if m0 % m1 == 0:
            if r0 % m1 != r1:
                return (0, 0)
            continue
        # g = gcd(m0, m1), im = (m0/g)^-1 mod (m1/g)
        a, b, x0, x1 = m0, m1, 1, 0
        while b:
            t = a // b
            a, b = b, a - t * b
            x0, x1 = x1, x0 - t * x1
        g = a
        d = r1 - r0
        if d % g:
            return (0, 0)
        u1 = m1 // g
        x = d // g * x0 % u1
        r0 += x * m0
        m0 *= u1
    return (r0 % m0, m0)


def floor_sum(n, m, a, b):
    '''
    sum_{i=0}^{n-1} floor((a*i + b) / m)  O(log m)  (ACL互換)
    0 <= n, 1 <= m。a, b は負でもよい (現行ACLと同じ)。
    Python の多倍長整数なので ACL の n, m < 2^32 制約はない。

    使用例:
        floor_sum(4, 10, 6, 3)    # 3   (0+0+1+2)
        floor_sum(5, 3, -2, -1)   # -10
    '''
    assert n >= 0 and m >= 1
    ans = 0
    # a, b を [0, m) に正規化 (負でも // は床関数なので正しい)
    if a >= m or a < 0:
        q, a = divmod(a, m)
        ans += n * (n - 1) // 2 * q
    if b >= m or b < 0:
        q, b = divmod(b, m)
        ans += n * q
    while True:
        if a >= m:
            q, a = divmod(a, m)
            ans += n * (n - 1) // 2 * q
        if b >= m:
            q, b = divmod(b, m)
            ans += n * q
        y_max = a * n + b
        if y_max < m:
            break
        n, b = divmod(y_max, m)
        m, a = a, m
    return ans
