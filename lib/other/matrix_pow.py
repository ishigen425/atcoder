def mat_mul(A, B, mod):
    '''行列積 (A: n×m, B: m×p)  O(nmp)'''
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) % mod for col in Bt] for row in A]


def mat_pow(A, k, mod):
    '''
    行列累乗 A^k  O(n^3 log k)
    線形漸化式を N ≤ 10^18 で解く定番

    使用例 (フィボナッチ F(n) mod 998244353):
        M = [[1, 1], [1, 0]]
        F_n = mat_pow(M, n, MOD)[0][1]

    一般に x_{i+1} = A x_i なら x_k = A^k x_0 → mat_vec(mat_pow(A, k, MOD), x0, MOD)
    '''
    n = len(A)
    R = [[int(i == j) for j in range(n)] for i in range(n)]
    A = [row[:] for row in A]
    while k:
        if k & 1:
            R = mat_mul(R, A, mod)
        A = mat_mul(A, A, mod)
        k >>= 1
    return R


def mat_vec(A, x, mod):
    '''行列 × ベクトル'''
    return [sum(a * b for a, b in zip(row, x)) % mod for row in A]
