import sys
sys.setrecursionlimit(10**9)

# child_node_cnt is nessesary in order to exclude itself.
class Node():
    def __init__(self):
        self.child_node_cnt = 0
        self.next = {}
    
    def add(self, value):
        self.child_node_cnt += 1
        if value in self.next:
            return self.next[value]
        new_node = Node()
        self.next[value] = new_node
        return new_node

N = int(input())
S = [input() for _ in range(N)]
root = Node()

for s in S:
    current = root
    for c in s:
        current = current.add(c)
    current.add("")

ans = 0
def dfs(node, s, i):
    global ans
    ans = max(ans, i)
    if len(s) <= i: return
    if s[i] in node.next and node.next[s[i]].child_node_cnt > 1:
        dfs(node.next[s[i]], s, i+1)

for s in S:
    ans = 0
    dfs(root, s, 0)
    print(ans)
