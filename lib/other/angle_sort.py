# 偏角ソート
# https://atcoder.jp/contests/abc481/tasks/abc481_e
from functools import cmp_to_key

# https://zenn.dev/asamichiruko/articles/a267450d8842d2
def half(p):
    """点 p が上半平面 (y > 0 または +x 軸上) に属する場合は 0 を, さもなくば 1 を返す"""
    x, y = p
    if y > 0 or (y == 0 and x >= 0):
        return 0
    else:
        return 1


def cross(a, b):
    """原点から見たベクトル a, b の外積 (符号付き面積) の値を返す"""
    ax, ay = a
    bx, by = b
    return ax * by - ay * bx


def norm2(p):
    """点 p の原点からの距離の二乗を返す"""
    x, y = p
    return x * x + y * y


def angle_cmp(a, b):
    """点 a, b の偏角と距離に基づく比較関数"""
    ha = half(a)
    hb = half(b)
    if ha < hb:
        return -1
    elif ha > hb:
        return 1

    c = cross(a, b)
    if c > 0:
        return -1
    elif c < 0:
        return 1

    da = norm2(a)
    db = norm2(b)
    if da < db:
        return -1
    elif da > db:
        return 1

    return 0

def is_same_dir(a, b):
    """点 a, b が原点でなく, かつ原点を始点とする同一半直線上にある場合は True を, さもなくば False を返す"""
    if (a[0] == 0 and a[1] == 0) or (b[0] == 0 and b[1] == 0):
        return False
    return half(a) == half(b) and cross(a, b) == 0

T = int(input())

def solve():
    N = int(input())
    XY = []
    for _ in range(N):
        x, y = map(int, input().split())
        XY.append((x, y))
    XY.sort(key=cmp_to_key(angle_cmp))
    XY = XY + XY
    ans = 0
    r = 0
    for i in range(N):
        r = max(i+1, r)
        while r < i + N and cross(XY[i], XY[r]) > 0:
            r += 1
        ans = max(ans, r-i)
    print(ans)
    return


for _ in range(T):
    solve()
