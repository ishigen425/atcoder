# 二次元累積和
N,M,Q = map(int, input().split())

train = [[0 for _ in range(N+1)] for _ in range(N+1)]

for i in range(M):
    l,r = map(int, input().split())
    train[l][r] += 1

for i in range(1, N+1):
    for j in range(1, N+1):
        train[i][j] += train[i-1][j] + train[i][j-1] - train[i-1][j-1] 

for _ in range(Q):
    p,q = map(int, input().split())

    print(train[q][q] - train[p-1][q] - train[q][p-1] + train[p-1][p-1])

# https://twitter.com/home
# https://qiita.com/drken/items/56a6b68edef8fc605821

