class Sieve:
    '''
    エラトステネスの篩 + 最小素因数(SPF)テーブル
    前処理 O(N log log N) (内側はスライス代入でC速度)  N=10^7 でも数秒以内

    使用例:
        sv = Sieve(10**6)
        sv.is_prime(97)          # True  O(1)
        sv.primes                # N以下の素数リスト
        sv.factorize(360)        # [(2, 3), (3, 2), (5, 1)]  O(log x)
        sv.divisors(12)          # [1, 2, 3, 4, 6, 12]  (ソート済み)
        sv.count_divisors(360)   # 24
        sv.totient(36)           # 12  オイラーのφ
    '''
    def __init__(self, n):
        n = max(n, 1)
        self.n = n
        spf = list(range(n + 1))
        r = int(n ** 0.5)
        while r * r > n: r -= 1
        while (r + 1) * (r + 1) <= n: r += 1
        # 大きい素数から書き込み、最後に小さい素数で上書き → 最小素因数が残る
        small = [p for p in range(2, r + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
        for p in reversed(small):
            spf[p * p::p] = [p] * ((n - p * p) // p + 1)
        self.spf = spf
        self.primes = [i for i in range(2, n + 1) if spf[i] == i]

    def is_prime(self, x):
        return x >= 2 and self.spf[x] == x

    def factorize(self, x):
        spf = self.spf
        res = []
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            res.append((p, e))
        return res

    def divisors(self, x):
        ds = [1]
        for p, e in self.factorize(x):
            ds = [d * pk for d in ds for pk in [p ** k for k in range(e + 1)]]
        ds.sort()
        return ds

    def count_divisors(self, x):
        c = 1
        for _, e in self.factorize(x):
            c *= e + 1
        return c

    def totient(self, x):
        for p, _ in self.factorize(x):
            x -= x // p
        return x


def is_prime_table(n):
    '''
    素数判定テーブルのみ (メモリ軽量 bytearray)  is_p[i] == 1 なら素数
    '''
    is_p = bytearray([1]) * (n + 1)
    is_p[0] = 0
    if n >= 1: is_p[1] = 0
    p = 2
    while p * p <= n:
        if is_p[p]:
            is_p[p * p::p] = bytes((n - p * p) // p + 1)
        p += 1
    return is_p


def divisors(n):
    '''
    約数列挙 O(sqrt N)  篩なしで単発の大きいN (~10^12) 向け
    '''
    lo, hi = [], []
    i = 1
    while i * i <= n:
        if n % i == 0:
            lo.append(i)
            if i != n // i: hi.append(n // i)
        i += 1
    return lo + hi[::-1]
