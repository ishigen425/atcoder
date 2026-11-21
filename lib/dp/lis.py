from bisect import bisect_left, bisect_right


def lis(a, strict=True, restore=False):
    '''
    最長増加部分列  O(N log N)
    strict=True : 狭義単調増加 (a_i < a_j)   False: 広義 (a_i <= a_j)
    restore=True で (長さ, 部分列) を返す

    使用例:
        lis([3, 1, 4, 1, 5, 9, 2, 6])                 # 4
        lis([3, 1, 4, 1, 5, 9, 2, 6], restore=True)   # (4, [1, 4, 5, 9])
        lis([-x for x in a])                          # 最長減少部分列
        # 各 i で終わる LIS 長が欲しい → lis_ending_at(a)
    '''
    bis = bisect_left if strict else bisect_right
    dp = []
    if not restore:
        for x in a:
            i = bis(dp, x)
            if i == len(dp): dp.append(x)
            else: dp[i] = x
        return len(dp)
    idx = []          # dp[k] を達成する a のインデックス
    prev = [-1] * len(a)
    for j, x in enumerate(a):
        i = bis(dp, x)
        if i == len(dp):
            dp.append(x); idx.append(j)
        else:
            dp[i] = x; idx[i] = j
        prev[j] = idx[i - 1] if i else -1
    res = []
    j = idx[-1] if idx else -1
    while j >= 0:
        res.append(a[j])
        j = prev[j]
    return len(dp), res[::-1]


def lis_ending_at(a, strict=True):
    '''各 i について a[i] で終わる LIS の長さ'''
    bis = bisect_left if strict else bisect_right
    dp, res = [], []
    for x in a:
        i = bis(dp, x)
        if i == len(dp): dp.append(x)
        else: dp[i] = x
        res.append(i + 1)
    return res
