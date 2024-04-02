class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True

def kruskal(graph):
    n = len(graph)
    edges = [(graph[u][v], u, v) for u in range(n) for v in range(u + 1, n)]
    edges.sort()

    mst = []
    uf = UnionFind(n)

    for cost, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, cost))

    return mst

def satisfy_requirements(mst, requirements):
    for a, b, t in requirements:
        found = False
        for u, v, cost in mst:
            if (u == a and v == b) or (u == b and v == a):
                if cost <= t:
                    found = True
                    break
        if not found:
            return False
    return True

def main():
    N, M = map(int, input().split())
    graph = [[float('inf')] * N for _ in range(N)]

    for _ in range(M):
        u, v, t = map(int, input().split())
        graph[u - 1][v - 1] = t
        graph[v - 1][u - 1] = t

    K = int(input())
    proposals = []
    for _ in range(K):
        u, v, t, c = map(int, input().split())
        proposals.append((u - 1, v - 1, t, c))

    P = int(input())
    requirements = []
    for _ in range(P):
        a, b, t = map(int, input().split())
        requirements.append((a - 1, b - 1, t))

    mst = kruskal(graph)
    satisfied_proposals = []
    for i, (u, v, _, _) in enumerate(proposals, start=1):
        if (u, v) not in [(x, y) for x, y, _ in mst] and (v, u) not in [(x, y) for x, y, _ in mst]:
            mst.append((u, v, graph[u][v]))
            if satisfy_requirements(mst, requirements):
                satisfied_proposals.append(i)

    if not satisfied_proposals:
        print(-1)
    else:
        print(len(satisfied_proposals))
        print(*satisfied_proposals)

if __name__ == "__main__":
    main()
