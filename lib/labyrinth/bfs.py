C[sy-1][sx-1] = 0
pre_list = [(sy-1,sx-1)]
count = 0
 
while C[gy-1][gx-1] == '.' or len(pre_list) > 0:
    count += 1
    next_list = []
    for y,x in pre_list:
        for i,j in ((1,0),(0,-1),(0,1),(-1,0)):
            if y+i < 0 or x+j < 0 or y+i >= H or x+j >= W:
                continue
            if C[y+i][x+j] == '.':
                C[y+i][x+j] = count
                next_list.append((y+i,x+j))
    pre_list = next_list
print(count)
