def _sa_is(s, upper):
    '''SA-IS 本体. s: 0..upper の int リスト. 再帰の深さは O(logN)'''
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1] if s[0] < s[1] else [1, 0]
    ls = [False] * n
    for i in range(n - 2, -1, -1):
        a, b = s[i], s[i + 1]
        ls[i] = ls[i + 1] if a == b else a < b
    sum_l = [0] * (upper + 2)
    sum_s = [0] * (upper + 2)
    for i in range(n):
        if ls[i]:
            sum_l[s[i] + 1] += 1
        else:
            sum_s[s[i]] += 1
    for i in range(upper + 1):
        sum_s[i] += sum_l[i]
        sum_l[i + 1] += sum_s[i]

    sa = [-1] * n

    def induce(lms):
        for i in range(n):
            sa[i] = -1
        buf = sum_s[:]
        for d in lms:
            if d == n:
                continue
            c = s[d]
            sa[buf[c]] = d
            buf[c] += 1
        buf = sum_l[:]
        c = s[n - 1]
        sa[buf[c]] = n - 1
        buf[c] += 1
        for i in range(n):
            v = sa[i] - 1
            if v >= 0 and not ls[v]:
                c = s[v]
                sa[buf[c]] = v
                buf[c] += 1
        buf = sum_l[:]
        for i in range(n - 1, -1, -1):
            v = sa[i] - 1
            if v >= 0 and ls[v]:
                c = s[v] + 1
                buf[c] -= 1
                sa[buf[c]] = v

    lms_map = [-1] * (n + 1)
    lms = []
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = len(lms)
            lms.append(i)
    m = len(lms)
    induce(lms)

    if m:
        sorted_lms = [v for v in sa if lms_map[v] != -1]
        rec_s = [0] * m
        rec_upper = 0
        for i in range(1, m):
            l = sorted_lms[i - 1]
            r = sorted_lms[i]
            jl = lms_map[l] + 1
            jr = lms_map[r] + 1
            end_l = lms[jl] if jl < m else n
            end_r = lms[jr] if jr < m else n
            # LMS 部分文字列 s[l..end_l] と s[r..end_r] (両端含む) が等しいか
            if not (end_l - l == end_r - r and end_l < n
                    and s[l:end_l + 1] == s[r:end_r + 1]):
                rec_upper += 1
            rec_s[lms_map[r]] = rec_upper
        rec_sa = _sa_is(rec_s, rec_upper)
        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]
        induce(sorted_lms)
    return sa


def _sa_doubling(s):
    '''ダブリング + ソート O(Nlog^2N). s: 非負 int リスト (比較用・ベンチ用)'''
    n = len(s)
    sa = list(range(n))
    rnk = s[:]
    k = 1
    while k < n:
        w = max(rnk) + 2
        key = [a * w + b + 1 for a, b in zip(rnk, rnk[k:] + [-1] * k)]
        sa.sort(key=key.__getitem__)
        r = 0
        prev = key[sa[0]]
        for i in sa:
            ki = key[i]
            if ki != prev:
                r += 1
                prev = ki
            rnk[i] = r
        if r == n - 1:
            break
        k <<= 1
    return sa


def suffix_array(s, upper=None):
    '''
    接尾辞配列 (ACL互換, SA-IS) O(N + upper)
    s: str (ord で変換) または int のリスト (座標圧縮される)
    upper を渡すと s の各要素が 0..upper である前提で座標圧縮を省略
    返り値 sa: s[sa[0]:] < s[sa[1]:] < ... となる開始位置のリスト

    使用例:
        sa = suffix_array("abracadabra")   # [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
        sa = suffix_array([3, -1, 10**18]) # 座標圧縮してから構築
        sa = suffix_array(A, upper=26)     # A[i] in [0, 26]
        lcp = lcp_array(s, sa)             # 隣接接尾辞の最長共通接頭辞
    '''
    if upper is not None:
        return _sa_is(list(s), upper)
    if isinstance(s, str):
        t = [ord(c) for c in s]
        return _sa_is(t, max(t, default=0))
    vals = sorted(set(s))
    d = {v: i for i, v in enumerate(vals)}
    return _sa_is([d[x] for x in s], max(len(vals) - 1, 0))


def lcp_array(s, sa):
    '''
    LCP 配列 (Kasai) O(N)
    s: str または int のリスト, sa: suffix_array(s)
    返り値 長さ N-1, lcp[i] = s[sa[i]:] と s[sa[i+1]:] の最長共通接頭辞長

    使用例:
        sa = suffix_array(s); lcp = lcp_array(s, sa)
        # 異なる部分文字列の個数
        n * (n + 1) // 2 - sum(lcp)
    '''
    n = len(s)
    if n == 0:
        return []
    rnk = [0] * n
    for i, v in enumerate(sa):
        rnk[v] = i
    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        if h:
            h -= 1
        r = rnk[i]
        if r == 0:
            continue
        j = sa[r - 1]
        while j + h < n and i + h < n and s[j + h] == s[i + h]:
            h += 1
        lcp[r - 1] = h
    return lcp


def z_algorithm(s):
    '''
    Z アルゴリズム O(N)
    s: str または リスト
    返り値 z[i] = s と s[i:] の最長共通接頭辞長 (z[0] = N, 空なら [])

    使用例:
        z = z_algorithm("aaabaaaab")   # [9, 2, 1, 0, 3, 4, 2, 1, 0]
        # パターン検索: z_algorithm(P + '\\0' + T) で z[i] >= len(P) の位置
    '''
    n = len(s)
    if n == 0:
        return []
    z = [0] * n
    j = 0  # [j, j + z[j]) が最右の一致区間
    for i in range(1, n):
        k = j + z[j] - i
        if k > 0:
            k = min(k, z[i - j])
        else:
            k = 0
        while i + k < n and s[k] == s[i + k]:
            k += 1
        z[i] = k
        if j + z[j] < i + k:
            j = i
    z[0] = n
    return z
