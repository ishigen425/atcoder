# SquareDivisionによるRMQ
import math
class SquareDivision():
    def __init__(self, n, array):
        self.MAX_NUM = 10 ** 18
        self.n = n
        self.bucket_size = math.floor(math.sqrt(n))
        self.bucket_count = math.ceil(n / self.bucket_size)
        self.bucket = [[] for _ in range(self.bucket_count)]
        self.bucket_min = [self.MAX_NUM] * (self.bucket_count+1)
        tmp = self.MAX_NUM
        for i, a in enumerate(array):
            bucket_idx, item_idx = self._get_idx(i)
            self.bucket[bucket_idx].append(a)
            if item_idx == self.bucket_size - 1:
                self.bucket_min[bucket_idx] = tmp
                tmp = self.MAX_NUM
            else:
                tmp = min(tmp, a)
        if tmp < self.MAX_NUM:
            self.bucket_min[bucket_idx] = tmp

    def _get_idx(self, i):
        return i // self.bucket_size, i % self.bucket_size

    def update(self, idx, a):
        bucket_idx, item_idx = self._get_idx(idx)
        self.bucket[bucket_idx][item_idx] = a
        self.bucket_min[bucket_idx] = min(self.bucket[bucket_idx])
    
    def query(self, l, r):
        ret = self.MAX_NUM
        l_bucket_idx, l_item_idx = self._get_idx(l)
        r_bucket_idx, r_item_idx = self._get_idx(r)
        if r_bucket_idx - l_bucket_idx < 1:
            for i in range(l_item_idx, min(r_item_idx, len(self.bucket[l_bucket_idx]))):
                ret = min(ret, self.bucket[l_bucket_idx][i])
            return ret
        # l_bucket_idxははみ出している部分のインデックスなので、+1した場所から数える
        for i in range(l_bucket_idx+1, r_bucket_idx):
            ret = min(ret, self.bucket_min[i])
        # 左にはみ出す部分
        for i in range(l_item_idx, len(self.bucket[l_bucket_idx])):
            ret = min(ret, self.bucket[l_bucket_idx][i])
        # 右にはみ出す部分
        for i in range(r_item_idx):
            ret = min(ret, self.bucket[r_bucket_idx][i])
        return ret

N, Q = map(int, input().split())
MAX_NUM = 2 ** 31 - 1
A = [MAX_NUM] * N
sd = SquareDivision(N, A)
for i in range(Q):
    c, l, r = map(int, input().split())
    if c == 0:
        sd.update(l, r)
    else:
        print(sd.query(l, r+1))


################################################################

# SquareDivisionによるRSQ
import math
class SquareDivision():
    def __init__(self, n, array):
        self.MAX_NUM = 10 ** 18
        self.n = n
        self.bucket_size = math.floor(math.sqrt(n))
        self.bucket_count = math.ceil(n / self.bucket_size)
        self.bucket = [[] for _ in range(self.bucket_count)]
        self.bucket_sum = [self.MAX_NUM] * (self.bucket_count+1)
        tmp = 0
        for i, a in enumerate(array):
            bucket_idx, item_idx = self._get_idx(i)
            self.bucket[bucket_idx].append(a)
            if item_idx == self.bucket_size - 1:
                self.bucket_sum[bucket_idx] = tmp
                tmp = 0
            else:
                tmp += a
        if tmp < self.MAX_NUM:
            self.bucket_sum[bucket_idx] = tmp

    def _get_idx(self, i):
        return i // self.bucket_size, i % self.bucket_size

    def update(self, idx, a):
        bucket_idx, item_idx = self._get_idx(idx)
        self.bucket[bucket_idx][item_idx] += a
        self.bucket_sum[bucket_idx] += a
    
    def query(self, l, r):
        ret = 0
        l_bucket_idx, l_item_idx = self._get_idx(l)
        r_bucket_idx, r_item_idx = self._get_idx(r)
        if r_bucket_idx - l_bucket_idx < 1:
            for i in range(l_item_idx, min(r_item_idx, len(self.bucket[l_bucket_idx]))):
                ret += self.bucket[l_bucket_idx][i]
            return ret
        # l_bucket_idxははみ出している部分のインデックスなので、+1した場所から数える
        for i in range(l_bucket_idx+1, r_bucket_idx):
            ret += self.bucket_sum[i]
        # 左にはみ出す部分
        for i in range(l_item_idx, len(self.bucket[l_bucket_idx])):
            ret += self.bucket[l_bucket_idx][i]
        # 右にはみ出す部分
        for i in range(r_item_idx):
            ret += self.bucket[r_bucket_idx][i]
        return ret

N, Q = map(int, input().split())
MAX_NUM = 2 ** 31 - 1
A = [0] * N
sd = SquareDivision(N, A)
for i in range(Q):
    c, l, r = map(int, input().split())
    if c == 0:
        sd.update(l-1, r)
    else:
        print(sd.query(l-1, r))

