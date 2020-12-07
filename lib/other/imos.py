# 累積和で求めたい数列が完成できるような数列を作成する
N, Q = map(int, input().split())
imos = [0] * (N+1)
for _ in range(Q):
    l, r = map(int, input().split())
    l -= 1
    imos[l] += 1
    imos[r] -= 1

#print(*imos)
t = 0
ret = [0] * N
for i in range(N):
    t += imos[i]
    ret[i] = t

print(''.join([str(i%2) for i in ret]))
