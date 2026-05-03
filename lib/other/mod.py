# 大きな桁の数のMODをO(N)で計算するときの方法
for i in X:
    if one_pop > 0:
        one_mod = one_mod * 2 + int(i)
        one_mod %= one_pop
    zero_mod = zero_mod * 2 + int(i)
    zero_mod %= zero_pop
