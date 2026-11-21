class ModInt:
    '''
    剰余環の整数 (ACL modint 相当)。法はクラス変数 ModInt.mod (デフォルト 998244353)。
    int と左右どちらでも演算可。割り算・inv は mod が素数 (または gcd=1) である前提。
    ※ 大量の演算ではオブジェクト生成が重いので、ホットループは素の int + % を推奨。

    使用例:
        ModInt.set_mod(10**9 + 7)    # 法の変更 (= ModInt.mod = 10**9 + 7)
        x = ModInt(3)
        y = x * 2 + 1 - ModInt(10)   # ModInt(998244350)
        z = 1 / x                    # 逆元 (= x.inv())
        x ** 10, x.pow(10), pow(x, -1)
        int(x), x.val(), x == 3      # 3, 3, True
    '''
    __slots__ = ('v',)
    mod = 998244353

    def __init__(self, v=0):
        self.v = v % ModInt.mod

    @staticmethod
    def set_mod(m):
        assert m >= 1
        ModInt.mod = m

    @classmethod
    def raw(cls, v):
        # 0 <= v < mod が保証されているとき剰余を省略して生成
        r = object.__new__(cls)
        r.v = v
        return r

    def val(self):
        return self.v

    def __int__(self):
        return self.v

    __index__ = __int__

    def __repr__(self):
        return str(self.v)

    def __hash__(self):
        return hash(self.v)

    def __eq__(self, o):
        if isinstance(o, ModInt):
            return self.v == o.v
        return self.v == o % ModInt.mod

    def __ne__(self, o):
        return not self == o

    def __bool__(self):
        return self.v != 0

    def __neg__(self):
        return ModInt.raw(-self.v % ModInt.mod)

    def __pos__(self):
        return self

    def __add__(self, o):
        return ModInt((self.v + o.v) if isinstance(o, ModInt) else (self.v + o))

    def __radd__(self, o):
        return ModInt(self.v + o)

    def __sub__(self, o):
        return ModInt((self.v - o.v) if isinstance(o, ModInt) else (self.v - o))

    def __rsub__(self, o):
        return ModInt(o - self.v)

    def __mul__(self, o):
        return ModInt((self.v * o.v) if isinstance(o, ModInt) else (self.v * o))

    def __rmul__(self, o):
        return ModInt(self.v * o)

    def __truediv__(self, o):
        m = ModInt.mod
        return ModInt(self.v * pow(o.v if isinstance(o, ModInt) else o, -1, m))

    def __rtruediv__(self, o):
        return ModInt(o * pow(self.v, -1, ModInt.mod))

    def __pow__(self, n, m=None):
        # 負の指数は逆元の累乗
        return ModInt.raw(pow(self.v, n, ModInt.mod))

    def pow(self, n):
        return ModInt.raw(pow(self.v, n, ModInt.mod))

    def inv(self):
        return ModInt.raw(pow(self.v, -1, ModInt.mod))
