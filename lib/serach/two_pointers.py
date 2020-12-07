# しゃくとり法
# https://qiita.com/drken/items/ecd1a472d3a0e7db8dce
r = 0
cnt = 0
s = 0
for l in range(n):
    while r < n and s < k:
        s += A[r]
        r += 1
    if s >= k:
        cnt += n-r+1
    s -= A[l]


n=int(input())
a=list(map(int,input().split()))
# s:今の範囲(l,r)での合計
# r:idx番号
# ans:組み合わせの数
ans=s=r=0
for l in range(n):
    # rをインデックス範囲内かつ今までの合計と配列Aの対象の数の論理積が0のうちはrを進める
    while r<n and s&a[r]==0:
        s+=a[r]
        r+=1
    s-=a[l]
    ans+=r-l

print(ans)

# https://atcoder.jp/contests/abc098/tasks/arc098_b


# https://onlinejudge.u-aizu.ac.jp/problems/0600
N = int(input())
A = [int(input()) for _ in range(N)]
total = sum(A)
A = A + A

def check(next_piece, piece_size, mid):
    for i in range(N):
        # 1番目のピース (iからniまで)
        ni = next_piece[i]
        if ni == -1: continue
        if piece_size[i] >= total: continue

        # 2番めのピース (niからnniまで)
        ni %= N
        nni = next_piece[ni]
        if nni == -1: continue

        # 3番目のピース (合計-1番目のピース-2番目のピース)
        if total - piece_size[i] - piece_size[ni] >= mid:
            # 最小値の最大値を二分探索で探しているので、全てのピースがmid以上であればTrueにする
            return True
    return False

def tow_pointers(mid):
    # しゃくとり法でインデックスの左側を全探索しつつ、合計がmid以上になる最小区間がどこまでかを求める
    # next_piece[i] := iから計算した合計がmid以上になる最小区間の終端インデックス
    # piece_size[i] := iから計算した合計がmid以上になる最小区間の終端インデックスまでの合計値
    next_piece = [-1] * N
    piece_size = [-1] * N
    right, amount = 0, 0
    for left in range(N):
        while right < N * 2 and amount < mid:
            amount += A[right]
            right += 1
        if amount >= mid:
            # amoutがmid以上の場合、それぞれの記録用配列に値を格納する
            next_piece[left] = right
            piece_size[left] = amount
        # 次のループのために始端インデックスの値を合計値から引いておく
        amount -= A[left]
    return next_piece, piece_size

# 二分探索
low, high = 0, 1 << 60
while high - low > 1:
    # オーバーフローを懸念してこの方法で中間地点を計算している
    mid = low + (high - low) // 2
    next_piece, piece_size = tow_pointers(mid)
    if check(next_piece, piece_size, mid):
        low = mid
    else:
        high = mid

print(low)


# https://atcoder.jp/contests/joi2018yo/submissions/me
# しゃくとりと二分探索の組み合わせ
N, K, L = map(int, input().split())
a = list(map(int, input().split()))

def tow_pointer(mid):
    right, num = 0, 0
    cnt = 0
    for left in range(N):
        while right < N and cnt < K:
            if a[right] <= mid: cnt += 1
            right += 1
        if cnt < K: break
        num += N - right + 1
        if a[left] <= mid: cnt -= 1
    return num >= L


# 二分探索
low, high = 0, N
while high - low > 1:
    mid = (high + low) // 2
    ok = tow_pointer(mid)
    if ok: high = mid
    else: low = mid

print(high)
