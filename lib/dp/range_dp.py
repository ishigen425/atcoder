# 区間DP
# https://atcoder.jp/contests/joi2015ho/tasks/joi2015ho_b
import sys
sys.setrecursionlimit(10**9)

n = int(input())
a = [int(input()) for i in range(n)]
# 円状のもののどこか一部を除くという処理を2倍にした配列を用いることで除く場所から後ろn個という範囲に変換している
a = a + a
# dp[i][j] := iからjのケーキが残っている状態で、joi君が最終的に獲得できるスコア
dp = [[-1] * (n+n) for i in range(n+n)]

def f(i, j):
    if dp[i][j] >= 0: return dp[i][j]
    if (j-i+1) % 2 == n % 2:
        # joi君のターン
        if i == j:
            # joi君のターンで最後の一つを取る場合(nが奇数)
            dp[i][j] = a[i]
        else:
            # a[i] を取って取った後の最大値 と a[j]を取って取った後の最大値
            dp[i][j] = max(f(i+1,j)+ a[i], f(i,j-1)+a[j])
    else:
        # ioiちゃんのターン
        if i == j:
            # ioiちゃんのターンで最後の一つを取る場合(nが偶数) joi君には得点が入らないので0にする
            dp[i][j] = 0
        else:
            # ioiちゃんは貪欲的に取れるほうのうち大きいほうを取る(スコアは加算しない)
            if a[i] > a[j]:
                dp[i][j] = f(i+1, j)
            else:
                dp[i][j] = f(i,j-1)
    return dp[i][j]

# joiくんが一番最初に選択するケーキを全探索する
ans = 0
for i in range(n):
    tmp = f(i+1,i+n-1) + a[i] # i番目を取ってから、余りのケーキでの最大化をdpで取る
    ans = max(ans, tmp)

print(ans)


# https://atcoder.jp/contests/past202012-open/submissions/20277888

N = int(input())
S = "x" + input() + "x"
T = input()

dp = [[0] * 110 for _ in range(110)]
for diff in range(2, N):
    for l in range(1, N+1):
        r = l+diff
        if r > N+1: continue
        tmp = max(dp[l-1][r], dp[l][r-1])
        for m in range(l+1, r):
            tmp = max(tmp, dp[l][m-1] + dp[m][r])
            judge = True
            judge &= dp[l+1][m-1] == m-l-1 or m-l == 1
            judge &= dp[m+1][r-1] == r-m-1 or r-m == 1
            judge &= S[l] + S[m] + S[r] == T
            if judge:
                tmp = max(tmp, r-l+1)
        dp[l][r] = tmp

print(dp[1][N]//3)


