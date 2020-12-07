class SegT():
    # originは初期データがあれば渡す
    def __init__(self, size, origin=None):
        self.size = 1
        while self.size < size: self.size *= 2
        self._data_init()
        if origin:
            for i in range(size):
                self.data[i+self.size-1] = origin[i]
            for i in range(self.size-2,-1,-1):
                self.data[i] = self._calc(self.data[i*2+1], self.data[i*2+2])

    def _data_init(self):
        self.e = pow(2, 31)-1 # 単位元
        self.data = [self.e for _ in range(self.size * 2 - 1)]

    def _calc(self, a, b):
        # ここは独自実装する
        return min(a, b)
    
    def update(self, i, x):
        i += (self.size - 1)
        self.data[i] = x
        while i > 0:
            i = (i - 1) // 2
            self.data[i] = self._calc(self.data[i*2+1], self.data[i*2+2])
        
    def get(self, a, b, node=0, l=0, r=-1):
        if r < 0: r = self.size
        if r <= a or b <= l: return self.e
        if a <= l and r <= b: return self.data[node]
        vl = self.get(a, b, node*2+1, l, (l+r)//2)
        vr = self.get(a, b, node*2+2, (l+r)//2, r)
        return self._calc(vl, vr)

