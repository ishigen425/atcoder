
def gcd(x, y):
    '''
    最大公約数の計算
    '''
    if y == 0:
        return x
    return gcd(y, x % y)

def lcm(x, y):
    '''
    最小公倍数の計算
    '''
    return (x * y) // gcd(x, y)

def mult(x, y):
    amount = 0
    shited_x = x
    for i in range(16):
        if (y >> i) & 1:
            amount += shited_x
        shited_x = shited_x << 1
    return amount

def divide(x, y):
    if y > x: return 0
    q = divide(x, 2 * y)
    if x - (2 * q * y) < y:
        return 2 * q
    else:
        return 2 * q + 1

#print(3&2)
#print(mult(2,53))
#print(divide(5, 1))

# Euclidean Algorithm
def gcd(m, n):
    r = m % n
    return gcd(n, r) if r else n

# Euclidean Algorithm (non-recursive)
def gcd2(m, n):
    while n:
        m, n = n, m % n
    return m

# Extended Euclidean Algorithm
def extgcd(a, b):
    if b:
        d, y, x = extgcd(b, a % b)
        y -= (a // b)*x
        return d, x, y
    return a, 1, 0

# lcm (least common multiple)
def lcm(m, n):
    return m//gcd(m, n)*n


def inv_gcd(a, b):
    a %= b
    if a == 0: return b, 0
    s, t = b, a
    m0, m1 = 0, 1
    while t:
        u = s // t
        s -= t * u
        m0 -= m1 * u
        s, t = t, s
        m0, m1 = m1, m0

    if m0 < 0: m0 += b // s
    return s, m0


def crt(r, m):
    """
    Parameters
        r : list[int, int] あまりのリスト
        m : list[int, int] modNのリスト
    """
    assert len(r) == len(m)
    n = len(r)
    r0, m0 = 0, 1
    for i in range(n):
        assert m[i] >= 1
        r1, m1 = r[i] % m[i], m[i]
        if m0 < m1:
            r0, r1 = r1, r0
            m0, m1 = m1, m0
        if m0 % m1 == 0:
            if r0 % m1 != r1: return [0, 0]
            continue
        g, im = inv_gcd(m0, m1)
        if (r1 - r0) % g: return [0, 0]
        u1 = m0 * m1 // g
        r0 += (r1 - r0) // g * m0 * im % u1
        m0 = u1
    return [r0, m0]
