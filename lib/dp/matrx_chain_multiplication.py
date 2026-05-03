# 区間DP（連鎖行列積の最適化）
# https://onlinejudge.u-aizu.ac.jp/problems/ALDS1_10_B
N = int(input())
R = [0]*N
C = [0]*N
for i in range(N):
    R[i], C[i] = map(int, input().split())

INF = 10**18
dp = [[INF]*N for i in range(N)]
# 対角成分は0埋めする
for i in range(N):
    dp[i][i] = 0
# lは対象区間の長さを表す
for l in range(1, N):
    # iは対象区間の左端
    for i in range(N-l):
        a0 = R[i]
        c0 = C[i+l]
        tmp = INF
        for j in range(i, i+l):
            p = dp[i][j]
            q = dp[j+1][i+l]
            r = a0*C[j]*c0
            tmp = min(tmp, a0*C[j]*c0 + dp[i][j] + dp[j+1][i+l])
        dp[i][i+l] = tmp
print(dp[0][N-1])

