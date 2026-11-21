def tree_order(n, adj, root=0):
    '''
    非再帰の木DFS  O(N)   (再帰DFS + setrecursionlimit の代わり)
    adj[u] = [v, ...]  (重み付きなら v だけのリストに変換して渡す)
    戻り値: (order, parent, depth)
        order  : 行きがけ順 (親が必ず子より先)
        parent : 根は -1
    帰りがけの処理 (部分木DP) は reversed(order) で回す

    使用例:
        order, par, dep = tree_order(N, adj)
        size = [1] * N                       # 部分木サイズ
        for v in reversed(order):
            if par[v] >= 0: size[par[v]] += size[v]
    '''
    parent = [-1] * n
    depth = [0] * n
    order = []
    seen = [False] * n
    seen[root] = True
    st = [root]
    while st:
        u = st.pop()
        order.append(u)
        du = depth[u] + 1
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                depth[v] = du
                st.append(v)
    return order, parent, depth


def euler_tour(n, adj, root=0):
    '''
    非再帰オイラーツアー  O(N)
    戻り値: (tin, tout)  部分木 v = 区間 [tin[v], tout[v])
    v が u の子孫 ⇔ tin[u] <= tin[v] < tout[u]
    「本物のDFS順」(子を adj の順に潜る) なので、行き/帰りのタイミング処理もここに書ける

    使用例 (部分木クエリをセグ木/BITに落とす):
        tin, tout = euler_tour(N, adj)
        ft = FenwickTree(N)           # lib/acl/fenwicktree.py (0-indexed, 半開区間)
        ft.add(tin[v], x)             # 頂点 v に加算
        ft.sum(tin[v], tout[v])       # v の部分木和
    '''
    tin = [0] * n
    tout = [0] * n
    seen = [False] * n
    it = [0] * n
    t = 0
    seen[root] = True
    tin[root] = t; t += 1
    st = [root]
    while st:
        u = st[-1]
        au = adj[u]
        if it[u] < len(au):
            v = au[it[u]]
            it[u] += 1
            if not seen[v]:
                seen[v] = True
                # ---- 行きがけ (u -> v に潜る) ----
                tin[v] = t; t += 1
                st.append(v)
        else:
            # ---- 帰りがけ (u を抜ける) ----
            tout[u] = t
            st.pop()
    return tin, tout
