MOD = 10**9 + 7
MAX = 10**6


def _build_factorials(max_size: int, mod: int) -> tuple[list[int], list[int]]:
    fact = [0] * max_size
    invfact = [0] * max_size

    fact[0] = 1
    for i in range(1, max_size):
        fact[i] = fact[i - 1] * i % mod

    invfact[max_size - 1] = pow(fact[max_size - 1], mod - 2, mod)
    for i in range(max_size - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % mod

    return fact, invfact


fact, invfact = _build_factorials(MAX, MOD)


def _validate_precomputed_range(n: int) -> None:
    if n >= MAX:
        raise ValueError(f"n={n} is out of precomputed range. Increase MAX ({MAX}).")


def nCk(n: int, k: int) -> int:
    if n < 0 or k < 0 or n < k:
        return 0
    _validate_precomputed_range(n)
    k = min(k, n - k)
    return fact[n] * invfact[k] % MOD * invfact[n - k] % MOD


def nPk(n: int, k: int) -> int:
    if n < 0 or k < 0 or n < k:
        return 0
    _validate_precomputed_range(n)
    return fact[n] * invfact[n - k] % MOD


def P(n: int) -> int:
    return nPk(n, n)


def calc_comb(n: int, k: int, mod: int) -> int:
    """n が大きい場合に使う O(k) の組み合わせ計算。"""
    if n < 0 or k < 0 or n < k:
        return 0

    k = min(k, n - k)
    denominator = 1
    numerator = 1

    for i in range(1, k + 1):
        denominator = denominator * i % mod
        numerator = numerator * (n - i + 1) % mod

    return numerator * pow(denominator, mod - 2, mod) % mod
