def bellman_ford(s):
    '''
    ベルマンフォード法

    Parameters
    s : int
        初期位置
    
    Returns
    d : list
        sからの最短経路のコストを表すリスト
    '''
    INIT = 10 ** 9
    d = [INIT] * V
    d[s] = 0
    while True:
        update = False
        for i in range(E):
            e = ed[i]
            if d[e.from_node] != INIT and d[e.to_node] > d[e.from_node] + e.cost:
                d[e.to_node] = d[e.from_node] + e.cost
                update = True
        if not update:
            return d
class edge:
    def __init__(self, from_node, to_node, cost):
        self.from_node = from_node
        self.to_node = to_node
        self.cost = cost
