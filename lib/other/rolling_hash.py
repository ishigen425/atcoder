import random


class RollingHash:
    '''
    ローリングハッシュ  mod = 2^61-1, 基数はランダム (hack・衝突対策)
    基数はクラス共通なので、別の文字列同士のハッシュも比較できる
    前処理 O(N), 部分文字列ハッシュ O(1)

    使用例:
        rh = RollingHash("abcabc")      # str でも list[int] でも可
        rh.get(0, 3) == rh.get(3, 6)    # True  s[0:3] == s[3:6]
        t = RollingHash("bca")
        rh.get(1, 4) == t.get(0, 3)     # True  別文字列とも比較可
        rh.lcp(0, 3)                    # 3  s[0:] と s[3:] の最長共通接頭辞
        RollingHash.connect(h1, h2, len2)  # hash(A + B)
        rh.find("bc")                   # [1, 4]  パターンの出現位置

        回文判定: rev = RollingHash(s[::-1]);  s[l:r] が回文
            ⇔ rh.get(l, r) == rev.get(n - r, n - l)
    '''
    MOD = (1 << 61) - 1
    BASE = random.randrange(10 ** 5, (1 << 61) - 2)
    _pw = [1]

    def __init__(self, s):
        MOD, B = self.MOD, self.BASE
        n = len(s)
        if isinstance(s, str):
            s = [ord(c) for c in s]
        h = [0] * (n + 1)
        x = 0
        for i, c in enumerate(s):
            x = (x * B + c + 1) % MOD
            h[i + 1] = x
        self.h = h
        self.n = n
        self._ensure(n)

    @classmethod
    def _ensure(cls, n):
        pw = cls._pw
        if len(pw) <= n:
            MOD, B = cls.MOD, cls.BASE
            x = pw[-1]
            for _ in range(n + 1 - len(pw)):
                x = x * B % MOD
                pw.append(x)

    def get(self, l, r):
        '''s[l:r] のハッシュ'''
        return (self.h[r] - self.h[l] * self._pw[r - l]) % self.MOD

    @classmethod
    def connect(cls, h1, h2, len2):
        '''hash(A) と hash(B) (|B| = len2) から hash(A + B)'''
        cls._ensure(len2)
        return (h1 * cls._pw[len2] + h2) % cls.MOD

    def lcp(self, i, j, other=None):
        '''self[i:] と other[j:] (省略時は self) の最長共通接頭辞長  O(log N)'''
        o = self if other is None else other
        lo, hi = 0, min(self.n - i, o.n - j)
        while lo < hi:
            m = (lo + hi + 1) >> 1
            if self.get(i, i + m) == o.get(j, j + m):
                lo = m
            else:
                hi = m - 1
        return lo

    def find(self, pattern):
        '''pattern の出現開始位置リスト  O(N + M)'''
        p = pattern if isinstance(pattern, RollingHash) else RollingHash(pattern)
        m = p.n
        target = p.get(0, m)
        h, pw, MOD = self.h, self._pw[m], self.MOD
        return [i for i in range(self.n - m + 1) if (h[i + m] - h[i] * pw) % MOD == target]
