MOD = 10 ** 9 + 7
MAX = 10 ** 6
fact = [0] * MAX
invfact = [0] * MAX
fact[0] = 1
for i in range(1, MAX):
    fact[i] = fact[i - 1] * i % MOD
invfact[MAX - 1] = pow(fact[MAX - 1], MOD-2, MOD)
for i in range(MAX - 2, -1, -1):
    invfact[i] = invfact[i+1] * (i+1) % MOD

def nCk(n, k):
    if k < 0 or n < k: return 0
    return (fact[n] * invfact[k] % MOD) * invfact[n-k] % MOD

def nPk(n, k):
    if k < 0 or n < k: return 0
    return fact[n] * invfact[n-k] % MOD

def P(n):
    return nPk(n, n)

def calc_comb(n, k, mod):
    '''
        n が大きい場合に使う
    '''
    a = 1
    b = 1
    for i in range(1,k+1):
        a *= i
        a %= mod
        b *= n
        n -= 1
        b %= mod
    return b * pow(a, mod-2, mod) % mod
