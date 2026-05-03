# bit全探索
for i in range(2**N):
    for j in range(N):
        if (i >> j) & 1:

from itertools import product
for p in product(range(2), repeat=N):
    pass
