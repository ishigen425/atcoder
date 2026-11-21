class Doubling:
    '''
    ダブリング  「x から K 回遷移した先」を O(log K) で
    前処理 O(N log K)   nxt[x]: x の1回遷移先 (0-indexed)
    weight を渡すと、K 回遷移で通過した重みの総和も求まる (遷移元の重みを加算)

    使用例:
        db = Doubling(nxt, 10**18)
        db.kth(x, K)                 # K 回後の位置
        db = Doubling(nxt, 10**18, weight=A)
        pos, s = db.kth_sum(x, K)    # 位置と、通過した A[x] の総和
    '''
    def __init__(self, nxt, max_k, weight=None):
        self.log = max(max_k.bit_length(), 1)
        n = len(nxt)
        self.table = [list(nxt)]
        self.wsum = None
        if weight is not None:
            self.wsum = [list(weight)]
        for _ in range(self.log - 1):
            p = self.table[-1]
            self.table.append([p[p[i]] for i in range(n)])
            if weight is not None:
                w = self.wsum[-1]
                self.wsum.append([w[i] + w[p[i]] for i in range(n)])

    def kth(self, x, k):
        t = self.table
        i = 0
        while k:
            if k & 1:
                x = t[i][x]
            k >>= 1
            i += 1
        return x

    def kth_sum(self, x, k):
        t, w = self.table, self.wsum
        s = 0
        i = 0
        while k:
            if k & 1:
                s += w[i][x]
                x = t[i][x]
            k >>= 1
            i += 1
        return x, s
