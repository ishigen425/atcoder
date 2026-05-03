T = int(input())

def main():
    N, M = map(int, input().split())
    UV = [tuple(map(int, input().split())) for _ in range(M)]
    W = int(input())
    S = [input() for _ in range(N)]
    edges = [[] for _ in range(N)]
    for u, v in UV:
        edges[u-1].append(v-1)
        edges[v-1].append(u-1)
    for i in range(N):
        edges[i].append(i)
    
    visited = set()
    now_list = []
    for i in range(N):
        if S[i][0] == "o":
            now_list.append(i)
    next_list = set()
    cnt = 0
    ans = False
    while now_list and not ans:
        cnt += 1
        week = cnt % W
        for now in now_list:
            if now * W + week in visited:
                ans = True 
                break
            visited.add(now * W + week)
            for nx in edges[now]:
                if S[nx][week] == "x": continue
                next_list.add(nx)
        now_list = list(next_list)
        next_list = set()
    print("Yes" if ans else "No")
    return


for _ in range(T):
    main()
