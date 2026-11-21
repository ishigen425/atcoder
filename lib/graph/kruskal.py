def kruskal(edge, n):
    '''
    クラスカル法で最小全域木を作成する(lib/acl/dsu.py の DSU を使う, 0-indexed)

    Parameters
    edge : list([from, to, c])
        全ての辺を[from, to, c]で表す
    n : int
        ノードの数
    
    Returns
    res : int
        最小全域木の全ての辺の総和
    '''
    edge.sort(key = lambda x:x[2])
    uf = DSU(n)
    res = 0
    for x, y, c in edge:
        if not uf.same(x, y):
            uf.merge(x, y)
            res += c
    return res

