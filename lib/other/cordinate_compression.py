# 座標圧縮
H, W = map(int, input().split())
field = [input() for _ in range(H)]

columns, rows = set([W-1]), set([H-1])

for h in range(H-1):
    ok = False
    for w in range(W):
        if field[h][w] != field[h+1][w]:
            ok = True
    if ok:
        rows.add(h)

for w in range(W-1):
    ok = False
    for h in range(H):
        if field[h][w] != field[h][w+1]:
            ok = True
    if ok:
        columns.add(w)

ans = [[] * len(columns) for _ in range(len(rows))]
row_cnt = -1
for h in range(H):
    if not h in rows:
        continue
    row_cnt += 1
    for w in range(W):
        if w in columns:
            ans[row_cnt].append(field[h][w])

print(*ans, sep="\n")

