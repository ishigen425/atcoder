def serach(target, array):
    l, r = -1, len(array)
    while r - l > 1:
        m = (l+r)//2
        if array[m] == target:
            return m, len(array) - m - 1
        elif array[m] < target:
            l = m
        else:
            r = m
    return l+1, len(array) - r

