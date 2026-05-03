# https://onlinejudge.u-aizu.ac.jp/problems/GRL_1_A
# 最もシンプルなダイクストラ
from heapq import heappop, heappush
V, E, r = map(int, input().split())
edge = [[] for _ in range(V)]
for _ in range(E):
    s,t,d = map(int, input().split())
    edge[s].append((d, t))

dp = [-1] * V

q = []
heappush(q, (0, r))

while len(q) > 0:
    d, x = heappop(q)
    if dp[x] > -1: continue
    dp[x] = d
    for nd, nt in edge[x]:
        heappush(q, (d+nd, nt))

for i in dp:
    print(i if i > -1 else "INF")




import heapq
def set_heapq(que, edge, used, v, add_dist=0):
    '''
    確定地点vからつながる辺を全てqueに設定し、返却する

    Parameters
    que : heapque(touple or list)
        辺を管理するキュー (距離、次の行き先)のtopuleまたはlistにて管理
    edge : list
        全ての辺を格納する二次元のリスト edge[0]にてノード0から伸びる辺であることを表し、
        edge[0] → [距離、次の行き先] を表すlistが格納されている
    v : int
        グラフ上のノード ダイクストラでは確定したノードがvにあたる
    add_dist : int
        確定した地点に足し合わせる距離 スタート地点以外では何かしらの値が追加されることになる

    Returns
    que : heapque(touple or list)
        引数queにvからつながる辺を追加したキュー
    '''
    for a,b in edge[v]:
        if used[b]:
            heapq.heappush(que,(a+add_dist,b))
    return que

def dijkstra_heap(n, s, edge):
    '''
    ダイクストラ法でsで指定された地点からの全てのノードまでの最短距離を返却
    
    Parameters
    n : int
        ノードの数
    s : int
        スタート地点
    edge : list
        全ての辺を格納する二次元のリスト edge[0]にてノード0から伸びる辺であることを表し、
        edge[0] → [距離、次の行き先] を表すlistが格納されている

    Returns
    d : list
        スタート地点から全てのノードの最短距離のリスト
    '''
    d = [float("inf")] * n
    used = [True] * n #True:未確定
    d[s], used[s] = 0, False
    edgelist = set_heapq([], edge, used, s)
    while len(edgelist):
        a, b = heapq.heappop(edgelist)
        # 確定していない頂点の中から最小の距離のものを探す
        if not used[b]:
            continue
        d[b], used[b] = a, False
        # 確定地点vからつながる辺を全て優先度付きキューに入れる
        edgelist = set_heapq(edgelist, edge, used, b, d[b])
    return d



# https://atcoder.jp/contests/abc164/tasks/abc164_e
# ダイクストラだけど、最短経路を格納するDPテーブルをいい感じに更新すると考えたほうがいいかも
from heapq import heappop, heappush, heapify

INF = 1 << 18
n, m, s = map(int, input().split())
s = min([s, 50*n])
tree = [[] for _i in range(n)]
for _i in range(m):
    u, v, a, b = map(int, input().split())
    u, v = u-1, v-1
    tree[u].append([v, a, b])
    tree[v].append([u, a, b])

cd = [[0] * 2 for _ in range(n)]
for i in range(n):
    cd[i][0], cd[i][1] = map(int, input().split())

# 距離だけのダイクストラではなく、距離（時間）* 所持金 という二次元の状態で各ノードの状態を作成し、そこに最短距離の数値を格納していく
dp = [[INF for _i in range(50*n+1)] for _j in range(n)]
# heapqueは(時間、ノード（1インデックス）、所持金（銀貨の枚数）)
hq = [[0, 0, s]]
dp[0][s] = 0
heapify(hq)
while hq:
    # 優先度付きキューから今現在最短で到達可能なノードを取り出す
    # t := 時間 p := ノード g := 所持金
    t, p, g = heappop(hq)
    # g+cd[p][0] <= 50 * n := 換金後に必要以上の所持金にならない場合
    if g+cd[p][0] <= 50*n:
        # x := 換金した場合の所要時間の合計
        # y := 換金後の所持金
        x, y = t+cd[p][1], g+cd[p][0]
        # 現在のpのノードへ所持金yでたどり着くルートの最短時間と比較して換金したほうが速く到達可能な場合
        if dp[p][y] > x:
            # dpテーブルを更新し、キューに時間、現在地、所持金を突っ込む
            dp[p][y] = x
            heappush(hq, [x, p, y])
    for x, y, z in tree[p]:
        # g-y := 手持ちの銀貨で移動可能な辺かどうか
        # dp[x][g-y] > t+z := このエッジをたどったルートがより速く到達可能なルートかどうか
        if g-y >= 0 and dp[x][g-y] > t+z:
            # 条件を満たす場合はdpテーブルを更新してキューにノードを追加する
            dp[x][g-y] = t+z
            # t+z := このエッジを通った場合の時間
            # x := ノード
            # g-y := 所持金
            heappush(hq, [t+z, x, g-y])

for i in dp[1:]:
    print(min(i))

