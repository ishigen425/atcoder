def dfs(x, y, field):
    '''
    深さ優先探索でゴールまでたどり着けるかどうか判定する

    Parameters
    x : int
        スタート地点
    y : int 
        ゴール地点
    field : list(string)
        平面上の迷路
    
    Returns
    available : bool
        ゴール可能かどうか
    '''
    for nx, ny in ((1,0), (0,1),(-1,0),(0,-1)):
        field[y][x] = "#"
        nx += x
        ny += y
        if nx < W and ny < H and 0 <= nx and 0 <= ny:
            if field[ny][nx] == "g":
                return True
            elif field[ny][nx] == "#":
               continue
            if dfs(nx, ny, field):
                return True
    return False
