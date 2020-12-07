def kruskal(edge, n):
    '''
    クラスカル法で最小全域木を作成する(UnionFindを使う)

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
    union = UnionFind(n)
    res = 0
    ret = []
    for x, y, c in edge:
        if not union.is_same_group(x, y):
            union.unite(x, y)
            ret.append((x, y, c))
            res += c
    return re
