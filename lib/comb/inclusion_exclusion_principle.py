# 以下の要件を満たす、n個の区別できるボールをk個の区別できる箱に入れる方法は何通りあるか?
# どのボールも必ずいずれかの箱に入れる
# どの箱にもひとつ以上のボールを入れる
# 全パターンは k ** n
# そこから控除原理で +少なくとも空箱が1つできる場合 -少なくとも空箱が2つできる場合 +.....と計算していく
N, K = map(int, input().split())

# pypyで通す
def createFacArr(n, mod):
    '''
    二項係数計算用の配列の作成

    Parameters
    n : int
        配列のサイズ
    mod : int
        あまり

    Returns
    fac : list
        階乗のリスト
    finv : list
        modの逆元のリスト
    ivn : list
    '''
    fac = [0] * n
    finv = [0] * n
    inv = [0] * n
    fac[0], fac[1] = 1, 1
    finv[0], finv[1] = 1, 1
    inv[1] = 1
    for i in range(2, n):
        fac[i] = fac[i-1] * i % mod
        inv[i] = mod - inv[mod%i] * (mod // i) % mod
        finv[i] = finv[i-1] * inv[i] % mod
    return fac, finv

def comb(n ,k, mod, fac, finv):
    '''
    二項係数の計算

    Parameters
    n : int
        元集合
    k : int
        元集合から選択する数
    mod : int
        あまり
    fac : list
        階乗のリスト
    finv : list
        逆元のリスト
    
    Returns
    c : int
        nCkの組み合わせの数
    '''
    if n < k:
        return 0
    if n < 0 or k < 0:
        return 0
    return fac[n] * (finv[k] * finv[n-k] % mod) % mod
mod = 10 ** 9 + 7
fac, finv = createFacArr(10000, mod)
ans = 0
for i in range(1, K+1):
    rest = K - i
    val = comb(K, i, mod, fac, finv) * pow(rest, N, mod) % mod
    if i % 2 == 1: ans = (ans + val) % mod
    else: ans = (ans - val + mod) % mod

ans = (pow(K, N, mod) - ans + mod) % mod
print(ans)
