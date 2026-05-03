
# 1からNまでの互いに素な数の個数を求める
from itertools import product
N = int(input())
origN = N
div = []
d = 2
while d * d <= N:
    if N % d == 0:
        div.append(d)
        while N % d == 0: N //= d
    d += 1

if N != 1:
    div.append(N)

M = len(div)
ans = 0

# Nの素因数を求めて、素因数の倍数の個数を足し引きしてNと互いに素ではない数の個数を求める
# 条件の個数が偶数個の場合は足して、奇数個の場合は引いて求める

for p in product(range(2), repeat=M):
    if sum(p) == 0:
        continue
    popcnt, mul = 0, 1
    for i in range(M):
        if p[i] == 1:
            mul *= div[i]
            popcnt += 1
    if popcnt % 2 == 1:
        ans += origN // mul
    else:
        ans -= origN // mul

ans = origN - ans
print(ans)

