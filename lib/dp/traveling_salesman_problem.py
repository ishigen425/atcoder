# bitDP DPの添字の一つの数字をbitでの集合に見立てて、状態を管理する
# 巡回セールスマン問題
V, E = map(int, input().split())
d = [[10 ** 9] * V for _ in range(V)]
dp = [[-1] * V for _ in range((1 << V))]
for i in range(E):
    s, t, di = map(int, input().split())
    d[s][t] = di

def rec(S, v, dp):
    # メモ化再帰なのですでに探索済みなら値を返却する
    if dp[S][v] >= 0: return dp[S][v]
    # S == (1 << V) - 1はSを二進数表記したときに全てのbitが1であるかどうかを判定している
    # Sの全てのbitが1かつ、v(現在のノード)が0のときは、一周巡回したということになるので、dp[S][v]=0を設定する
    if (S == ((1 << V) - 1)) and v == 0:
        dp[S][v] = 0
        return 0
    res = 10 ** 9
    for u in range(V):
        # 集合Sを右シフトして左からu番目のbitが0の場合、到達していないノードという判定になるから、そのノードの最短経路を求めにいく
        if (S >> u & 1) == 0:
            # 集合Sに対して、今から調査するノードを整数で表すと(1 << u)となるので、S | (1 << u)を引数にする
            # ちなみにS >> u & 1 == 0であることが確定しているので、orだけじゃなくて加算しても動く
            res = min(res, rec(S + (1 << u), u, dp) + d[v][u])
    dp[S][v] = res
    return dp[S][v]

ans = rec(0, 0, dp)
print(ans if ans < 10 ** 9 else -1)

# 入力想定
# ノードの数, 辺の数
# from, to, weight
# ...

from itertools import permutations
from collections import Counter
N, M = map(int, input().split())
A = [int(input()) for _ in range(N)]
c = Counter(A)


def make_camulative_sum_array():
    camulative = [[0] * (N+1) for _ in range(M+1)]
    for i, a in enumerate(A):
        camulative[a][i+1] = 1
    for i in range(M+1):
        for j in range(N):
            camulative[i][j+1] += camulative[i][j]
    return camulative

# 二次元の累積和
# camulative[i][j] := 種類iのぬいぐるみが初期状態の陳列でjまでに並んでいる個数
camulative = make_camulative_sum_array()


dp = [10 ** 9] * (2 ** M)
# 集合0(何も陳列されていない状態)を作るコストは0
dp[0] = 0
# total[i] := 集合iの状態ですでに並んでいるぬいぐるみの数
total = [0] * (2**M)
for i in range(2**M):
    for j in range(M):
        if i >> j & 1: continue
        # 今回追加する種類のぬいぐるみの個数
        target_cnt = c[j+1]
        # 集合iの状態ですでに並んでいるぬいぐるみの個数
        total_cnt = total[i]
        # 集合iに今回追加する種類を追加した集合にぬいぐるみの総数を格納する
        total[i + (2 ** j)] = total_cnt + target_cnt
        # cost := 今回追加する種類のぬいぐるみで動かさないといけないもの(今回追加する種類のぬいぐるみの個数 - すでに今回追加する種類のぬいぐるみが並んでいた個数)
        cost = target_cnt - (camulative[j+1][total_cnt + target_cnt] - camulative[j+1][total_cnt])
        # 今のdp配列に入っているものと今回の種類追加の順番で発生するコストを比較して小さい方を入れる
        dp[i + (2 ** j)] = min(dp[i + (2 ** j)], dp[i] + cost)

print(dp[-1])

# https://atcoder.jp/contests/joi2017yo/submissions/me

from itertools import permutations
from collections import Counter
N, M = map(int, input().split())
A = [int(input()) for _ in range(N)]
c = Counter(A)


def make_camulative_sum_array():
    camulative = [[0] * (N+1) for _ in range(M+1)]
    for i, a in enumerate(A):
        camulative[a][i+1] = 1
    for i in range(M+1):
        for j in range(N):
            camulative[i][j+1] += camulative[i][j]
    return camulative

# 二次元の累積和
# camulative[i][j] := 種類iのぬいぐるみが初期状態の陳列でjまでに並んでいる個数
camulative = make_camulative_sum_array()


dp = [10 ** 9] * (2 ** M)
# 集合0(何も陳列されていない状態)を作るコストは0
dp[0] = 0
# total[i] := 集合iの状態ですでに並んでいるぬいぐるみの数
total = [0] * (2**M)
for i in range(2**M):
    for j in range(M):
        if i >> j & 1: continue
        # 今回追加する種類のぬいぐるみの個数
        target_cnt = c[j+1]
        # 集合iの状態ですでに並んでいるぬいぐるみの個数
        total_cnt = total[i]
        # 集合iに今回追加する種類を追加した集合にぬいぐるみの総数を格納する
        total[i + (2 ** j)] = total_cnt + target_cnt
        # cost := 今回追加する種類のぬいぐるみで動かさないといけないもの(今回追加する種類のぬいぐるみの個数 - すでに今回追加する種類のぬいぐるみが並んでいた個数)
        cost = target_cnt - (camulative[j+1][total_cnt + target_cnt] - camulative[j+1][total_cnt])
        # 今のdp配列に入っているものと今回の種類追加の順番で発生するコストを比較して小さい方を入れる
        dp[i + (2 ** j)] = min(dp[i + (2 ** j)], dp[i] + cost)

print(dp[-1])
