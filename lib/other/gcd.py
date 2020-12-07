
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

