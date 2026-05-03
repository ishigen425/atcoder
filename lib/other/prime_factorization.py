class factrize_osa_k():
    from collections import defaultdict
    '''
        高速素因数分解
        前処理 O(maxnum log log maxnum)
        素因数分解 O(log n)
    '''
    def __init__(self, maxnum):
        self.maxnum = maxnum
        self.sieve = [i for i in range(maxnum)]
        p = 2
        while p * p < maxnum:
            if self.sieve[p] == p:
                for q in range(2*p, maxnum, p):
                    if self.sieve[q] == q:
                        self.sieve[q] = p
            p += 1
    
    def calc_prime(self, a):
        d = defaultdict(int)
        while a > 1:
            d[self.sieve[a]] += 1
            a //= self.sieve[a]
        return d
    
    def is_prime(self, a):
        return self.sieve[a] == a

def prime_factorize(n):
    res, a = [], 2
    while a*a <= n:
        if n % a == 0:
            ex = 0
            while n % a == 0:
                ex += 1
                n //= a
            res.append((a, ex))
        a += 1
    if n != 1:
        res.append((n, 1))
    return res

# 約数列挙(1,N)も含まれる
# O (sqrt N)
prime, i = set(), 1
while i * i <= N:
    if N % i == 0:
        prime.add(i)
        prime.add(N//i)
    i += 1

# O (n log n)
def primes(n):
    '''
    素数テーブルの作成
    '''
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if not is_prime[i]:
            continue
        for j in range(i * 2, n + 1, i):
            is_prime[j] = False
    return is_prime
