from Point import Point

def initialize_single_source(graph, start):
    distance = {}
    predecessor = {}
    for vertex in graph:
        distance[vertex] = float('inf')
        predecessor[vertex] = None
    distance[start] = 0
    return distance, predecessor

def relax(u, v, weight, distance, predecessor):
    if distance[v] > distance[u] + weight:
        distance[v] = distance[u] + weight
        predecessor[v] = u

def bellman_ford(graph, start):
    distance, predecessor = initialize_single_source(graph, start)
    for _ in range(len(graph) - 1):
        for u in graph:
            for v in graph[u]:
                weight = u.Distance(v)
                relax(u, v, weight, distance, predecessor)
    return distance, predecessor
