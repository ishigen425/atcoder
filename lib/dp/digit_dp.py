# 桁DP
# https://atcoder.jp/contests/abc154/submissions/11262492
N = input()
K = int(input())

def solve(N, K):
    l = len(N)
    # dp[桁数][n未満フラグ][0以外の数の個数]
    dp = [[[0] * (10) for i in range(2)] for _ in range(l+1)]
    dp[0][0][0] = 1
    for i in range(l):
        D = int(N[i])
        for j in range(2):
            for k in range(K+1):
                for d in range(10):
                    if j == 0 and d > D: break
                    # dが0のときは数が変わらない、ずっと1であるまま
                    # dが0以外のとき0以外の数がi+1で増えるので、k+1する
                    dp[i+1][j or (d < D)][k if d == 0 else k+1] += dp[i][j][k]
    
    return dp[l][0][K] + dp[l][1][K]

print(solve(N,K))

# https://atcoder.jp/contests/abc135/submissions/11335832
S = input()
L = len(S)

MOD = 10 ** 9 + 7
dp = [[0] * 13 for _ in range(10**5+10)]
dp[0][0] = 1
for i in range(L):
    j = -1 if S[i] == "?" else int(S[i])
    if j > -1:
        # jが確定しているので、jを全探索する必要はなく、前回桁までの組み合わせの数にjを足して次のDPへ入れる
        # jが確定しているから数字の組み合わせ自体が増えるわけではない
        # そのためこれまで確定していた桁に対して、jを追加した場合のあまりを単純に移送することになる
        
        # 前回桁までの数 * 10 + j をすると、今回桁をjにしたときのあまりがわかる
        # 3?1 → 301 % 13 = 2, 30 % 13 = 4であるから、ki=4のとき、dp[i][4]の数値をdp[i+1][2]に足す
        # 30と4はmod13の世界では合同になっている
        # すなわち*10した結果である300と40も合同
        # そこにjを足した数 300+jと40+jもまた合同であると言える、ともにあまりは2
        # ここでは具体的な値である30は計算していないが、その具体的な数と合同である数字を用いて、今回桁で作成可能な数字のmodを数えているdp[i+1][2]にdp[i][4]を突っ込むことになる
        # modの世界では両辺に同じ数をかけても合同であるという性質を用いて、10をかけながら、桁ごとに数値を足していっていることになる

        for ki in range(13):
            dp[i+1][(ki * 10 + j) % 13] += dp[i][ki]
    else:
        # jが確定していないので、jになりうる値を全て試す
        # 0-9の10パターンの数字が考えられるので、全ての組み合わせ自体は*10になる
        # ? だと10パターン ??だと100パターンになるので、?が来ると、数字の組み合わせが10倍になるのは自明
        # 10**(?の数) の組み合わせの総数になる
        for j in range(10):
            for ki in range(13):
                dp[i+1][(ki * 10 + j) % 13] += dp[i][ki]
    
    for j in range(13):
        dp[i+1][j] %= MOD

print(dp[L][5])


# https://atcoder.jp/contests/abc129/tasks/abc129_e
s = list(input())
size = len(s)
mod = 10 ** 9 + 7
# dp[i][j] := i桁目まで確定したときの個数をjのフラグで一致==0or未満==1で管理していく
dp = [[0] * 2 for _ in range(100005)]

dp[0][0] = 1

# 前提として、、、
# a+bで桁が繰り上がるような組み合わせ（A&B) > 0の組み合わせは、AxorBとは一致しないため、考えなくていい
# 逆に繰り上がらない数字の組み合わせならXORとSUMが一致するから、DPで数えるべきなのは、合計がLを超えない組み合わせの個数を数えれば答えにたどり着ける
# その桁だけ見たときにa+bが0の場合と1の場合のみ考えればよくて、これらは桁ごとに独立で考えることができる

for i in range(size):
    # a+b = 0
    # aもbも0にするから、1通りしかない
    if s[i] == '0':
        # 次の桁に今の桁でL以下となることが確定している組み合わせの個数を足す
        dp[i+1][0] += dp[i][0]
        dp[i+1][0] %= mod
        # 次の桁に今の桁までLと一致している数の組み合わせの個数を足す
        dp[i+1][1] += dp[i][1]
        dp[i+1][1] %= mod
    else:
        # s[i]が1のときに、aもbも0にするので、dp[i][1]もL未満となることが確定するので、この遷移になる
        dp[i+1][1] += dp[i][0] + dp[i][1] % mod
        dp[i+1][1] %= mod
    # a+b = 1
    # aかbを1にするから、1にするほうのパターンが2通りある
    if s[i] == '0':
        # s[i]が0でa,bどちらかを1にするときは、未満が確定している個数のみ更新する
        dp[i+1][1] += dp[i][1] * 2 % mod
        dp[i+1][1] %= mod
    else:
        # s[i]が0のときにa,bのどちらかを1にするので、これまで一致している個数も未満が確定している個数も合わせて足す
        dp[i+1][0] += dp[i][0] * 2 % mod
        dp[i+1][0] %= mod
        dp[i+1][1] += dp[i][1] * 2 % mod
        dp[i+1][1] %= mod

ans = dp[size][1] + dp[size][0] % mod

print(ans)


# 入力された数値以下の整数でいずれかの桁に3を含む数

n = input()
l = len(n)
dp = [[[0] * 2 for i in range(2)] for j in range(100)]
dp[0][0][0] = 1

# dp[i][smaller][j]
for i in range(l):
    target = int(n[i])
    for smaller in range(2):
        for j in range(2):
            for x in range(10 if smaller == 1 else target+1):
                dp[i+1][smaller or int(x < target)][j or int(x == 3)] += dp[i][smaller][j]

print(dp[l][1][1] + dp[l][0][1])
