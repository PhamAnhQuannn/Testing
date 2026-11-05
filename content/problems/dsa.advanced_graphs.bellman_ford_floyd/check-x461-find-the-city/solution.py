def find_the_city(n, edges, distance_threshold):
    INF = float("inf")
    dist = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = dist[v][u] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    best_city = -1
    best_count = n + 1
    for i in range(n):
        count = sum(1 for j in range(n) if j != i and dist[i][j] <= distance_threshold)
        if count <= best_count:
            best_count = count
            best_city = i
    return best_city
